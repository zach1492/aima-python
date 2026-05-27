# aima-python

Assignments from COMPX216 at the University of Waikato. Built on top of the aima-python codebase which implements algorithms from *Artificial Intelligence: A Modern Approach*.

## Assignments

### Assignment 1 — Zen Puzzle Garden
Search-based solution to a rake-the-garden puzzle. A rake enters from the edge of a grid and travels in a straight line until it hits a rock or the boundary, leaving a trail behind. The goal is to rake every empty tile.

Covers:
- Reading puzzle configs from a file
- Breadth-first graph search
- A* search with a custom heuristic (counts unraked tiles)
- Beam search

---

### Assignment 2 — KNetWalk
Local search approaches to solving a network tile-rotation puzzle. Tiles need to be rotated so their connectors line up with their neighbours.

Covers:
- Fitness function based on matching connections between tiles
- Hill climbing
- Simulated annealing
- Genetic algorithm
- Local beam search
- Stochastic beam search

---

### Assignment 3 — N-Gram Language Model
Builds and samples from n-gram language models trained on a text corpus.

Covers:
- Unigram, bigram, and general n-gram model building
- Querying models for next-token predictions
- Blended probability sampling across multiple models
- Log-likelihood evaluation (ramp-up and blended)

---

### Assignment 4 — Multi-Layer Perceptron Training
Training and evaluating MLP models for binary classification on a circles dataset, using a custom automatic differentiation library (YAAE).

Covers:
- Forward pass and backpropagation training loop
- Cross-entropy loss and classification accuracy
- Comparing wider vs deeper network architectures
- Effect of training set size on model performance

---

## Dependencies

- Python 3
- numpy
- matplotlib

## Usage

Each assignment has its own file. Run with:

```bash
python3 assignment1.py
python3 assignment2.py
python3 assignment3.py
python3 assignment4.py
```
