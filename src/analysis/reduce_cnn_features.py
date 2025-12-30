import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Load CNN features
df = pd.read_csv("data/processed/cnn_image_features.csv")

# Remove non-feature columns if any
X = df.select_dtypes(include=["float64", "float32", "int64"])

# Standardize
X_scaled = StandardScaler().fit_transform(X)

# Reduce to 20 principal components (industry standard)
pca = PCA(n_components=20, random_state=42)
X_pca = pca.fit_transform(X_scaled)

# Save reduced features
pca_df = pd.DataFrame(X_pca, columns=[f"pc_{i}" for i in range(20)])
pca_df.to_csv("data/processed/cnn_features_pca.csv", index=False)

print("✅ PCA-reduced CNN features saved")
