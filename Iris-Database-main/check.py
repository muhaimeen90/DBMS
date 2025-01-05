import csv
import math
import random

MIN_SAMPLE_SIZE = 4
MAX_DEPTH = 3

def read_iris_dataset(filename='IRIS.csv'):
    data = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip headers
        for row in reader:
            data.append({
                "sepal_length": float(row[0]),
                "sepal_width": float(row[1]),
                "petal_length": float(row[2]),
                "petal_width": float(row[3]),
                "species": row[4]
            })

    # print(data)
    return data

def entropy(data):
    if not data: return 0
    classes = {"Iris-setosa":0, "Iris-versicolor":0, "Iris-virginica":0}
    for d in data:
        classes[d["species"]] += 1
    ent = 0
    total = len(data)
    for c in classes.values():
        if c > 0:
            p = c / total
            ent -= p * math.log(p, 2)
    return ent

def split_dataset(data, attr, val):
    left = [d for d in data if d[attr] < val]
    right = [d for d in data if d[attr] >= val]
    return left, right

def info_gain(data, attr, val):
    if not data: return 0
    left, right = split_dataset(data, attr, val)
    p_l, p_r = len(left)/len(data), len(right)/len(data)
    return entropy(data) - (p_l*entropy(left) + p_r*entropy(right))

def best_split(attributes, domains, data):
    best = (0, None, None)
    for attr in attributes:
        for val in domains[attr]:
            gain = info_gain(data, attr, val)
            if gain >= best[0]:
                best = (gain, attr, val)
    return best

def majority_class(data):
    counts = {"Iris-setosa":0, "Iris-versicolor":0, "Iris-virginica":0}
    for d in data:
        counts[d["species"]] += 1
    return max(counts, key=counts.get)

class TreeNode:
    def __init__(self, data, attrs, domains, depth=0):
        self.data = data
        self.attrs = attrs
        self.domains = domains
        self.depth = depth
        self.is_leaf = False
        self.attr = None
        self.val = None
        self.left = None
        self.right = None
        self.prediction = None

    def build(self):
        if (self.depth < MAX_DEPTH and len(self.data) >= MIN_SAMPLE_SIZE 
            and len(set(d["species"] for d in self.data)) > 1):
            gain, attr, val = best_split(self.attrs, self.domains, self.data)
            if gain > 0:
                self.attr, self.val = attr, val
                left_data, right_data = split_dataset(self.data, attr, val)
                self.left = TreeNode(left_data, self.attrs, self.domains, self.depth+1)
                self.right = TreeNode(right_data, self.attrs, self.domains, self.depth+1)
                self.left.build()
                self.right.build()
                return
        self.is_leaf = True
        self.prediction = majority_class(self.data)

    def predict(self, sample):
        if self.is_leaf: 
            return self.prediction
        if sample[self.attr] < self.val:
            return self.left.predict(sample)
        return self.right.predict(sample)

    def merge_leaves(self):
        if not self.is_leaf:
            self.left.merge_leaves()
            self.right.merge_leaves()
            if self.left.is_leaf and self.right.is_leaf and self.left.prediction == self.right.prediction:
                self.is_leaf = True
                self.prediction = self.left.prediction

    def print(self, prefix=""):
        if self.is_leaf:
            print("\t"*self.depth + prefix + self.prediction)
        else:
            print("\t"*self.depth + prefix + f"{self.attr}<{self.val}?")
            self.left.print("[True] ")
            self.right.print("[False] ")

class ID3Tree:
    def __init__(self):
        self.root = None

    def build(self, data, attrs, domains):
        self.root = TreeNode(data, attrs, domains)
        self.root.build()

    def predict(self, sample):
        return self.root.predict(sample)

    def merge_leaves(self):
        self.root.merge_leaves()

    def print(self):
        print("------------\nDECISION TREE")
        self.root.print()
        print("------------")

if __name__ == '__main__':
    dataset = read_iris_dataset()
    if not dataset:
        print("dataset is empty!")
        exit(1)

    attr_list = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    domains = {}
    for attr in attr_list:
        domains[attr] = sorted(set(d[attr] for d in dataset))
    # print(domains)

    confusion = {c:{c2:0 for c2 in ["Iris-setosa","Iris-versicolor","Iris-virginica"]} 
                 for c in ["Iris-setosa","Iris-versicolor","Iris-virginica"]}    
    print(confusion)
    accuracies = []

    for _ in range(5):
        species_groups = {}
        for d in dataset:
            species_groups.setdefault(d["species"], []).append(d)
        test = []
        for species in species_groups:
            test += random.sample(species_groups[species], 10)
        train = [d for d in dataset if d not in test]

        tree = ID3Tree()
        tree.build(train, attr_list, domains)
        tree.merge_leaves()

        correct = 0
        for sample in test:
            pred = tree.predict(sample)
            confusion[sample["species"]][pred] += 1
            if pred == sample["species"]:
                correct += 1
        print(confusion)
        accuracies.append(correct/len(test))
        tree.print()
        print(f"Accuracy: {accuracies[-1]*100:.2f}%")

    print(f"Avg Accuracy: {sum(accuracies)/len(accuracies)*100:.2f}%")