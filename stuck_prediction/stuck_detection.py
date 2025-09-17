import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta

# Load cleaned data
df = pd.read_csv('cleaned_for_analysis.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Sort by user and date
df = df.sort_values(['Username', 'Date'])

# Define 'stuck': 3+ consecutive non-accepted submissions before an accepted one
stuck_events = []
for user, group in df.groupby('Username'):
    group = group.reset_index(drop=True)
    streak = 0
    for i, row in group.iterrows():
        if row['Result'].lower() != 'accepted':
            streak += 1
        else:
            if streak >= 3:
                stuck_events.append({
                    'Username': user,
                    'streak_length': streak,
                    'resolved_at': row['Date'],
                    'problem_code': row['Problem_Code']
                })
            streak = 0

# Convert to DataFrame
stuck_df = pd.DataFrame(stuck_events)

# Save stuck events
stuck_df.to_csv('stuck_events.csv', index=False)

# Visualize: Top users with most stuck events
top_users = stuck_df['Username'].value_counts().head(10)
plt.figure(figsize=(10,6))
sns.barplot(x=top_users.values, y=top_users.index, orient='h')
plt.title('Top 10 Users with Most Stuck Events')
plt.xlabel('Number of Stuck Events')
plt.ylabel('Username')
plt.tight_layout()
plt.savefig('top_stuck_users.png')
plt.close()

print('Stuck event detection complete. Results saved as stuck_events.csv and top_stuck_users.png')
