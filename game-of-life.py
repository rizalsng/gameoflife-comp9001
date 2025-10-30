#!/usr/bin/env python3
import random
import os
import sys
import time

ROWS, COLS = 30, 50

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

def display(grid, generation):
    """Print grid with title and alive count."""
    os.system('cls' if os.name == 'nt' else 'clear')
    alive_count = sum(cell for row in grid for cell in row)
    print("Conway Game of Life".center(COLS))
    print(f"Generation: {generation}".center(COLS))
    print("-" * COLS)
    for row in grid:
        print(''.join('x' if cell else '-' for cell in row))
    print("-" * COLS)
    print(f"Alive cells: {alive_count}".center(COLS))

def main():
    if len(sys.argv) < 2:
        print("Usage: python life.py <alive_percent>")
        print("Example: python life.py 60")
        sys.exit(1)

    alive_percent = float(sys.argv[1])
    alive_prob = alive_percent / 100.0
    grid = create_grid(alive_prob)
    generation = 0

    try:
        while True:
            display(grid, generation)
            grid = step(grid)
            generation += 1
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nGame stopped.")

if __name__ == "__main__":
    main()