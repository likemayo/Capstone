import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load stuck events
df = pd.read_csv('stuck_events.csv')

# Summary: Most common problems where users get stuck
problem_counts = df['problem_code'].value_counts().head(10)
print('Top 10 problems where users get stuck:')
print(problem_counts)

# Visualization
plt.figure(figsize=(10,6))
sns.barplot(x=problem_counts.values, y=problem_counts.index, orient='h')
plt.title('Top 10 Problems Where Users Get Stuck')
plt.xlabel('Number of Stuck Events')
plt.ylabel('Problem Code')
plt.tight_layout()
plt.savefig('top_stuck_problems.png')
plt.close()
print('Saved plot: top_stuck_problems.png')
