import pandas as pd
import numpy as np

# Reconstruct user error counts with clusters
df_all = pd.read_csv('cleaned_for_analysis.csv')
error_types = df_all['Result'].str.lower().unique().tolist()
error_types = [e for e in error_types if e != 'accepted']
user_error_counts = df_all[df_all['Result'].str.lower() != 'accepted'].groupby(['Username', 'Result']).size().unstack(fill_value=0)
for e in error_types:
    if e not in user_error_counts.columns:
        user_error_counts[e] = 0
user_error_counts = user_error_counts[error_types]
clusters = pd.read_csv('user_cluster_assignments.csv')
user_error_counts = user_error_counts.reset_index().merge(clusters, on='Username')

# Only use numeric error columns for summary
numeric_error_cols = [col for col in user_error_counts.columns if col not in ['Username', 'Cluster', 'PCA1', 'PCA2'] and user_error_counts[col].dtype in [int, float, np.int64, np.float64]]
cluster_summary = user_error_counts.groupby('Cluster')[numeric_error_cols].mean()

# Save summary
cluster_summary.to_csv('cluster_error_summary.csv')
print('Cluster error summary saved as cluster_error_summary.csv')
print(cluster_summary)
