## gameoflife-comp9001

A simple terminal implementation of Conway's Game of Life written in Python. It renders generations in the console using `x` for live cells and `-` for dead cells, with toroidal (wrap-around) edges.

### Summary
- **Grid size**: `30 x 50` (configurable via `ROWS` and `COLS` in `game-of-life.py`).
- **Initialization**: Random population based on a user-provided alive percentage (e.g., `60` -> 60% chance a cell starts alive).
- **Evolution rules**: Standard Conway rules with wrap-around neighbors.
- **Display**: Clears terminal each frame, shows world ID, generation number and alive cell count, updates ~10 FPS (`time.sleep(0.1)`).
- **Logging**: Each world (simulation run) generates a unique UUID and logs step-by-step data to JSON files in the `logs/` directory.
- **Analysis**: Analyze any previously run world using its unique ID to view statistics and trends.

### How it works
Key functions in `game-of-life.py`:
- `create_grid(alive_prob)`: Builds the initial grid using the provided probability of a cell being alive.
- `count_neighbors(grid, x, y)`: Counts the 8 neighbors using wrap-around indexing (toroidal board).
- `step(grid)`: Applies Game of Life rules to produce the next generation.
- `display(grid, generation, world_id)`: Clears the screen and prints the current grid with header, world ID, and stats.
- `init_logging(world_id, alive_percent)`: Creates a log directory and initializes a JSON log file for the world.
- `log_step(log_file, generation, alive_count, grid)`: Logs step data (generation, timestamp, alive/dead counts) to the log file.
- `analyze_world(world_id)`: Reads a world's log file and displays comprehensive statistics and analysis.
- `plot_ascii_trend(alive_counts, width, height)`: Creates an ASCII line plot visualization of the alive cell trend over generations.
- `main()`: Handles two modes: simulation (generates unique world ID, runs simulation) or analysis (analyzes existing world by ID).

### Usage
Requirements:
- Python 3.7+

#### Running a Simulation
```bash
python3 game-of-life.py <alive_percent>
# example
python3 game-of-life.py 60
```

Controls:
- Press `Ctrl+C` to stop the simulation.

#### Analyzing a World
After running a simulation, you'll receive a world ID. Use it to analyze the simulation:

```bash
python3 game-of-life.py analyze <world_id>
# example
python3 game-of-life.py analyze a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

The analyze command displays:
- World metadata (ID, grid size, initial alive percentage)
- Start/end times and duration
- Total number of generations
- Alive cell statistics (min, max, average, initial, final)
- **ASCII-based line plot visualization** showing alive cells trend over all generations
- Generation-by-generation trends (first 10 and last 10 generations)

### Logging Feature
Each simulation (called a "world") is assigned a unique UUID and logs step-by-step data to JSON files:

- **Log location**: `logs/world_<uuid>.json`
- **Log format**: JSON with world metadata and step-by-step data
- **What's logged**: 
  - World metadata: unique ID, start/end times, alive percentage, grid size
  - Per-step data: generation number, timestamp, alive cell count, dead cell count

Example log file structure:
```json
{
  "world_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
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

The log file is automatically created in the `logs/` directory (created if it doesn't exist) and updated after each generation step. When you stop a simulation (Ctrl+C), you'll be shown the world ID and the command to analyze it.

### Configuration
You can change these constants at the top of `game-of-life.py`:
- `ROWS, COLS`: Grid dimensions (default `30, 50`).
- `LOG_DIR`: Directory where log files are stored (default `"logs"`).
- `time.sleep(0.1)`: Adjust frame delay for slower/faster animation.
- Characters used for rendering are in `display(...)` (`'x'` for live, `'-'` for dead).

### Game rules (Conway)
- A live cell with fewer than 2 live neighbors dies (underpopulation).
- A live cell with 2 or 3 live neighbors lives on to the next generation.
- A live cell with more than 3 live neighbors dies (overpopulation).
- A dead cell with exactly 3 live neighbors becomes a live cell (reproduction).

### Notes and caveats
- The grid uses wrap-around edges (top connects to bottom, left to right), so patterns may behave differently compared to bounded boards.
- The docstring in `create_grid` mentions a `100x100` grid, but the actual default is `30x50`. This is cosmetic and does not affect behavior.
- Log files are written to disk after each generation step, which may have a slight performance impact on very fast systems.
- If logging fails (e.g., disk full, permission issues), the simulation continues without interruption.

### Example output (truncated)
```
                 Conway Game of Life                 
     World ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890        
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
World started with ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
Logging to: logs/world_a1b2c3d4-e5f6-7890-abcd-ef1234567890.json
```

When you stop (Ctrl+C), you'll see:
```
Game stopped.
Log file saved: logs/world_a1b2c3d4-e5f6-7890-abcd-ef1234567890.json
To analyze this world, run: python game-of-life.py analyze a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

### Example Analysis Output
```
============================================================
                        WORLD ANALYSIS                        
============================================================

World ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
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


