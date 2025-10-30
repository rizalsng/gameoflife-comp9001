## gameoflife-comp9001

A simple terminal implementation of Conway's Game of Life written in Python. It renders generations in the console using `x` for live cells and `-` for dead cells, with toroidal (wrap-around) edges.

### Summary
- **Grid size**: `30 x 50` (configurable via `ROWS` and `COLS` in `game-of-life.py`).
- **Initialization**: Random population based on a user-provided alive percentage (e.g., `60` -> 60% chance a cell starts alive).
- **Evolution rules**: Standard Conway rules with wrap-around neighbors.
- **Display**: Clears terminal each frame, shows generation number and alive cell count, updates ~10 FPS (`time.sleep(0.1)`).

### How it works
Key functions in `game-of-life.py`:
- `create_grid(alive_prob)`: Builds the initial grid using the provided probability of a cell being alive.
- `count_neighbors(grid, x, y)`: Counts the 8 neighbors using wrap-around indexing (toroidal board).
- `step(grid)`: Applies Game of Life rules to produce the next generation.
- `display(grid, generation)`: Clears the screen and prints the current grid with header and stats.
- `main()`: Parses the alive percentage argument, initializes the grid, and runs the simulation loop until interrupted (Ctrl+C).

### Usage
Requirements:
- Python 3.7+

Run:
```bash
python3 game-of-life.py <alive_percent>
# example
python3 game-of-life.py 60
```

Controls:
- Press `Ctrl+C` to stop the simulation.

### Configuration
You can change these constants at the top of `game-of-life.py`:
- `ROWS, COLS`: Grid dimensions (default `30, 50`).
- `time.sleep(0.1)`: Adjust frame delay for slower/faster animation.
- Characters used for rendering are in `display(...)` (`'x'` for live, `'-'` for dead).

### Game rules (Conway)
- A live cell with fewer than 2 live neighbors dies (underpopulation).
- A live cell with 2 or 3 live neighbors lives on to the next generation.
- A live cell with more than 3 live neighbors dies (overpopulation).
- A dead cell with exactly 3 live neighbors becomes a live cell (reproduction).

### Notes and caveats
- The grid uses wrap-around edges (top connects to bottom, left to right), so patterns may behave differently compared to bounded boards.
- In `main()`, the usage text says `python life.py`, but the file name is `game-of-life.py`. Use the command shown above.
- The docstring in `create_grid` mentions a `100x100` grid, but the actual default is `30x50`. This is cosmetic and does not affect behavior.

### Example output (truncated)
```
                 Conway Game of Life                 
                    Generation: 12                   
--------------------------------------------------
x--x---x----x-----x--x----x---x-----x--x----x----x-
--x-x-x-x--x-x---x-x-x--x-x-x---x-x-x--x-x--x-x-x--
... (more rows) ...
--------------------------------------------------
                 Alive cells: 723                  
```

### License
MIT (or your preferred license)

