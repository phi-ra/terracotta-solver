# Solver for Terracotta Puzzle

**Note:** This repository is a work in progress

This repository contains the module to solve a terracotta style puzzle on a grid of $7 \times 10$. 

### Usage
Either import the `TerracottaPuzzle` class from the `main/terracotta_solver.py` module and solve it with the `TerraCottaSolver` or any other appropriate solver.

You can also use the module directly by calling

```
python main/terracotta_solver.py 123
```
Where you can replace `123` with any other seed number for the shuffling of the created list. 

Note that the implementation requires the installation of `numpy` via
```
pip install numpy
```