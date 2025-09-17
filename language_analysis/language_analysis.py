import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load cleaned data
df = pd.read_csv('cleaned_for_analysis.csv')

# Ensure output directory exists
output_dir = 'language_analysis'
os.makedirs(output_dir, exist_ok=True)

# 1. Acceptance rate by language
def acceptance_rate_by_language(df):
    total = df.groupby('Language').size()
    accepted = df[df['Result'].str.lower() == 'accepted'].groupby('Language').size()
    rate = (accepted / total).fillna(0).sort_values(ascending=False)
    return rate

# 2. Average execution time and memory usage by language
def avg_time_memory_by_language(df):
    avg_time = df.groupby('Language')['Exec_Time_num'].mean().sort_values()
    avg_mem = df.groupby('Language')['Memory_num'].mean().sort_values()
    return avg_time, avg_mem

# 3. Language usage vs. problem difficulty and accuracy
def language_vs_difficulty_accuracy(df):
    diff = df.groupby('Language')[['Implementation_difficulty', 'Concept_difficulty']].mean()
    acc = df.groupby('Language')['Accuracy_num'].mean()
    return diff, acc

def plot_bar(series, title, ylabel, filename, top_n=10):
    plt.figure(figsize=(10,6))
    sns.barplot(x=series.head(top_n).values, y=series.head(top_n).index, orient='h')
    plt.title(title)
    plt.xlabel(ylabel)
    plt.ylabel('Language')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

def plot_difficulty(diff, filename):
    plt.figure(figsize=(12,8))
    diff = diff.sort_values('Implementation_difficulty', ascending=False).head(10)
    diff[['Implementation_difficulty', 'Concept_difficulty']].plot(kind='barh')
    plt.title('Top 10 Languages by Problem Difficulty')
    plt.xlabel('Average Difficulty')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

if __name__ == '__main__':
    # Acceptance Rate
    rate = acceptance_rate_by_language(df)
    plot_bar(rate, 'Top 10 Languages by Acceptance Rate', 'Acceptance Rate', 'acceptance_rate.png')
    print('Saved plot: language_analysis/acceptance_rate.png')

    # Average Execution Time
    avg_time, avg_mem = avg_time_memory_by_language(df)
    plot_bar(avg_time, 'Top 10 Languages by Avg Execution Time (Lowest)', 'Avg Execution Time (sec)', 'avg_exec_time.png')
    print('Saved plot: language_analysis/avg_exec_time.png')

    # Average Memory Usage
    plot_bar(avg_mem, 'Top 10 Languages by Avg Memory Usage (Lowest)', 'Avg Memory Usage (MB)', 'avg_memory.png')
    print('Saved plot: language_analysis/avg_memory.png')

    # Difficulty
    diff, acc = language_vs_difficulty_accuracy(df)
    plot_difficulty(diff, 'difficulty.png')
    print('Saved plot: language_analysis/difficulty.png')

    # Accuracy
    plot_bar(acc.sort_values(ascending=False), 'Top 10 Languages by Problem Accuracy', 'Avg Accuracy (%)', 'accuracy.png')
    print('Saved plot: language_analysis/accuracy.png')
