# this is a vibecoded mess
# ================================
# Life Expectancy Dataset Preprocessing
# ================================

# Terminal command to install required packages:
# ------------------------------------------------
# pip install pandas numpy scikit-learn matplotlib seaborn

# ------------------------------------------------
# Step 1: Import required libraries
# ------------------------------------------------
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ------------------------------------------------
# Step 2: Load dataset
# Replace 'dataset.csv' with your CSV file name
# ------------------------------------------------
df = pd.read_csv("countries.csv")

# Preview the dataset
print("Initial Dataset:\n", df.head())

# ------------------------------------------------
# Step 3: Handle missing values
# Strategy:
# - For numeric columns: fill with median
# - For categorical columns (country name): fill with mode
# ------------------------------------------------
numeric_cols = ["gdp_pcap", "co2_pcap", "child_mort_pcap", "lex"]
categorical_cols = ["name"]

# Fill numeric missing values with median
for col in numeric_cols:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].median(), inplace=True)

# Fill categorical missing values with mode
for col in categorical_cols:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].mode()[0], inplace=True)

# Verify missing values handled
print("\nMissing Values after imputation:\n", df.isnull().sum())

# ------------------------------------------------
# Step 4: Encode non-numerical classes
# Convert 'Country' column to numeric using LabelEncoder
# ------------------------------------------------
le = LabelEncoder()
df["Country_encoded"] = le.fit_transform(df["name"])

# Drop original country column if not needed
# df.drop('Country', axis=1, inplace=True)

# ------------------------------------------------
# Step 5: Flag obvious outliers
# Using z-score method to flag numeric outliers
# ------------------------------------------------

z_scores = np.abs(stats.zscore(df[numeric_cols]))
threshold = 3  # Common threshold for extreme outliers
outliers = z_scores > threshold

# Add a column to indicate if row has any outlier
df["Outlier_Flag"] = outliers.any(axis=1)

# Optional: inspect outliers
print("\nRows flagged as outliers:\n", df[df["Outlier_Flag"]])

# ------------------------------------------------
# Step 6: Normalize numeric values (0-1 scaling)
# Use MinMaxScaler for all numeric columns except LifeExpectancy (target)
# ------------------------------------------------
scaler = MinMaxScaler()

# Features to scale (exclude target)
features_to_scale = ["gdp_pcap", "co2_pcap", "child_mort_pcap"]
df[features_to_scale] = scaler.fit_transform(df[features_to_scale])

# Optional: check the scaled values
print("\nScaled numeric features:\n", df[features_to_scale].head())

# ------------------------------------------------
# Step 7: Save preprocessed dataset
# ------------------------------------------------
df.to_csv("dataset_preprocessed.csv", index=False)
print("\nPreprocessing complete. Saved as 'dataset_preprocessed.csv'.")

# ------------------------------------------------
# Step 8: Optional Visualizations
# Plot distributions to check preprocessing
# ------------------------------------------------
sns.pairplot(df[numeric_cols])
plt.show()
