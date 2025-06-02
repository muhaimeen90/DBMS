# DBMS Course Repository

A comprehensive collection of database management systems concepts and machine learning algorithms implemented during an academic course. This repository showcases the progression from fundamental database concepts to advanced machine learning techniques.

## 📚 Course Overview

This repository contains practical implementations and assignments covering:
- **Database Management Systems** - Core concepts and recovery algorithms
- **Data Mining & Machine Learning** - Various ML algorithms and data analysis techniques
- **Performance Analysis** - Multi-core partitioning and optimization

## 🗂️ Repository Structure

### Database Management Systems

#### Lab 1: Checkpoint Failure Recovery
- **File**: `Lab1(Checkpoint failure)/lab1.py`
- **Concept**: Database recovery using checkpoint and transaction logs
- **Implementation**: Undo/Redo operations for transaction recovery
- **Input**: Transaction log file with START, COMMIT, and CHECKPOINT operations

### Data Mining & Machine Learning Algorithms

#### Lab 3: Apriori Algorithm
- **Files**: `lab3(apriory)/apriori.py`, `lab3(apriory)/apriori.txt`
- **Concept**: Frequent itemset mining for market basket analysis
- **Implementation**: Generates frequent itemsets from transaction data
- **Dataset**: Transaction database with items I1-I5

#### Lab 4: Multi-core Partitioning
- **Files**: `lab04(multi core partition)/`
- **Concept**: Data partitioning strategies for parallel processing
- **Implementation**: Distributes data across multiple cores for optimization
- **Data**: Large datasets (array2.txt, array3.txt) for performance testing

#### Lab 6: Decision Tree Classification
- **Files**: `lab06(decisiontree)/decisiontree.py`, `lab06(decisiontree)/check.py`
- **Concept**: ID3 algorithm and decision tree construction
- **Implementation**: 
  - Entropy calculation and information gain
  - Tree building with pruning
  - Cross-validation and performance metrics (F1, F2 scores)
- **Dataset**: IRIS dataset for classification

#### Naive Bayes Classification
- **Files**: `naiveBayes/nb.py`, `naiveBayes/test.py`
- **Concept**: Probabilistic classification using Gaussian Naive Bayes
- **Implementation**: 
  - Skin/Non-skin pixel classification
  - Image processing and classification
  - Mean and variance calculation for feature distributions
- **Application**: Image segmentation for skin detection

#### K-Means Clustering
- **Files**: `kmeans/kmeans.py`
- **Concept**: Unsupervised clustering algorithm
- **Implementation**: 
  - Image color quantization
  - Centroid initialization and updates
  - Euclidean distance calculations
- **Application**: Dominant color extraction from images

## 🛠️ Technologies Used

- **Python**: Primary programming language
- **NumPy**: Numerical computations
- **Pandas**: Data manipulation and analysis
- **OpenCV**: Image processing
- **Scikit-learn**: Machine learning utilities
- **Matplotlib**: Data visualization

## 🚀 Getting Started

### Prerequisites
```bash
pip install numpy pandas opencv-python scikit-learn matplotlib pillow
```

### Running the Examples

1. **Database Recovery (Lab 1)**:
   ```bash
   cd "Lab1(Checkpoint failure)"
   python lab1.py
   ```

2. **Apriori Algorithm (Lab 3)**:
   ```bash
   cd "lab3(apriory)"
   python apriori.py
   ```

3. **Decision Tree (Lab 6)**:
   ```bash
   cd "lab06(decisiontree)"
   python decisiontree.py
   ```

4. **Naive Bayes Classification**:
   ```bash
   cd naiveBayes
   python test.py
   ```

5. **K-Means Clustering**:
   ```bash
   cd kmeans
   python kmeans.py
   ```

## 📊 Key Features

### Database Concepts
- **Transaction Recovery**: Implements ARIES-style recovery with undo/redo operations
- **Checkpoint Management**: Handles checkpoint-based recovery scenarios

### Machine Learning Implementations
- **Classification**: Decision Trees and Naive Bayes for supervised learning
- **Clustering**: K-Means for unsupervised pattern discovery
- **Association Mining**: Apriori algorithm for frequent pattern mining
- **Performance Metrics**: Comprehensive evaluation using F1, F2, precision, and recall

### Data Processing
- **Image Processing**: Skin detection and color quantization
- **Cross-validation**: K-fold validation for model evaluation
- **Large Dataset Handling**: Multi-core partitioning for scalability

## 📈 Learning Outcomes

This repository demonstrates proficiency in:
- Database recovery mechanisms and transaction management
- Fundamental machine learning algorithms from scratch
- Data preprocessing and feature engineering
- Performance evaluation and model validation
- Multi-core programming and optimization techniques

## 📝 Academic Context

Developed as part of a comprehensive DBMS course that evolved to include machine learning concepts, showcasing the intersection between database systems and data science methodologies.

---

*This repository serves as a practical demonstration of database management systems and machine learning concepts learned throughout the academic course.*
