import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.decomposition import PCA

# Load the image
image_path = "image.jpg"  # Replace with your image path
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

# Reshape the image into a 2D array of pixels
X = image.reshape(-1, 3)  # Shape (num_pixels, 3)

# Set the number of clusters
k = 15 # Adjust the number of dominant colors

# Randomly initialize k centroids from the dataset
np.random.seed(42)
centroids = X[np.random.choice(X.shape[0], k, replace=False)]

def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return np.sqrt(np.sum((p1 - p2) ** 2))

def assign_clusters(X, centroids):
    """Assign each data point to the nearest centroid."""
    clusters = [[] for _ in range(k)]
    
    for i, point in enumerate(X):
        distances = [euclidean_distance(point, centroid) for centroid in centroids]
        cluster_idx = np.argmin(distances)  # Get index of closest centroid
        clusters[cluster_idx].append(i)  # Store index of the data point

    return clusters

def update_centroids(X, clusters):
    """Recalculate centroids as the mean of all points in each cluster."""
    new_centroids = np.array([X[cluster].mean(axis=0) if cluster else centroids[i] for i, cluster in enumerate(clusters)])
    return new_centroids

# Run K-Means clustering
max_iters = 100
for _ in range(max_iters):
    clusters = assign_clusters(X, centroids)  # Step 1: Assign points
    new_centroids = update_centroids(X, clusters)  # Step 2: Update centroids

    if np.allclose(centroids, new_centroids):  # Stop if centroids don't change
        break
    centroids = new_centroids

# Convert cluster indices to labels for visualization
labels = np.zeros(X.shape[0])
for cluster_idx, cluster_points in enumerate(clusters):
    for point_idx in cluster_points:
        labels[point_idx] = cluster_idx

# Display the dominant colors
# plt.figure(figsize=(8, 6))
# plt.pie([len(cluster) for cluster in clusters], labels=[f'Cluster {i+1}' for i in range(k)], colors=np.array(centroids / 255), autopct='%1.1f%%')
# plt.title("Dominant Colors in Image")
# plt.show()
# Reduce dimensionality to 2D for visualization
pca = PCA(n_components=2)
X_2D = pca.fit_transform(X)

# Plot the clustered data
plt.figure(figsize=(8, 6))
for i in range(k):
    plt.scatter(X_2D[labels == i, 0], X_2D[labels == i, 1], color=np.array(centroids[i]) / 255, label=f'Cluster {i+1}')
plt.scatter(pca.transform(centroids)[:, 0], pca.transform(centroids)[:, 1], c='black', marker='X', s=200, label='Centroids')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('K-Means Clustering on Image Colors')
plt.legend()
plt.show()