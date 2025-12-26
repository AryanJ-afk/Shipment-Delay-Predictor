import xgboost as xgb
import pandas as pd
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score

# Load the model
bst = xgb.Booster()
bst.load_model('xgboost-model')  # or the correct filename inside tar.gz

# Load validation data
val_df = pd.read_csv('/Users/aryanjha/Desktop/MsAI/Personal/Python/shipment_delay_prediction/src/tmp/validation.csv')
X_val = val_df.drop(columns=['delayed'])
y_val = val_df['delayed']

categorical_cols = ['customer_state', 'seller_state']
for col in categorical_cols:
    X_val[col] = X_val[col].astype('category')

# Now create DMatrix with enable_categorical=True
dval = xgb.DMatrix(X_val, label=y_val, enable_categorical=True)

# Make predictions
y_pred_prob = bst.predict(dval)

# Apply threshold
y_pred_class = (y_pred_prob >= 0.6).astype(int)

# Compute metrics
auc = roc_auc_score(y_val, y_pred_prob)
accuracy = accuracy_score(y_val, y_pred_class)
f1 = f1_score(y_val, y_pred_class)

print("AUC:", auc)
print("Accuracy:", accuracy)
print("F1-score:", f1)
