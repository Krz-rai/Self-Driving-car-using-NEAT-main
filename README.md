# NEAT-based Car Avoidance and Coin Collection Game

This Python project uses the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to evolve a car AI that avoids obstacles (rocks) while collecting coins. The AI learns to navigate using a feed-forward neural network that controls the car's left and right movement based on the environment.

## Features
- **Obstacle Avoidance**: The car must avoid randomly placed rocks on the road.
- **Coin Collection**: The car is rewarded for collecting coins placed on the road.
- **AI Evolution**: The NEAT algorithm evolves the neural network to improve car movement over multiple generations.
- **Real-Time Visualization**: Displays the car's movements, obstacles, coins, and score in real-time using the Pygame library.

## Prerequisites

To run the project, you'll need the following dependencies:

- **Python 3.x**
- **Pygame**: For game visualization.
- **NEAT-Python**: For implementing neuroevolution.

You can install the dependencies using the following commands:

```bash
pip install pygame neat-python
```

## How It Works

1. **Neural Network Inputs**: The neural network controlling each car receives the following inputs:
    - Distance from the left and right edges of the screen.
    - Distance from the car to the rock's left and right edges.
    - Rock's Y-position and velocity.
    - Coin's X and Y positions.

2. **Movement Decision**: The neural network outputs two values:
    - Whether to move left or right.
    - Whether to prioritize moving toward a coin.

3. **Rewards and Penalties**:
    - The car is rewarded for collecting coins.
    - The car is penalized for collisions with rocks or for missing coins.

4. **Fitness Evaluation**: Each car's neural network is evaluated based on its performance in avoiding rocks and collecting coins. The fitness score determines which networks survive and evolve.

## Code Breakdown

### 1. `Car` Class
Defines the car object, including its movement, drawing, and collision detection with other objects.

### 2. `Rock` and `BigRock` Classes
Defines the rocks (obstacles) that the car must avoid. A `BigRock` consists of two `Rock` objects with a gap between them.

### 3. `Coin` Class
Defines the coin object, which moves down the screen and rewards the car for collecting it.

### 4. `main(genomes, config)` Function
The core loop where the NEAT algorithm runs. Each car is controlled by a neural network and must navigate through the game environment. Cars receive rewards or penalties based on their performance.

### 5. `run(config_path)` Function
Initializes the NEAT algorithm and runs the evolutionary process for 20 generations.

## Running the Game

1. **Clone the repository**:

```bash
git clone https://github.com/kr3287/neat-car-game.git
cd Self-Driving-car-using-NEAT
```

2. **Run the Game**:

```bash
python self-drive.py
```

The `self-drive.py` file will start the simulation, and you'll see the cars trying to avoid rocks and collect coins.

## NEAT Configuration

The NEAT algorithm is configured using the `config-feedforward.txt` file. You can adjust parameters like population size, mutation rates, and fitness thresholds to tweak the evolution process.

## Example Output

After running the simulation, you should see cars navigating through rocks and collecting coins. Over time, the cars should improve their performance as the neural networks evolve.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
