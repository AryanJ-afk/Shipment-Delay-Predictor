import boto3
import pandas as pd
import time
import argparse

def export_athena_table_to_csv(database, table_name, output_csv, region='ap-south-1', s3_temp='s3://your-bucket/athena-temp/'):
    """
    Query an Athena table and save the full results to a local CSV, handling pagination.

    Parameters:
    - database: Athena database name
    - table_name: Table to query (e.g., sagemaker_orders)
    - output_csv: Local path to save CSV
    - region: AWS region
    - s3_temp: S3 folder for Athena query results
    """
    session = boto3.Session(region_name=region)
    athena = session.client("athena")

    query = f"SELECT * FROM {table_name}"

    # Start Athena query execution
    resp = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": database},
        ResultConfiguration={"OutputLocation": s3_temp},
    )
    qid = resp["QueryExecutionId"]

    # Wait for query to finish
    while True:
        time.sleep(2)
        q = athena.get_query_execution(QueryExecutionId=qid)
        state = q["QueryExecution"]["Status"]["State"]
        if state in ("SUCCEEDED", "FAILED", "CANCELLED"):
            if state != "SUCCEEDED":
                raise RuntimeError(f"Athena query failed: {q}")
            break

    # Fetch results with pagination
    rows = []
    next_token = None
    while True:
        if next_token:
            res = athena.get_query_results(QueryExecutionId=qid, NextToken=next_token)
        else:
            res = athena.get_query_results(QueryExecutionId=qid)

        # Get column names from metadata
        if not rows:
            cols = [c["Label"] for c in res["ResultSet"]["ResultSetMetadata"]["ColumnInfo"]]

        # Get data rows
        data_rows = res["ResultSet"]["Rows"]
        if not rows:
            # Skip header row only for the first page
            data_rows = data_rows[1:]
        rows.extend([[d.get("VarCharValue") for d in r["Data"]] for r in data_rows])

        next_token = res.get("NextToken")
        if not next_token:
            break

    # Convert to DataFrame and save
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(output_csv, index=False)
    print(f"Athena table '{table_name}' fully saved to {output_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Athena table to CSV")
    parser.add_argument('--database', required=True, help='Athena database name')
    parser.add_argument('--table', required=True, help='Athena table name')
    parser.add_argument('--output', required=True, help='Local CSV path')
    parser.add_argument('--region', default='ap-south-1', help='AWS region')
    parser.add_argument('--s3_temp', default='s3://your-bucket/athena-temp/', help='S3 temp folder for Athena queries')

    args = parser.parse_args()
    export_athena_table_to_csv(args.database, args.table, args.output, args.region, args.s3_temp)
