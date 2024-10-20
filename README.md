# Search Problem - 2024

## Description

This project involves implementing the **DFS**, **BFS**, and **A\*** search algorithms to navigate an agent through a map, where it must solve a **problem** (such as *collecting gems*, *finding an exit*, or *visiting specific points*). More info in `./pdf/consignes.pdf`.

<p align="center">
  <img src="./pdf/map.png" alt="search problem" width="400"/>
  <br/>
  <strong>Instance of the Search Problem, where agent must collect gems and find the exit.</strong>
</p>

## Features

- **Algorithmic graph search approach**: Transforms the problem into a graph, with nodes representing "world states", and navigates through them using A*, BFS, and DFS.
- **Search problems**: Implements various problems, including one where finding every gem is required to exit, another where the goal is simply to find the exit, and one where you must visit every corner before exiting.
- **Visualization**: A visual demonstration of the search algorithms, where the agent moves according to the solution found by the algorithm.

## Usage

Make sure you have `Python >= 3.12` installed.


### Running the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/Ant0in/Projet1-IA.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Projet1-IA/
   ```

3. Install dependencies:
   
   ```bash
   pip install -r "requirements.txt"
   ```

4. Run the project on a grid `map1.txt`:

   ```bash
   python "./main.py" "./tests/map1.txt" --problem "gem" --algo "bfs" --verbose
   ```

### Running Tests

To run the tests using Pytest (verbose):

   ```bash
   pytest .\tests\ -vvv
   ```

## License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute this software.

## Acknowledgements

This project was developed for the Artificial Intelligence course `INFO-F311`. Special thanks to `Tom Lenaerts & Yannick Molinghen (ULB)` for their guidance and support.

