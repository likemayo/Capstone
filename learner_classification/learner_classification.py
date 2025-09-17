import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns


# Load cleaned data
df = pd.read_csv('cleaned_for_analysis.csv')
# Fill NaNs in relevant columns before aggregation
for col in ['Problems_Solved', 'World_Rank', 'Solved_Classical_Count', 'Solved_Challenge_Count', 'Solved_Tutorial_Count', 'Solved_Partial_Count', 'Solved_Other_Count']:
    if col in df.columns:
        df[col] = df[col].fillna(0)


# Features for classification
user_stats = df.groupby('Username').agg({
    'Problems_Solved': 'max',
    'World_Rank': 'min',
    'Solved_Classical_Count': 'max',
    'Solved_Challenge_Count': 'max',
    'Solved_Tutorial_Count': 'max',
    'Solved_Partial_Count': 'max',
    'Solved_Other_Count': 'max',
    'Language': pd.Series.nunique
}).rename(columns={'Language': 'Language_Variety'})

# Fill missing values after aggregation
user_stats = user_stats.fillna(0)

# Rule-based classification
user_stats['Level'] = 'beginner'
user_stats.loc[(user_stats['Problems_Solved'] >= 50) | (user_stats['World_Rank'] < 10000), 'Level'] = 'intermediate'
user_stats.loc[(user_stats['Problems_Solved'] >= 200) | (user_stats['World_Rank'] < 2000), 'Level'] = 'advanced'


# Clustering (optional, on problem mix and performance)
X = user_stats[['Problems_Solved','World_Rank','Solved_Classical_Count','Solved_Challenge_Count','Solved_Tutorial_Count','Solved_Partial_Count','Solved_Other_Count','Language_Variety']]
X = X.fillna(0)
X_scaled = (X - X.mean()) / X.std()
kmeans = KMeans(n_clusters=3, random_state=42)
user_stats['Cluster'] = kmeans.fit_predict(X_scaled)

# Save results
user_stats.to_csv('learner_levels.csv')

# Visualization
plt.figure(figsize=(8,6))
sns.countplot(x='Level', data=user_stats, order=['beginner','intermediate','advanced'])
plt.title('User Level Distribution (Rule-based)')
plt.xlabel('Level')
plt.ylabel('Number of Users')
plt.tight_layout()
plt.savefig('user_level_distribution.png')
plt.close()

print('Learner classification complete. Results saved as learner_levels.csv and user_level_distribution.png')
