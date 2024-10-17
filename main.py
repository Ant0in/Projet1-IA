import argparse
from lle import World
from src.problem import SearchProblem, GemProblem, ExitProblem, CornerProblem
from src.search import astar, bfs, dfs, Solution, visualize_solution


PROBLEMS: dict = {
    'gem': GemProblem,
    'exit': ExitProblem,
    'corner': CornerProblem
}

ALGORITHMS: dict = {
    'astar': astar,
    'bfs': bfs,
    'dfs': dfs
}

def main():
    
    parser = argparse.ArgumentParser(description='Solve a problem in a world using different algorithms.')
    parser.add_argument('world_file', type=str, help='Path to the text file containing the world representation.')
    parser.add_argument('--problem', required=True, choices=PROBLEMS.keys(), help='Type of problem to solve (gem, exit, corner).')
    parser.add_argument('--algo', required=True, choices=ALGORITHMS.keys(), help='Algorithm to use (astar, bfs, dfs).')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode for debugging.')
    args = parser.parse_args()

    with open(args.world_file, 'r') as f:
        str_world = f.read()
    
    world: World = World(str_world)
    problem_class: SearchProblem = PROBLEMS[args.problem]
    problem: object = problem_class(world=world)
    algorithm: callable = ALGORITHMS[args.algo]
    sol: Solution = algorithm(problem=problem, verbose=args.verbose)
    visualize_solution(w=world, solution=sol, name='Solution')



if __name__ == '__main__':
    main()

