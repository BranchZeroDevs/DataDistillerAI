"""Sample data for testing and demonstration."""

# Sample Document 1: ML Overview
SAMPLE_DOC_1 = """
Machine Learning Fundamentals

Machine learning is a subset of artificial intelligence that enables systems to learn and improve 
from experience without being explicitly programmed. It uses algorithms and statistical models 
to identify patterns in data.

Key Concepts:

1. Supervised Learning: The model learns from labeled training data. Common algorithms include 
linear regression, logistic regression, and decision trees.

2. Unsupervised Learning: The model discovers patterns in unlabeled data. Clustering and 
dimensionality reduction are common unsupervised tasks.

3. Reinforcement Learning: The model learns through interaction with an environment, receiving 
rewards or penalties for actions.

Applications:

- Computer Vision: Image classification, object detection, facial recognition
- Natural Language Processing: Sentiment analysis, machine translation, text classification
- Recommendation Systems: Netflix recommendations, Amazon product suggestions
- Predictive Analytics: Stock price forecasting, demand prediction

Workflow:

1. Data Collection: Gather relevant data
2. Data Preprocessing: Clean and normalize data
3. Feature Engineering: Create meaningful features
4. Model Selection: Choose appropriate algorithm
5. Training: Fit model to training data
6. Evaluation: Assess performance on test data
7. Hyperparameter Tuning: Optimize model parameters
8. Deployment: Put model into production
"""

# Sample Document 2: Deep Learning
SAMPLE_DOC_2 = """
Deep Learning and Neural Networks

Deep learning is a specialized branch of machine learning that uses neural networks with 
multiple layers (hence "deep") to model complex patterns in large amounts of data.

Neural Network Architecture:

- Input Layer: Receives input features
- Hidden Layers: Perform transformations and feature extraction
- Output Layer: Produces final predictions
- Weights and Biases: Learnable parameters adjusted during training

Common Architectures:

1. Convolutional Neural Networks (CNN): Specialized for image processing, uses convolutional layers 
to automatically detect spatial features.

2. Recurrent Neural Networks (RNN): Handles sequential data like time series and text, maintains 
hidden state to capture temporal dependencies.

3. Transformer Networks: Based on self-attention mechanism, enables parallel processing of sequences, 
used in modern NLP (BERT, GPT).

Training Process:

1. Forward Pass: Input flows through network producing output
2. Loss Calculation: Compare output to ground truth
3. Backward Pass: Compute gradients using backpropagation
4. Parameter Update: Adjust weights using gradient descent optimizer

Popular Frameworks:

- TensorFlow: Google's framework with Keras high-level API
- PyTorch: Facebook's framework known for research flexibility
- JAX: Numerical computing library with automatic differentiation

Challenges:

- Requires large amounts of labeled data
- Computationally expensive (GPUs/TPUs needed)
- Difficult to interpret decisions (black box)
- Prone to overfitting on small datasets
"""

if __name__ == "__main__":
    # Save sample documents
    from pathlib import Path
    
    data_dir = Path(__file__).parent / "data" / "documents"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    with open(data_dir / "ml_fundamentals.txt", "w") as f:
        f.write(SAMPLE_DOC_1)
    
    with open(data_dir / "deep_learning.txt", "w") as f:
        f.write(SAMPLE_DOC_2)
    
    print("Sample documents created successfully!")
