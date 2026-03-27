import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from Function_Scripts import Best_Contestents_Functions as BCF

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
model_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling Scaled.csv')

X = model_data.select_dtypes(include=[float, int])

# PCA ("Which combination of metrics best explains differences between contestants?")
pca_weights = BCF.get_pca_weights(data = X)

model_data["pca_score"] = (X * pca_weights).sum(axis=1)

model_data["pca_score_shift"] = BCF.get_shift_score(data = model_data, score_column_name = 'pca_score')

model_data["pca_score_rescale"] = BCF.get_scale_score(data = model_data, score_column_name = 'pca_score')

#Entropy Weighting (gives higher weight to variables with more variation.)

# normalize X (0-1)
X_norm = (X - X.min()) / (X.max() - X.min())

ent_weights = BCF.get_entropy_weights(data = X_norm)

model_data["entropy_score"] = (X_norm * ent_weights).sum(axis=1)

model_data["entropy_score_shift"] = BCF.get_shift_score(data = model_data, score_column_name = 'entropy_score')

model_data["entropy_score_rescale"] = BCF.get_scale_score(data = model_data, score_column_name = 'entropy_score')

#Final Weights and Scores
final_weights = (pca_weights + ent_weights) / 2
final_weights = final_weights / final_weights.sum()

model_data["final_score"] = (X_norm * final_weights).sum(axis=1)

model_data["final_score_shift"] = BCF.get_shift_score(data = model_data, score_column_name = 'final_score')

model_data["final_score_rescale"] = BCF.get_scale_score(data = model_data, score_column_name = 'final_score')

model_data["Contestent Rank"] = model_data["final_score"].rank(ascending=False, method="min").astype(int)

####
#Bootstrap method to get confidence (%) of the overall contestent position

n_sim = 5000
rank_results = []

weights_series = pd.Series(final_weights, index=X_norm.columns)

for i in range(n_sim):

    # sample contestants WITH their features
    sample = model_data.sample(n=len(model_data), replace=True)

    X_sample = sample[X_norm.columns]

    scores = (X_sample * weights_series).sum(axis=1)

    ranking = pd.DataFrame({"Name": sample["Name"], "Score": scores})

    ranking = ranking.sort_values("Score", ascending=False)
    ranking["Rank"] = range(1, len(ranking)+1)

    rank_results.append(ranking[["Name","Rank"]])

rank_df = pd.concat(rank_results).reset_index(drop = True)
print(rank_df.groupby("Name")["Rank"].mean())

rank_probs = rank_df.groupby(["Name","Rank"]).size().div(n_sim).unstack(fill_value=0)

model_data["Confidence"] = model_data.apply(
    lambda row: rank_probs.loc[row["Name"], row["Contestent Rank"]],
    axis=1
)

model_data["Confidence_%"] = model_data["Confidence"] * 100

expected_rank = (rank_probs * rank_probs.columns).sum(axis=1)
model_data["Expected_Rank"] = model_data["Name"].map(expected_rank)

standard_deviation_rank = rank_df.groupby("Name")["Rank"].std()
model_data['Rank Stability'] = model_data["Name"].map(standard_deviation_rank)

overall_performance = model_data[['Series', 'Name', 'pca_score',
       'pca_score_shift', 'pca_score_rescale', 'entropy_score',
       'entropy_score_shift', 'entropy_score_rescale', 'final_score',
       'final_score_shift', 'final_score_rescale', 'Contestent Rank',
       'Confidence', 'Confidence_%', 'Expected_Rank', 'Rank Stability']]

overall_performance = overall_performance.sort_values('Contestent Rank', ascending=True).reset_index(drop = True)

print(overall_performance.head())
print(overall_performance.tail())

top_5_contestents = overall_performance[overall_performance['Contestent Rank'] <= 5]['Name']
bottom_5_contestents = overall_performance[overall_performance['Contestent Rank'] >= 96]['Name']

print('Top 5: ', top_5_contestents)
print('Bottom  5: ', bottom_5_contestents)

overall_performance.to_csv(file_path + 'Overall Contestent Performance.csv', index = False, sep = ',')
