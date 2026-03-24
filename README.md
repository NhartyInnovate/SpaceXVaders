# 🚀 Space Invaders (Python Turtle)

A polished, arcade-style Space Invaders clone built entirely with Python's built-in `turtle` module. This project was built to practice game loops, state machines, and dynamic logic structure.

## ✨ Features
* **State Machine Logic:** Clean separation between "playing" and "game_over" states to allow for seamless restarts without breaking the main loop.
* **Destructible Environments:** Classic green bunkers that chip away piece-by-piece when hit by either player or enemy lasers.
* **Dynamic Difficulty:** Enemy movement delay scales down cleanly as levels progress, creating a smooth difficulty curve rather than jarring speed spikes.
* **Optimized Collision:** Uses list-slicing (`for enemy in enemies[:]`) to safely modify game entities during iterations without causing index errors.
* **Custom Framerate Control:** Uses `screen.tracer(0)` and `time.sleep()` for a smooth, consistent 60 FPS experience.

## 🎮 How to Play
### Prerequisites
* Python 3.x installed on your machine.
* No external libraries required (uses built-in `turtle`, `time`, and `random`).

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/NhartyInnovate/Space-Invaders-Python.git](https://github.com/NhartyInnovate/Space-Invaders-Python.git)

2. Navigate to the directory and run the game:

  ```bash
  cd Space-Invaders-Python
  python main.py

3. Controls
Left Arrow: Move Left

Right Arrow: Move Right

Spacebar: Fire Laser

R: Restart Game (Available on Game Over screen)
