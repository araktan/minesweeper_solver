## A toy project for visualizing the Breadth First Search Algorithm. 

### Usage example: 

```python
from .minesweeper_solver import animate_solution

ani = animate_solution()
ani.save('animation_0.gif', writer='PillowWriter', fps=25)
```

to get an output like this:
![minesweeper animation](animationm_0.gif)

you can also have it show directly in your jupyterlab notebook like this:

```python
from IPython.display import HTML

HTML(ani.to_jshtml())
```

### Note

If you ask the question - can this solve any minesweeper grid - the answer is **no**. Minesweeper is a rabithole. Albeit an interesting one. Inherently not all minesweeper grids are solvable. The nature of the puzzle is such that for a randomly generated grid - it may require to guess at some point. This is a very rudimentary algorithm. Humans are able to identify patterns - heuristics are not implemented here. Not yet anyway.