## gameoflife-comp9001

A simple terminal implementation of Conway's Game of Life written in Python. It renders generations in the console using `x` for live cells and `-` for dead cells, with toroidal (wrap-around) edges.

### Conway's Game of Life
The Game of Life, also known as Conway's Game of Life or simply Life, is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves. 

### Rules (Conway's Game of Life)
The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead (or populated and unpopulated, respectively). Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. 

<table>
  <tr>
    <td width="50%" valign="top">
      <img src="static/gameofliferules11.jpg" alt="Conway's Game of Life Rules" width="320" />
    </td>
    <td width="50%" valign="top">
      <ul>
        <li>A live cell with fewer than 2 live neighbors dies (underpopulation).</li>
        <li>A live cell with 2 or 3 live neighbors lives on to the next generation.</li>
        <li>A live cell with more than 3 live neighbors dies (overpopulation).</li>
        <li>A dead cell with exactly 3 live neighbors becomes a live cell (reproduction).</li>
      </ul>
    </td>
  </tr>
  </table>

### Summary
- **Grid size**: configurable via `ROWS` and `COLS` in `game-of-life.py`).
- **Initialization**: Random population based on a user-provided alive percentage (e.g., `60` -> 60% chance a cell starts alive).
- **Evolution rules**: Standard Conway rules with wrap-around neighbors.
- **Display**: Clears terminal each frame, shows world name, generation number and alive cell count, updates ~10 FPS (`time.sleep(0.1)`).
- **Logging**: Each world (simulation run) logs step-by-step data to a JSON file in the `logs/` directory, named by the world (e.g., `world_Alice.json`). If a name already exists, a numeric suffix is added (e.g., `world_Alice_2.json`).
- **Analysis**: Analyze any previously run world using its name to view statistics and trends.


### Usage
Requirements:
- Python 3.7+

#### Running a Simulation
```bash
python3 game-of-life.py <world_name> <alive_percent>
# example
python3 game-of-life.py Alice 60
```

Controls:
- Press `Ctrl+C` to stop the simulation.

#### Analyzing a World
Analyze a simulation by its world name (the filename without `world_` and `.json`):

```bash
python3 game-of-life.py analyze <world_name>
# example
python3 game-of-life.py analyze Alice
```

The analyze command displays:
- World metadata (name, grid size, initial alive percentage)
- Start/end times and duration
- Total number of generations
- Alive cell statistics (min, max, average, initial, final)
- **ASCII-based line plot visualization** showing alive cells trend over all generations
- Generation-by-generation trends (first 10 and last 10 generations)

### How it works
 Key functions in `game-of-life.py`:
- `create_grid(alive_prob)`: Builds the initial grid using the provided probability of a cell being alive.
- `count_neighbors(grid, x, y)`: Counts the 8 neighbors using wrap-around indexing (toroidal board).
- `step(grid)`: Applies Game of Life rules to produce the next generation.
- `display(grid, generation, world_name)`: Clears the screen and prints the current grid with header (world name) and stats.
- `init_logging(alive_percent, world_name)`: Creates a log directory and initializes a JSON log file named after the world.
- `log_step(log_file, generation, alive_count, grid)`: Logs step data (generation, timestamp, alive/dead counts) to the log file.
- `analyze_world(world_name)`: Reads a world's log file by name and displays comprehensive statistics and analysis.
- `plot_ascii_trend(alive_counts, width, height)`: Creates an ASCII line plot visualization of the alive cell trend over generations.
- `main()`: Handles two modes: simulation (runs a world with a provided name) or analysis (analyzes existing world by name).



### Logging Feature
Each simulation (called a "world") logs step-by-step data to JSON:

- **Log location**: `logs/world_<name>.json` (e.g., `logs/world_Alice.json`). If a log with the same name exists, a numeric suffix is added (e.g., `logs/world_Alice_2.json`).
- **Log format**: JSON with world metadata and step-by-step data
- **What's logged**: 
  - World metadata: world name, start/end times, alive percentage, grid size
  - Per-step data: generation number, timestamp, alive cell count, dead cell count

Example log file structure:
```json
{
  "world_name": "Alice",
  "start_time": "2024-01-15T10:30:45.123456",
  "alive_percent": 60.0,
  "grid_size": {"rows": 30, "cols": 50},
  "steps": [
    {
      "generation": 0,
      "timestamp": "2024-01-15T10:30:45.234567",
      "alive_count": 900,
      "dead_count": 600
    },
    ...
  ],
  "end_time": "2024-01-15T10:35:22.789012"
}
```

The log file is automatically created in the `logs/` directory (created if it doesn't exist) and updated after each generation step. When you stop a simulation (Ctrl+C), you'll be shown the chosen world name and the command to analyze it.

### Configuration
You can change these constants at the top of `game-of-life.py`:
- `ROWS, COLS`: Grid dimensions (default `30, 50`).
- `LOG_DIR`: Directory where log files are stored (default `"logs"`).
- `time.sleep(0.1)`: Adjust frame delay for slower/faster animation.
- Characters used for rendering are in `display(...)` (`'x'` for live, `'-'` for dead).


### Example output (truncated)
```
                 Conway Game of Life                 
                   World: Alice                    
                    Generation: 12                   
--------------------------------------------------
x--x---x----x-----x--x----x---x-----x--x----x----x-
--x-x-x-x--x-x---x-x-x--x-x-x---x-x-x--x-x--x-x-x--
... (more rows) ...
--------------------------------------------------
                 Alive cells: 723                  
```

On start, you'll see:
```
World started: Alice
Logging to: logs/world_Alice.json
```

When you stop (Ctrl+C), you'll see:
```
Game stopped.
Log file saved: logs/world_Alice.json
To analyze this world, run: python game-of-life.py analyze Alice
```

### Example Analysis Output
```
============================================================
                        WORLD ANALYSIS                        
============================================================

World: Alice
Grid Size: 30 x 50
Initial Alive Percentage: 60.0%

Start Time: 2024-01-15T10:30:45.123456
End Time: 2024-01-15T10:35:22.789012
Duration: 0:04:37
Total Generations: 2756

------------------------------------------------------------
              ALIVE CELL STATISTICS              
------------------------------------------------------------
Minimum Alive: 423
Maximum Alive: 987
Average Alive: 723.45
Initial Alive: 900
Final Alive: 645

------------------------------------------------------------
          ALIVE CELLS TREND VISUALIZATION          
------------------------------------------------------------
(Alive cells over generations)

 987|                                               
    |           *                                    
    |         . .                                   
    |       .   .                                   
    |     .     .                                   
    |   .       .                                   
    | .         .                                   
 423|*...............*.*.*.................*.*.*.*.*
    +------------------------------------------------
     Generation →

------------------------------------------------------------
           GENERATION TREND (First 10)           
------------------------------------------------------------
Generation   Alive        Dead         % Alive     
------------------------------------------------------------
0            900          600          60.00       
1            923          577          61.53       
...
```


