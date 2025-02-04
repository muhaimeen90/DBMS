import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import KFold
from sklearn.metrics import f1_score, fbeta_score
import math
from sklearn.metrics import precision_score, recall_score

def is_pure(dataset):
    labels = dataset[:, -1]
    return len(np.unique(labels)) == 1

def get_majority_label(dataset):
    labels = dataset[:, -1]
    unique_labels, counts = np.unique(labels, return_counts=True)
    return unique_labels[counts.argmax()]

def collect_candidate_splits(dataset):
    _, cols = dataset.shape
    candidate_splits = {}
    for col_idx in range(cols - 1):
        candidate_splits[col_idx] = []
        col_vals = dataset[:, col_idx]
        distinct_vals = np.unique(col_vals)
        for i in range(1, len(distinct_vals)):
            candidate = (distinct_vals[i] + distinct_vals[i - 1]) / 2
            candidate_splits[col_idx].append(candidate)
    return candidate_splits

def subset_data(dataset, col_idx, threshold):
    col_vals = dataset[:, col_idx]
    left_split = dataset[col_vals <= threshold]
    right_split = dataset[col_vals > threshold]
    return left_split, right_split

def compute_entropy(subset):
    labels = subset[:, -1]
    _, counts = np.unique(labels, return_counts=True)
    probabilities = counts / counts.sum()
    return -sum(probabilities * np.log2(probabilities))

def information_gain(left_split, right_split):
    total = len(left_split) + len(right_split)
    left_ratio = len(left_split) / total
    right_ratio = len(right_split) / total
    return (left_ratio * compute_entropy(left_split)
            + right_ratio * compute_entropy(right_split))

def best_split_fdr(dataset):
    
    labels = np.unique(dataset[:, -1])
    best_feature = None
    best_fdr = float('-inf')
    
    for col_idx in range(dataset.shape[1] - 1):
        overall_mean = np.mean(dataset[:, col_idx])
        between_var = 0
        within_var = 0

        for label in labels:
            class_data = dataset[dataset[:, -1] == label, col_idx]
            class_mean = np.mean(class_data)
            between_var += len(class_data) * (class_mean - overall_mean)**2
            within_var += np.sum((class_data - class_mean)**2)

        if within_var == 0:
            continue
        fdr = between_var / within_var
        if fdr > best_fdr:
            best_fdr = fdr
            best_feature = col_idx

    best_threshold = np.mean(dataset[:, best_feature])
    return best_feature, best_threshold

def best_split(dataset, candidates):
    lowest_entropy = float("inf")
    split_col = None
    split_val = None
    for col_idx in candidates:
        for val in candidates[col_idx]:
            left, right = subset_data(dataset, col_idx, val)
            curr_entropy = information_gain(left, right)
            if curr_entropy < lowest_entropy:
                lowest_entropy = curr_entropy
                split_col = col_idx
                split_val = val
    return split_col, split_val

def build_tree(df, current_depth=0, min_size=2, max_depth=5):
    global HEADERS
    if current_depth == 0:
        HEADERS = df.columns
        data = df.values
    else:
        data = df

    if is_pure(data) or (len(data) < min_size) or (current_depth == max_depth):
        return get_majority_label(data)
    current_depth += 1
    candidates = collect_candidate_splits(data)
   # col, val = best_split(data, candidates)
    col, val = best_split_fdr(data)
    left, right = subset_data(data, col, val)
    feature_name = HEADERS[col]
    tree_query = f"{feature_name} <= {val}"
    node = {tree_query: []}

    yes_branch = build_tree(left, current_depth, min_size, max_depth)
    no_branch = build_tree(right, current_depth, min_size, max_depth)
    if yes_branch == no_branch:
        node = yes_branch
    else:
        node[tree_query].append(yes_branch)
        node[tree_query].append(no_branch)
    return node

def predict_example(row, tree):
    query = list(tree.keys())[0]
    feat, _, cutoff = query.split()
    if row[feat] <= float(cutoff):
        result = tree[query][0]
    else:
        result = tree[query][1]
    if isinstance(result, dict):
        return predict_example(row, result)
    return result

def evaluate_model(df, tree):
    df = df.copy()
    df["prediction"] = df.apply(predict_example, axis=1, args=(tree,))
    return (df["prediction"] == df[df.columns[-2]]).mean()

def cross_validate_model(df, folds):
    splitter = KFold(n_splits=folds, shuffle=True)
    accuracies = []
    for train_idx, test_idx in splitter.split(df):
        training_data = df.iloc[train_idx]
        testing_data = df.iloc[test_idx]
        model = build_tree(training_data, max_depth=3)
        accuracies.append(evaluate_model(testing_data, model))
        print(accuracies[-1])
    avg = np.mean(accuracies)
    print(f"Average accuracy over {folds} folds: {avg * 100:.2f}%")

def test_prediction(sample, tree):
    query = list(tree.keys())[0]
    feat, _, cutoff = query.split()
    if sample[HEADERS.get_loc(feat)] <= float(cutoff):
        result = tree[query][0]
    else:
        result = tree[query][1]
    if isinstance(result, dict):
        return test_prediction(sample, result)
    return result

def ask_input_features():
    feats = []
    for i in range(len(HEADERS) - 1):
        val = float(input(f"Enter value for {HEADERS[i]}: "))
        feats.append(val)
    return feats
def compute_f1_f2(true_values, predicted_values):
    f1 = f1_score(true_values, predicted_values, average='macro')
    f2 = fbeta_score(true_values, predicted_values, beta=2, average='macro')
    print("F1 measure:", f1)
    print("F2 measure:", f2)

def calculate_d2h_precision_recall(data, true_labels, predicted_labels):

    precision = precision_score(true_labels, predicted_labels, average='macro')
    recall = recall_score(true_labels, predicted_labels, average='macro')

    precision_norm = precision
    recall_norm = recall

    heaven = {"precision_norm": 1, "recall_norm": 1}

    d2h = math.sqrt((heaven["precision_norm"] - precision_norm)**2 +
                    (heaven["recall_norm"] - recall_norm)**2)
    d2h_final = d2h / math.sqrt(2)

    print("d2h for precision and recall:", d2h_final)

iris_data = sns.load_dataset("iris")
k_folds = 10
cross_validate_model(iris_data, k_folds)
tree = build_tree(iris_data, max_depth=3)
iris_data["prediction"] = iris_data.apply(predict_example, axis=1, args=(tree,))
compute_f1_f2(iris_data["species"], iris_data["prediction"])
calculate_d2h_precision_recall(iris_data, iris_data["species"], iris_data["prediction"])