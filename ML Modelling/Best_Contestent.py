import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
model_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling Scaled.csv')

X = model_data.select_dtypes(include=[float, int])
print(len(X.columns))

# PCA ("Which combination of metrics best explains differences between contestants?")
pca = PCA(n_components=1)
pca.fit(X)

weights = pd.Series(pca.components_[0], index=X.columns)

# normalize weights
pca_weights = weights / weights.abs().sum()

# composite score
model_data["pca_score"] = X @ pca_weights

model_data["pca_score_shift"] = model_data["pca_score"] - model_data["pca_score"].min()

model_data["pca_score_rescale"] = (
    (model_data["pca_score"] - model_data["pca_score"].min()) /
    (model_data["pca_score"].max() - model_data["pca_score"].min())
) * 100

print(pca_weights)
print(model_data["pca_score"])
print(model_data["pca_score_shift"])
print(model_data["pca_score_rescale"])



#Entropy Weighting (gives higher weight to variables with more variation.)

# normalize X (0-1)
X_norm = (X - X.min()) / (X.max() - X.min())

# convert to probabilities
P = X_norm / X_norm.sum()

# entropy
k = 1 / np.log(len(model_data))
entropy = -k * (P * np.log(P + 1e-9)).sum()

# diversification
d = 1 - entropy

# weights
weights = d / d.sum()

ent_weights = pd.Series(weights, index=X.columns)

# composite score
model_data["entropy_score"] = (X_norm * ent_weights).sum(axis=1)

print(ent_weights)

print(model_data["entropy_score"])

final_weights = (pca_weights + ent_weights) / 2
final_weights = final_weights / final_weights.sum()
model_data["final_score"] = X_norm @ final_weights
print(model_data["final_score"])

print(model_data.head())

###

n_sim = 5000
contestants = model_data["Name"]

rank_results = []

for i in range(n_sim):

    # resample rows (tasks) with replacement
    sample_idx = np.random.choice(X_norm.index, size=len(X_norm), replace=True)
    X_sample = X_norm.loc[sample_idx].reset_index(drop=True)

    # recompute scores
    scores = X_sample @ final_weights

    # aggregate per contestant
    score_df = pd.DataFrame({
        "Name": model_data["Name"],
        "Score": scores
    })

    ranking = score_df.sort_values("Score", ascending=False)
    ranking["Rank"] = range(1, len(ranking)+1)

    rank_results.append(ranking[["Name","Rank"]])

rank_df = pd.concat(rank_results)

rank_probs = (
    rank_df
    .groupby(["Name","Rank"])
    .size()
    .div(n_sim)
    .unstack(fill_value=0)
)
print(rank_df)
print(rank_probs)

expected_rank = (rank_probs * rank_probs.columns).sum(axis=1)
print(expected_rank)


# X_scaled = StandardScaler().fit_transform(X)
# pca = PCA(n_components=2)
# X_pca = pca.fit_transform(X_scaled)

# model_data["PCA1"] = X_pca[:,0]
# model_data["PCA2"] = X_pca[:,1]