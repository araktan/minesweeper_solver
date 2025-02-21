## A toy project primarily for visualizing the Breadth First Search Algorithm. 

### Usage example: 

```python
from minesweeper_solver import animate_solution

ani = animate_solution()
ani.save('animation_0.gif', writer='PillowWriter', fps=25)
```

to get an output like this:

![](https://github.com/araktan/minesweeper_solver/blob/main/animation_0.gif)

you can also have it show directly in your jupyterlab notebook like this:

```python
from IPython.display import HTML

HTML(ani.to_jshtml())
```

### Note

If you ask the question - can this solve any minesweeper grid - the answer is **no**. Inherently not all minesweeper grids are solvable. The nature of the puzzle is such that solving a randomly generated grid may require guessing. 

