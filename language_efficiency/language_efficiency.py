import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway

# Load cleaned data
df = pd.read_csv('cleaned_for_analysis.csv')

# Remove outliers (top/bottom 1%) for Exec_Time_num and Memory_num
for col in ['Exec_Time_num', 'Memory_num']:
    q_low = df[col].quantile(0.01)
    q_high = df[col].quantile(0.99)
    df = df[(df[col] >= q_low) & (df[col] <= q_high)]

# For each problem with >=3 languages used, compare efficiency
problem_lang_counts = df.groupby('Problem_Code')['Language'].nunique()
problems_multi_lang = problem_lang_counts[problem_lang_counts >= 3].index

results = []
for problem in problems_multi_lang:
    sub = df[df['Problem_Code'] == problem]
    for metric in ['Exec_Time_num', 'Memory_num']:
        means = sub.groupby('Language')[metric].mean()
        if means.count() < 3:
            continue
        # ANOVA
        groups = [g[metric].dropna().values for name, g in sub.groupby('Language')]
        fval, pval = f_oneway(*groups)
        results.append({'Problem_Code': problem, 'Metric': metric, 'F': fval, 'p': pval})

anova_df = pd.DataFrame(results)
anova_df.to_csv('anova_results.csv', index=False)

# Visualization: Boxplots for a sample problem
sample_problem = problems_multi_lang[0] if len(problems_multi_lang) > 0 else None
if sample_problem:
    plt.figure(figsize=(12,6))
    sns.boxplot(x='Language', y='Exec_Time_num', data=df[df['Problem_Code']==sample_problem])
    plt.title(f'Execution Time by Language for {sample_problem}')
    plt.tight_layout()
    plt.savefig('boxplot_exec_time.png')
    plt.close()
    plt.figure(figsize=(12,6))
    sns.boxplot(x='Language', y='Memory_num', data=df[df['Problem_Code']==sample_problem])
    plt.title(f'Memory Usage by Language for {sample_problem}')
    plt.tight_layout()
    plt.savefig('boxplot_memory.png')
    plt.close()

print('Language efficiency analysis complete. Results saved as anova_results.csv, boxplot_exec_time.png, and boxplot_memory.png')
