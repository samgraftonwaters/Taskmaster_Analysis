import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
model_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling Scaled.csv')

X = model_data.select_dtypes(include=[float, int])
print(len(X.columns))

# PCA ("Which combination of metrics best explains differences between contestants?")

def get_pca_weights(data):
    pca = PCA(n_components=1)
    pca.fit(data)

    weights = pd.Series(pca.components_[0], index=data.columns)

    # normalize weights
    weights = weights / weights.abs().sum()

    return(weights)

def get_shift_score(data, score_column_name:str):
    shift_score = data[score_column_name] - data[score_column_name].min()
    return(shift_score)

def get_scale_score(data, score_column_name:str):
    scale_score = (
        (data[score_column_name] - data[score_column_name].min()) /
        (data[score_column_name].max() - data[score_column_name].min())
    ) * 100
    return(scale_score)

pca_weights = get_pca_weights(data = X)
# composite score
model_data["pca_score"] = X @ pca_weights

model_data["pca_score_shift"] = get_shift_score(data = model_data, score_column_name = 'pca_score')

model_data["pca_score_rescale"] = get_scale_score(data = model_data, score_column_name = 'pca_score')


print(pca_weights)
print(model_data["pca_score"])
print(model_data["pca_score_shift"])
print(model_data["pca_score_rescale"])



#Entropy Weighting (gives higher weight to variables with more variation.)

# normalize X (0-1)
X_norm = (X - X.min()) / (X.max() - X.min())

def get_entropy_weights(data):

    # convert to probabilities
    P = X_norm / X_norm.sum()

    # entropy
    k = 1 / np.log(len(model_data))
    entropy = -k * (P * np.log(P + 1e-9)).sum()

    # diversification
    d = 1 - entropy

    # weights
    weights = d / d.sum()
    
    return(weights)


ent_weights = get_entropy_weights(data = X_norm)

model_data["entropy_score"] = (X_norm * ent_weights).sum(axis=1)

model_data["entropy_score_shift"] = get_shift_score(data = model_data, score_column_name = 'entropy_score')

model_data["entropy_score_rescale"] = get_scale_score(data = model_data, score_column_name = 'entropy_score')

print(model_data["entropy_score"])
print(model_data["entropy_score_shift"])
print(model_data["entropy_score_rescale"])

# ####

final_weights = (pca_weights + ent_weights) / 2
final_weights = final_weights / final_weights.sum()
model_data["final_score"] = X_norm @ final_weights

model_data["final_score_shift"] = get_shift_score(data = model_data, score_column_name = 'final_score')

model_data["final_score_rescale"] = get_scale_score(data = model_data, score_column_name = 'final_score')

model_data["Contestent Rank"] = model_data["final_score"].rank(ascending=False, method="min").astype(int)
print(model_data.head())

# ###

n_sim = 5000
rank_results = []

weights_series = pd.Series(final_weights, index=X_norm.columns)

for i in range(n_sim):

    # sample contestants WITH their features
    sample = model_data.sample(n=len(model_data), replace=True)

    X_sample = sample[X_norm.columns]

    scores = X_sample @ weights_series

    ranking = pd.DataFrame({
        "Name": sample["Name"],
        "Score": scores
    })

    ranking = ranking.sort_values("Score", ascending=False)
    ranking["Rank"] = range(1, len(ranking)+1)

    rank_results.append(ranking[["Name","Rank"]])

rank_df = pd.concat(rank_results).reset_index(drop = True)
print(rank_df.groupby("Name")["Rank"].mean())

rank_probs = (
    rank_df
    .groupby(["Name","Rank"])
    .size()
    .div(n_sim)
    .unstack(fill_value=0)
)
print(rank_df)
print(rank_probs)

model_data["Confidence"] = model_data.apply(
    lambda row: rank_probs.loc[row["Name"], row["Contestent Rank"]],
    axis=1
)

model_data["Confidence_%"] = model_data["Confidence"] * 100

expected_rank = (rank_probs * rank_probs.columns).sum(axis=1)
model_data["Expected_Rank"] = model_data["Name"].map(expected_rank)

standard_deviation_rank = rank_df.groupby("Name")["Rank"].std()
model_data['Rank Stability'] = model_data["Name"].map(standard_deviation_rank)

print(expected_rank)

print(model_data.head(30))



# # X_scaled = StandardScaler().fit_transform(X)
# # pca = PCA(n_components=2)
# # X_pca = pca.fit_transform(X_scaled)

# # model_data["PCA1"] = X_pca[:,0]
# # model_data["PCA2"] = X_pca[:,1]