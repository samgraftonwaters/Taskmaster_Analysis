import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, kruskal

import gender_age_functions as GAF

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

episode_scores = pd.read_csv(file_path + 'Episode Wins and Losses.csv', encoding="utf-8")
final_scores = pd.read_csv(file_path + 'Total Final Scores and Positions.csv', encoding="utf-8")

print(episode_scores.head())
print(final_scores.head())

gender_age_table = pd.read_csv(file_path + 'Contestent_Gender_Age.csv', encoding="utf-8")
gender_age_table['Series Number'] = gender_age_table['Series'].str.replace('S', '').astype(int)
print(gender_age_table.columns)

gender_count = GAF.gender_count_percent(gender_age_table)
gender_series = GAF.gender_count_series(gender_age_table)
GAF.gender_count_series_bar(gender_age_table = gender_age_table, series_seat = 'series', 
                            title = 'Counts of Male and Female per Series')

age_table = gender_age_table[['Name', 'Series Number', 'Age_at_First_Air']]

age_binned_table = GAF.setting_age_bins(table = age_table)

age_range_counts = GAF.age_range_metrics(table = age_binned_table)

age_series = GAF.age_group_series(table = age_binned_table)

GAF.age_series_stacked_bar(table = age_series, series_seat = 'Series', 
                           title = 'Number of Age Ranges for each Contestent per Series')

final_scores_age_gender = GAF.merge_series_age_gender(series_table = final_scores, gender_table = gender_age_table, 
                        age_table = age_binned_table)

seat_gender_table = GAF.seat_gender_metrics(datatable = final_scores_age_gender)

seat_age_table = GAF.seat_age_metrics(datatable = final_scores_age_gender)

GAF.gender_count_series_bar(gender_age_table = seat_gender_table, series_seat = 'seat', 
                            title = 'Counts of Male and Female per Seat')

GAF.age_series_stacked_bar(table = seat_age_table, series_seat = 'seat', 
                           title = 'Number of Age Ranges for each Seat')


print(final_scores_age_gender.head())

position_gender_table = final_scores_age_gender[['Position', 'Gender', 'Score']]
position_age_table = final_scores_age_gender[['Position', 'Age_Ranges', 'Score']]

position_gender_count = position_gender_table.groupby(['Gender', 'Position'], observed=True)['Score'].sum().reset_index()
position_age_count = position_age_table.groupby(['Age_Ranges', 'Position'], observed=True)['Score'].sum().reset_index()

print(position_age_count)
print(position_gender_count)

contingency_age = pd.pivot_table(position_age_count, values="Score", index="Age_Ranges", columns="Position", 
                                 aggfunc="sum", fill_value=0)

contingency_gender = pd.pivot_table(position_gender_count, values="Score", index="Gender", columns="Position", 
                                 aggfunc="sum", fill_value=0)

print(contingency_age)
print(contingency_gender)
print()

chi2_gender, p_gender, dof_gender, expected_gender = chi2_contingency(contingency_gender)

print(f"Chi-squared statistic: {chi2_gender:.3f}")
print(f"Degrees of freedom: {dof_gender}")
print(f"P-value: {p_gender:.6f}")

expected_gender = pd.DataFrame(expected_gender, index=contingency_gender.index, columns=contingency_gender.columns)

print(expected_gender)
print()

chi2_age, p_age, dof_age, expected_age = chi2_contingency(contingency_age)

print(f"Chi-squared statistic: {chi2_age:.3f}")
print(f"Degrees of freedom: {dof_age}")
print(f"P-value: {p_age:.6f}")

expected_age = pd.DataFrame(expected_age, index=contingency_age.index, columns=contingency_age.columns)

print(expected_age)

# chi-squared result does not show gender bias in Taskmaster scoring for gener.
# It shows that gender and finishing position are statistically associated, but not by scoring bias.

#Given similar performance opportunities, are contestants of different genders scored differently?
final_scores_age_gender["Score_Rank_Series"] = (
    final_scores_age_gender
    .groupby("Series")["Score"]
    .rank(method="dense", ascending=False)
)

series_max = final_scores_age_gender.groupby("Series")["Score_Rank_Series"].transform("max")

final_scores_age_gender["Normalized_Rank"] = (
    1.0
    - (final_scores_age_gender["Score_Rank_Series"] - 1).astype(float) / (series_max - 1)
)

# Handle series with only 1 contestant
final_scores_age_gender.loc[series_max == 1, "Normalized_Rank"] = 1.0

# final_scores_age_gender = final_scores_age_gender.sort_values(["Series", "Score_Rank_Series"])[
#     ["Series", "Name", "Score", "Score_Rank_Series", "Normalized_Rank"]
# ]

# Normalized rank must be per series, because each series is a separate mini-competition.

# After normalization, Normalized_Rank ranges from 0–1 in each series, making contestants from different series comparable in terms of relative performance within their series.

final_scores_age_gender["Score_z"] = final_scores_age_gender.groupby("Series")["Score"].transform(
    lambda x: (x - x.mean()) / x.std() #“Did contestants score higher or lower than their series average?”
)

print(final_scores_age_gender.head())

# age_order = ["20-29", "30-39", "40-49", "50-59", "60-69"]
# final_scores_age_gender["Age_Ranges"] = pd.Categorical(
#     final_scores_age_gender["Age_Ranges"],
#     categories=age_order,
#     ordered=True
# )

age_groups = [
    g["Normalized_Rank"].values
    for _, g in final_scores_age_gender.groupby("Age_Ranges")
    if len(g) > 1   # guard against sparse bins
]

stat_age, p_age = kruskal(*age_groups)

print(f"Kruskal–Wallis Age stat: {stat_age:.4f}; p-value: {p_age:.4f}")

gender_groups = [
    g["Normalized_Rank"].values
    for _, g in final_scores_age_gender.groupby("Gender")
]

stat_gender, p_gender = kruskal(*gender_groups)
print(f"Kruskal–Wallis Gender stat: {stat_gender:.4f}; p-value: {p_gender:.4f}")

# p ≥ 0.05 → No evidence of gender bias in final outcomes

# p < 0.05 → Gender is associated with relative finishing position

# This test now:
# ✅ Respects Taskmaster’s structure
# ✅ Removes forced rank dependence
# ✅ Directly addresses bias


sns.boxplot(
    data=final_scores_age_gender,
    x="Gender",
    y="Normalized_Rank"
)

plt.axhline(0.5, ls="--", color="gray", alpha=0.6)
plt.title("Within-Series Normalized Final Rank by Gender")
plt.show()


sns.boxplot(
    data=final_scores_age_gender,
    x="Age_Ranges",
    y="Normalized_Rank"
)

plt.axhline(0.5, ls="--", color="gray", alpha=0.6)
plt.title("Within-Series Normalized Final Rank by Age")
plt.show()


# Age results

# What the numbers mean

# Kruskal–Wallis statistic = 1.4202
# Measures the degree of difference in normalized ranks across your age bins.
# Low values → little difference between groups.

# p-value = 0.8407
# Very high (≫ 0.05), meaning the differences you see could easily arise by chance.

# 2️⃣ Interpretation

# “There is no statistically significant difference in relative finishing positions between age ranges.”

# Put another way:

# Contestants in different age groups tend to perform similarly relative to their series, based on normalized ranks.

# There’s no evidence of bias in Taskmaster scoring based on age.