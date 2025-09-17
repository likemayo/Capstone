# Capstone

## Completed Analyses

### 1. Language Choice & Problem-Solving Performance
- Acceptance rate, average execution time, and memory usage were compared across languages.
- Visualizations and summary statistics are available in the `language_analysis` folder (see PNGs and CSVs).

### 2. User Clustering by Error Patterns
- Users were clustered based on their error type distributions (e.g., wrong answer, compilation error).
- Results and cluster summaries are in the `user_clustering` folder, including cluster assignments and error profiles.

### 3. Stuck Event Detection
- Detected when users were “stuck” (3+ consecutive failed submissions before an accepted one).
- Results and visualizations of stuck users and problems are in the `stuck_prediction` folder.

### 4. Language-Specific Efficiency
- Compared execution time and memory usage across languages for problems solved in 3 or more languages.
- Outliers were excluded and ANOVA was used to test for significant differences.
- Results and visualizations (boxplots, ANOVA results) are in the `language_efficiency` folder.

## How to Reproduce Analyses
- Each analysis has its own folder with scripts and outputs.
- See the respective folders for details and to rerun or extend the analysis.