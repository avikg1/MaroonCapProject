import pandas as pd
from sklearn.linear_model import LinearRegression
import sys

from check_user import DIR_PATH

sys.path.append(f"{DIR_PATH}/MaroonCapProject/functions") # Add functions module to the path

def preprocess_data(file_path):
    data = pd.read_csv(file_path, header=0, usecols=["Market", "Risk_Free", "SMB", "HML", "Long_Rate"])
    data["SMB_interaction"] = data["SMB"] * data["Long_Rate"]
    data["HML_interaction"] = data["HML"] * data["Long_Rate"]
    data["M-RF"] = data["Market"] - data["Risk_Free"]
    data.drop(['Market', 'Risk_Free', 'Long_Rate'], axis=1, inplace=True)
    return data

def calculate_interactions(data, returner_df, factors):
    interactions = []
    for contender in returner_df.columns:
        if "Risk_Free" in contender or "Unnamed" in contender:
            continue
        returner_df[contender] = pd.to_numeric(returner_df[contender], errors='coerce')
        merged_data = pd.merge(returner_df[["Risk_Free", contender]], data, left_index=True, right_index=True, how="left").dropna()
        merged_data["Return-Rf"] = merged_data[contender] - merged_data["Risk_Free"]
        if len(merged_data) <= min_num_of_data_points:
            continue
        X = merged_data[factors].values
        y = merged_data["Return-Rf"].values.reshape(-1, 1)

        reg = LinearRegression().fit(X, y)
        r_squared = reg.score(X, y)  # Calculate R^2 score
        interactions.append([contender] + list(reg.coef_[0]) + [r_squared])  # Append R^2 score to interactions
    return interactions

# Constants
min_num_of_data_points = 120
file_path = f'{DIR_PATH}/MaroonCapProject/clean/train_data.csv'

# Preprocess data
everyday = preprocess_data(file_path)

# Read and clean returner data
returner_df = pd.read_csv(file_path, header=0).drop(["index", "Date", "Market", "SMB", "HML", "Long_Rate"], axis=1)

# Calculate interactions for different factor models
for factors, output_file in [(["SMB", "HML", "SMB_interaction", "HML_interaction", "M-RF"], f"{DIR_PATH}/MaroonCapProject/clean/BIGGESTWIN.csv"),
                             (["SMB", "SMB_interaction", "M-RF"], f"{DIR_PATH}/MaroonCapProject/clean/SMB_win.csv"),
                             (["HML", "HML_interaction", "M-RF"], f"{DIR_PATH}/MaroonCapProject/clean/HML_win.csv"),
                             (["HML", "SMB", "M-RF"], f"{DIR_PATH}/MaroonCapProject/clean/classic.csv")]:
    interactions_data = calculate_interactions(everyday, returner_df, factors)
    columns_names = ['Stock'] + factors + ['R_squared']  # Add 'R_squared' to the column names
    interactions_df = pd.DataFrame(interactions_data, columns=columns_names)
    wanted_columns = [col for col in interactions_df.columns if "interaction" in col] + ["Stock", "R_squared"]  # Keep 'R_squared' in the wanted columns
    result_df = interactions_df[wanted_columns]
    
    # Print out R^2 scores
    print(f"R^2 scores for {output_file}:")
    print(result_df[['Stock', 'R_squared']])
    
    result_df.drop(columns=['R_squared'], inplace=True)  # Optional: Drop 'R_squared' if not needed in the output file
    result_df.to_csv(output_file, index=False)
