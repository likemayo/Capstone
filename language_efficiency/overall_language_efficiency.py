import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv('cleaned_for_analysis.csv')

# Remove outliers (top/bottom 1%) for Exec_Time_num and Memory_num
for col in ['Exec_Time_num', 'Memory_num']:
    q_low = df[col].quantile(0.01)
    q_high = df[col].quantile(0.99)
    df = df[(df[col] >= q_low) & (df[col] <= q_high)]

# Aggregate mean and median execution time and memory usage by language
agg = df.groupby('Language').agg(
    mean_exec_time=('Exec_Time_num', 'mean'),
    median_exec_time=('Exec_Time_num', 'median'),
    mean_memory=('Memory_num', 'mean'),
    median_memory=('Memory_num', 'median'),
    count=('Exec_Time_num', 'count')
).sort_values('mean_exec_time')
agg.to_csv('overall_language_efficiency.csv')

# Barplot: Mean execution time by language
plt.figure(figsize=(12,6))
sns.barplot(x=agg.index, y=agg['mean_exec_time'])
plt.xticks(rotation=45, ha='right')
plt.title('Mean Execution Time by Language (Overall)')
plt.ylabel('Mean Execution Time (sec)')
plt.xlabel('Language')
plt.tight_layout()
plt.savefig('overall_mean_exec_time.png')
plt.close()

# Barplot: Mean memory usage by language
plt.figure(figsize=(12,6))
sns.barplot(x=agg.index, y=agg['mean_memory'])
plt.xticks(rotation=45, ha='right')
plt.title('Mean Memory Usage by Language (Overall)')
plt.ylabel('Mean Memory Usage (MB)')
plt.xlabel('Language')
plt.tight_layout()
plt.savefig('overall_mean_memory.png')
plt.close()

print('Overall language efficiency analysis complete. Results saved as overall_language_efficiency.csv, overall_mean_exec_time.png, and overall_mean_memory.png')
