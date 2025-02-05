import numpy as np

# Function to calculate the mean and variance for each class (skin and non-skin)
def mean_variance(X, y):
    mean_var = {}
    for label in np.unique(y):
        class_data = X[y == label]
        mean_var[label] = {
            'mean': np.mean(class_data, axis=0),
            'var': np.var(class_data, axis=0)
        }
    return mean_var

# Function to calculate prior probabilities
def prior_probs(y):
    class_probs = {}
    total_samples = len(y)
    for label in np.unique(y):
        class_probs[label] = np.sum(y == label) / total_samples
    return class_probs

# Function to calculate Gaussian likelihood
def gaussian_likelihood(x, mean, var):
    exponent = np.exp(-0.5 * ((x - mean) ** 2) / var)
    return (1 / np.sqrt(2 * np.pi * var)) * exponent

# Naïve Bayes prediction
def predict(X, mean_var, priors):
    predictions = []
    for x in X:
        class_probs = {}
        for label in mean_var.keys():
            mean = mean_var[label]['mean']
            var = mean_var[label]['var']
            likelihood = np.prod(gaussian_likelihood(x, mean, var))
            class_probs[label] = np.log(priors[label]) + np.sum(np.log(likelihood))
        predicted_class = max(class_probs, key=class_probs.get)
        predictions.append(predicted_class)
    return predictions
