#!/usr/bin/env python3
import random
import os
import sys
import time
import uuid
import json
from datetime import datetime

ROWS, COLS = 30, 50
LOG_DIR = "logs"

def create_grid(alive_prob):
    """Create a 100x100 grid with given alive probability."""
    return [[random.random() < alive_prob for _ in range(COLS)] for _ in range(ROWS)]

def count_neighbors(grid, x, y):
    """Count live neighbors with wrap-around edges."""
    count = 0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = (x + dx) % ROWS, (y + dy) % COLS
            if grid[nx][ny]:
                count += 1
    return count

def step(grid):
    """Generate next generation."""
    new_grid = [[False]*COLS for _ in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLS):
            n = count_neighbors(grid, i, j)
            if grid[i][j]:
                new_grid[i][j] = (n == 2 or n == 3)
            else:
                new_grid[i][j] = (n == 3)
    return new_grid

def init_logging(world_id, alive_percent):
    """Initialize log directory and log file for a new world."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    log_file = os.path.join(LOG_DIR, f"world_{world_id}.json")
    
    # Initialize log file with world metadata
    log_data = {
        "world_id": world_id,
        "start_time": datetime.now().isoformat(),
        "alive_percent": alive_percent,
        "grid_size": {"rows": ROWS, "cols": COLS},
        "steps": []
    }
    
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)
    
    return log_file

def log_step(log_file, generation, alive_count, grid):
    """Log step data to the log file."""
    try:
        # Read existing log data
        with open(log_file, 'r') as f:
            log_data = json.load(f)
        
        # Add step data
        step_data = {
            "generation": generation,
            "timestamp": datetime.now().isoformat(),
            "alive_count": alive_count,
            "dead_count": ROWS * COLS - alive_count
        }
        log_data["steps"].append(step_data)
        
        # Update end time
        log_data["end_time"] = datetime.now().isoformat()
        
        # Write back to file
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
    except Exception as e:
        # Silently handle logging errors to not interrupt the simulation
        pass

def display(grid, generation, world_id=None):
    """Print grid with title and alive count."""
    os.system('cls' if os.name == 'nt' else 'clear')
    alive_count = sum(cell for row in grid for cell in row)
    print("Conway Game of Life".center(COLS))
    if world_id:
        print(f"World ID: {world_id}".center(COLS))
    print(f"Generation: {generation}".center(COLS))
    print("-" * COLS)
    for row in grid:
        print(''.join('x' if cell else '-' for cell in row))
    print("-" * COLS)
    print(f"Alive cells: {alive_count}".center(COLS))

def plot_ascii_trend(alive_counts, width=60, height=15):
    """Create an ASCII line plot visualization of alive cell trend."""
    if not alive_counts:
        return ""
    
    # Sample data if too many points (to fit in width)
    if len(alive_counts) > width:
        step = len(alive_counts) / width
        sampled = [alive_counts[int(i * step)] for i in range(width)]
    else:
        sampled = alive_counts
    
    min_val = min(alive_counts)
    max_val = max(alive_counts)
    range_val = max_val - min_val if max_val > min_val else 1
    
    # Create a grid for plotting
    plot_width = len(sampled)
    plot_grid = [[' ' for _ in range(plot_width)] for _ in range(height + 1)]
    
    # Normalize and plot points
    normalized = []
    for i, val in enumerate(sampled):
        y_pos = int((val - min_val) / range_val * height)
        y_pos = max(0, min(height, y_pos))  # Clamp to valid range
        normalized.append(height - y_pos)  # Flip Y-axis (0 is at top)
        # Plot the point
        plot_grid[height - y_pos][i] = '*'
    
    # Draw lines between points using interpolation
    for i in range(len(normalized) - 1):
        x1, y1 = i, normalized[i]
        x2, y2 = i + 1, normalized[i + 1]
        
        # Simple line interpolation
        steps = max(abs(x2 - x1), abs(y2 - y1))
        if steps > 0:
            for s in range(steps + 1):
                t = s / steps
                x = int(x1 + t * (x2 - x1))
                y = int(y1 + t * (y2 - y1))
                
                if 0 <= y <= height and 0 <= x < plot_width:
                    if plot_grid[y][x] == ' ':
                        # Use dot for line segments
                        plot_grid[y][x] = '.'
                    elif plot_grid[y][x] == '*':
                        # Keep the data point marker
                        pass
    
    # Build chart from top to bottom
    lines = []
    lines.append("")  # Empty line before chart
    
    # Y-axis labels and plot
    for y in range(height + 1):
        y_val = min_val + ((height - y) / height) * range_val
        if y == 0:
            y_label = f"{max_val:>4}|"
        elif y == height:
            y_label = f"{min_val:>4}|"
        else:
            y_label = "    |"
        
        line = y_label + " "
        line += "".join(plot_grid[y])
        lines.append(line)
    
    # X-axis
    lines.append("    +" + "-" * plot_width)
    
    # X-axis labels (show generation numbers at key points)
    x_labels = "     "
    show_note = False
    if len(alive_counts) <= width:
        # Show generation numbers directly
        for i in range(len(normalized)):
            gen_num = i
            if gen_num < 10:
                x_labels += str(gen_num)
            elif i % 5 == 0:
                x_labels += str(gen_num % 10)
            else:
                x_labels += " "
    else:
        # Show labels at key points (start, quarters, end)
        num_labels = min(5, width)  # Show up to 5 labels
        if num_labels > 1:
            label_positions = [int(i * (width - 1) / (num_labels - 1)) for i in range(num_labels)]
            label_positions[-1] = width - 1  # Ensure last position is at end
            
            label_gen_nums = [int(i * (len(alive_counts) - 1) / (num_labels - 1)) for i in range(num_labels)]
            label_gen_nums[-1] = len(alive_counts) - 1  # Ensure last is the last generation
        else:
            label_positions = [0]
            label_gen_nums = [0]
        
        for i in range(plot_width):
            if i < len(label_positions) and i in label_positions:
                idx = label_positions.index(i)
                gen_num = label_gen_nums[idx]
                # Show generation number (truncated if needed)
                if gen_num < 10:
                    x_labels += str(gen_num)
                else:
                    # Use marker for sampled points
                    x_labels += "^"
                    show_note = True
            else:
                x_labels += " "
    
    lines.append(x_labels)
    if show_note:
        lines.append("     (^ marks generation checkpoints)")
    lines.append("     Generation →")
    
    return "\n".join(lines)

def analyze_world(world_id):
    """Analyze a world's log file and display statistics."""
    log_file = os.path.join(LOG_DIR, f"world_{world_id}.json")
    
    if not os.path.exists(log_file):
        print(f"Error: World with ID '{world_id}' not found.")
        print(f"Log file expected at: {log_file}")
        return
    
    try:
        with open(log_file, 'r') as f:
            log_data = json.load(f)
        
        # Extract data
        world_id = log_data.get("world_id", "Unknown")
        start_time = log_data.get("start_time", "Unknown")
        end_time = log_data.get("end_time", "Unknown")
        alive_percent = log_data.get("alive_percent", 0)
        grid_size = log_data.get("grid_size", {})
        steps = log_data.get("steps", [])
        
        if not steps:
            print(f"World {world_id} has no recorded steps.")
            return
        
        # Calculate statistics
        total_generations = len(steps)
        alive_counts = [step["alive_count"] for step in steps]
        dead_counts = [step["dead_count"] for step in steps]
        
        min_alive = min(alive_counts)
        max_alive = max(alive_counts)
        avg_alive = sum(alive_counts) / len(alive_counts) if alive_counts else 0
        
        # Calculate duration
        try:
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
            duration = end_dt - start_dt
            duration_str = str(duration).split('.')[0]  # Remove microseconds
        except:
            duration_str = "Unknown"
        
        # Display analysis
        print("=" * 60)
        print("WORLD ANALYSIS".center(60))
        print("=" * 60)
        print(f"\nWorld ID: {world_id}")
        print(f"Grid Size: {grid_size.get('rows', '?')} x {grid_size.get('cols', '?')}")
        print(f"Initial Alive Percentage: {alive_percent}%")
        print(f"\nStart Time: {start_time}")
        print(f"End Time: {end_time}")
        print(f"Duration: {duration_str}")
        print(f"Total Generations: {total_generations}")
        print("\n" + "-" * 60)
        print("ALIVE CELL STATISTICS".center(60))
        print("-" * 60)
        print(f"Minimum Alive: {min_alive}")
        print(f"Maximum Alive: {max_alive}")
        print(f"Average Alive: {avg_alive:.2f}")
        print(f"Initial Alive: {alive_counts[0] if alive_counts else 0}")
        print(f"Final Alive: {alive_counts[-1] if alive_counts else 0}")
        
        # ASCII Trend Visualization
        print("\n" + "-" * 60)
        print("ALIVE CELLS TREND VISUALIZATION".center(60))
        print("-" * 60)
        print("(Alive cells over generations)")
        trend_chart = plot_ascii_trend(alive_counts, width=55, height=12)
        print(trend_chart)
        
        # Show generation-by-generation trend (first 10 and last 10)
        print("\n" + "-" * 60)
        print("GENERATION TREND (First 10)".center(60))
        print("-" * 60)
        print(f"{'Generation':<12} {'Alive':<12} {'Dead':<12} {'% Alive':<12}")
        print("-" * 60)
        for step in steps[:10]:
            gen = step["generation"]
            alive = step["alive_count"]
            dead = step["dead_count"]
            total = alive + dead
            pct = (alive / total * 100) if total > 0 else 0
            print(f"{gen:<12} {alive:<12} {dead:<12} {pct:<12.2f}")
        
        if len(steps) > 10:
            print("\n... (showing last 10 generations)")
            print(f"{'Generation':<12} {'Alive':<12} {'Dead':<12} {'% Alive':<12}")
            print("-" * 60)
            for step in steps[-10:]:
                gen = step["generation"]
                alive = step["alive_count"]
                dead = step["dead_count"]
                total = alive + dead
                pct = (alive / total * 100) if total > 0 else 0
                print(f"{gen:<12} {alive:<12} {dead:<12} {pct:<12.2f}")
        
        print("\n" + "=" * 60)
        
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in log file: {log_file}")
    except Exception as e:
        print(f"Error analyzing world: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Simulation: python game-of-life.py <alive_percent>")
        print("  Analysis:   python game-of-life.py analyze <world_id>")
        print("\nExamples:")
        print("  python game-of-life.py 60")
        print("  python game-of-life.py analyze a1b2c3d4-e5f6-7890-abcd-ef1234567890")
        sys.exit(1)

    # Check if analyze command
    if sys.argv[1].lower() == "analyze":
        if len(sys.argv) < 3:
            print("Error: World ID required for analyze command.")
            print("Usage: python game-of-life.py analyze <world_id>")
            sys.exit(1)
        world_id = sys.argv[2]
        analyze_world(world_id)
        return

    # Simulation mode
    # Generate unique world ID
    world_id = str(uuid.uuid4())
    
    alive_percent = float(sys.argv[1])
    alive_prob = alive_percent / 100.0
    grid = create_grid(alive_prob)
    generation = 0
    
    # Initialize logging
    log_file = init_logging(world_id, alive_percent)
    print(f"World started with ID: {world_id}")
    print(f"Logging to: {log_file}")
    time.sleep(1)  # Brief pause to show world info

    try:
        while True:
            alive_count = sum(cell for row in grid for cell in row)
            display(grid, generation, world_id)
            log_step(log_file, generation, alive_count, grid)
            grid = step(grid)
            generation += 1
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nGame stopped.")
        print(f"Log file saved: {log_file}")
        print(f"To analyze this world, run: python game-of-life.py analyze {world_id}")

if __name__ == "__main__":
    main()