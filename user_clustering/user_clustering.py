import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load cleaned data
df = pd.read_csv('cleaned_for_analysis.csv')

# 1. Count error types per user
error_types = df['Result'].str.lower().unique().tolist()
error_types = [e for e in error_types if e != 'accepted']
user_error_counts = df[df['Result'].str.lower() != 'accepted'].groupby(['Username', 'Result']).size().unstack(fill_value=0)

# 2. Fill missing error types (if any)
for e in error_types:
    if e not in user_error_counts.columns:
        user_error_counts[e] = 0
user_error_counts = user_error_counts[error_types]

# 3. Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(user_error_counts)

# 4. KMeans clustering (choose k=3 for illustration)
k = 3
kmeans = KMeans(n_clusters=k, random_state=42)
clusters = kmeans.fit_predict(X_scaled)
user_error_counts['Cluster'] = clusters

# 5. PCA for 2D visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
user_error_counts['PCA1'] = X_pca[:,0]
user_error_counts['PCA2'] = X_pca[:,1]

# 6. Plot clusters
plt.figure(figsize=(10,7))
sns.scatterplot(data=user_error_counts, x='PCA1', y='PCA2', hue='Cluster', palette='Set2', s=60)
plt.title('User Clusters by Error Patterns')
plt.xlabel('PCA1')
plt.ylabel('PCA2')
plt.legend(title='Cluster')
plt.tight_layout()
plt.savefig('user_clusters.png')
plt.close()

# 7. Save cluster assignments
user_error_counts.reset_index()[['Username', 'Cluster']].to_csv('user_cluster_assignments.csv', index=False)
print('Clustering complete. Results saved as user_clusters.png and user_cluster_assignments.csv')
