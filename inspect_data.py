
import pandas as pd
import numpy as np

# Load the data
file_path = 'cleaned_data.csv'
df = pd.read_csv(file_path)

# Convert date columns
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
if 'Join_Date' in df.columns:
	df['Join_Date'] = pd.to_datetime(df['Join_Date'], errors='coerce')

# Convert Exec_Time, Memory, Time_Limit, Memory_Limit to numeric
def parse_time(x):
	try:
		return float(str(x).replace('sec', '').strip())
	except:
		return np.nan
def parse_memory(x):
	try:
		return float(str(x).replace('M', '').replace('MB', '').strip())
	except:
		return np.nan
df['Exec_Time_num'] = df['Exec_Time'].apply(parse_time)
df['Memory_num'] = df['Memory'].apply(parse_memory)
df['Time_Limit_num'] = df['Time_Limit'].apply(parse_time)
df['Memory_Limit_num'] = df['Memory_Limit'].apply(parse_memory)

# Clean accuracy column (remove % if present)
if 'Accuracy (%)' in df.columns:
	df['Accuracy_num'] = df['Accuracy (%)'].apply(lambda x: float(str(x).replace('%','').strip()) if pd.notnull(x) else np.nan)

# Create a cleaned DataFrame for analysis (drop rows with missing key values)
key_columns = ['Quality', 'Implementation_difficulty', 'Concept_difficulty', 'World_Rank', 'Points', 'Problems_Solved']
df_clean = df.dropna(subset=key_columns)

# Show info for both DataFrames
print('--- Original DataFrame info ---')
df.info()
print('\n--- Cleaned DataFrame info (dropped rows with missing key values) ---')
df_clean.info()


print('\n--- Head of cleaned DataFrame ---')
print(df_clean.head())

# Save cleaned DataFrame to CSV for download
df_clean.to_csv('cleaned_for_analysis.csv', index=False)
print('\nSaved cleaned DataFrame as cleaned_for_analysis.csv')
