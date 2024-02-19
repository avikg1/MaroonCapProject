import pandas as pd
from sklearn.linear_model import LinearRegression
import sys
import joblib
import os

from check_user import DIR_PATH

sys.path.append(f"{DIR_PATH}/MaroonCapProject/functions") # Add functions module to the path


models_dir = f'{DIR_PATH}/MaroonCapProject/clean/model/'
# Function to load all models from the directory
def load_models(models_dir):
    models = {}
    for filename in os.listdir(models_dir):
        if filename.endswith("_model.joblib"):
            # Extract the contender name from the filename
            contender = filename.replace('.joblib', '')
            # Load the model
            model_path = os.path.join(models_dir, filename)
            models[contender] = joblib.load(model_path)
    return models

def preprocess_data(file_path):
    data = pd.read_csv(file_path, header=0)
    data["SMB_interaction"] = data["SMB"] * data["Long_Rate"]
    data["HML_interaction"] = data["HML"] * data["Long_Rate"]
    data["M-RF"] = data["Market"] - data["Risk_Free"]
    data.drop(['Market', 'Risk_Free', 'Long_Rate'], axis=1, inplace=True)
    return data

def predict_with_loaded_models(test_data, models_dir, factors):
    # Initialize an empty DataFrame for predictions
    predictions_df = pd.DataFrame()
    
    for filename in os.listdir(models_dir):
        if filename.endswith(".joblib"):
            model = joblib.load(os.path.join(models_dir, filename))
            contender = filename.replace('.joblib', '')
            
        
        if contender not in test_data.columns:
            continue
            
        X_test = test_data[factors].values
        model.predict(X_test)
        # Predict and assign to DataFrame
        predictions_df[contender] = model.predict(X_test)
    
    return predictions_df

# Load test data
test_file_path = f'{DIR_PATH}/MaroonCapProject/clean/test_data.csv'  # Make sure to use the test data path
test_data = preprocess_data(test_file_path)


factors = ["SMB", "HML", "SMB_interaction", "HML_interaction", "M-RF"]

print(test_data.head())  # Check the first few rows
print(test_data[factors].head())  # Specifically check the factors


# Load models and predict
loaded_models_dir = f'{DIR_PATH}/MaroonCapProject/clean/model/'
predictions_df = predict_with_loaded_models(test_data, loaded_models_dir, factors)

# Save predictions to CSV
predictions_df.to_csv(f'{DIR_PATH}/MaroonCapProject/clean/predictions.csv', index=False)
