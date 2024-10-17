

from dataclasses import dataclass
from typing import Generic, Optional, TypeVar
from lle import Action, WorldState, World
from src.priority_queue import PriorityQueue
from src.problem import SearchProblem, GemProblem, ExitProblem, CornerProblem
import cv2
import time
import matplotlib.pyplot as plt
import numpy as np



S = TypeVar("S", bound=WorldState)



@dataclass
class Solution(Generic[S]):
    
    actions: list[Action]
    states: list[S]

    @property
    def n_steps(self) -> int:
        # Returns how many steps are required to reach the solution.
        return len(self.actions)

    @staticmethod
    def from_node(node: "SearchNode") -> "Solution[S]":
        
        # Find the path from a Node state to the initial state, and reverse the route to
        # give the solution up to a certain node 'node'.

        actions: list[Action] = list()
        states: list[WorldState] = list()

        while node.parent is not None:

            actions.append(node.prev_action)
            states.append(node.state)
            node = node.parent

        actions.reverse()
        return Solution(actions, states)


@dataclass
class SearchNode:

    state: WorldState
    parent: Optional["SearchNode"]
    prev_action: Optional[Action]
    cost: float = 0.0

    def __hash__(self) -> int:
        return hash((self.state, self.cost))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SearchNode):
            return NotImplemented
        return self.state == other.state and self.cost == other.cost



def visualize_solution(w: World, solution: Solution, name: str) -> None:
    
    # Little method used to visualize solutions using openCV2
    if not isinstance(solution, Solution): print('No solution found!'); return

    def show_img(img, step: int, action: Action) -> None:
        cv2.imshow("Visualisation", img)
        cv2.waitKey(1)
        input(f'[{name} : Step {step}] Action : {action} ')

    show_img(img=w.get_image(), step=0, action='Initial state')
    for step, a in enumerate(solution.actions):
        w.step(action=a)
        show_img(img=w.get_image(), step=step+1, action=a)
    print(f'[G] Goal reached in {len(solution.actions)} steps for {name}.')

def dfs(problem: SearchProblem, verbose: bool = False) -> Optional[Solution]:
    
    # DFS Method for algorithmic search in a graph.
    stack: list[SearchNode] = [SearchNode(state=problem.initial_state, parent=None, prev_action=None)]
    visited: set = set()

    # while we have element to explore / we did not find any solution ;
    while stack:

        current: SearchNode = stack.pop()
        if current not in visited:            
            visited.add(current)
    
            if problem.is_goal_state(state=current.state):
                if verbose: print(f'[v] Node visited : {len(visited)}')
                return Solution.from_node(node=current)

            # We get every sucessors to current and add them to the stack
            successors: list = problem.get_successors(state=current.state)
            for s, a in successors: stack.append(SearchNode(state=s, parent=current, prev_action=a))

    if verbose: print(f'[v] Node visited : {len(visited)}')
    return None

def bfs(problem: SearchProblem, verbose: bool = False) -> Optional[Solution]:
    
    # BFS for algorithmic search in a graph.
    queue: PriorityQueue = PriorityQueue()
    queue.push(item=SearchNode(state=problem.initial_state, parent=None, prev_action=None), priority=0)
    visited: set = set()

    # while we have element to explore;
    while not queue.isEmpty():

        current: SearchNode = queue.pop()
        if current not in visited:
            visited.add(current)

            if problem.is_goal_state(state=current.state):
                if verbose: print(f'[v] Node visited : {len(visited)}')
                return Solution.from_node(node=current)

            # We get every sucessors to current and add them to the queue
            successors: list = problem.get_successors(state=current.state)
            for s, a in successors: queue.push(item=SearchNode(state=s, parent=current, prev_action=a), priority=0)

    if verbose: print(f'[v] Node visited : {len(visited)}')
    return None

def astar(problem: SearchProblem, verbose: bool = False) -> Optional[Solution]:
    
    # A* for algorithmic search in a graph.
    init_node: SearchNode = SearchNode(state=problem.initial_state, parent=None, prev_action=None, cost=0.0)
    queue: PriorityQueue = PriorityQueue()
    
    initial_priority = problem.heuristic(problem_state=problem.initial_state)
    queue.push(item=init_node, priority=initial_priority)

    visited: dict = {}
    
    # while we have element to explore
    while not queue.isEmpty():
        
        current: SearchNode = queue.pop()

        if current.state in visited and visited[current.state] <= current.cost: continue
        visited[current.state] = current.cost

        if problem.is_goal_state(state=current.state):
            if verbose: print(f'[v] Node visited : {len(visited)}')
            return Solution.from_node(node=current)

        for s, a in problem.get_successors(state=current.state):
    
            estimated_distance: float = 1 + problem.heuristic(problem_state=s)
            new_cost: float = current.cost + estimated_distance
            node = SearchNode(state=s, parent=current, prev_action=a, cost=new_cost)
            queue.push(item=node, priority=new_cost)

    if verbose: print(f'[v] Node visited : {len(visited)}')
    return None


class TestHelper:

    def __init__(self, LLEmap: str) -> None:
        
        self.world: World = World(LLEmap)

    def get_exit_problem(self) -> ExitProblem:
        return ExitProblem(self.world)
    
    def get_gem_problem(self) -> GemProblem:
        return GemProblem(self.world)
    
    def get_corner_problem(self) -> CornerProblem:
        return CornerProblem(self.world)
    
    def run_tests(self, pr: SearchProblem) -> dict:

        ret: dict = dict()

        separator: str = '\n-----------------------------'
        print(f'[i] Running tests for {pr}.\n')


        for f, n in zip([dfs, bfs, astar], ['DFS', 'BFS', 'ASTAR']):
            print(f'[i] Running {n} algorithm...')
            ref: float = time.time()
            ret[n] = f(problem=pr, verbose=True)
            delta: float = time.time() - ref
            if ret[n]: print(f'[i] Solution taking {ret[n].n_steps} steps')
            print(f'[i] Time elapsed : {round(delta, 3)}s (={round(delta*1000)} ms).{separator}')

        return ret 

    @staticmethod
    def make_graph(data: dict) -> None:
        
        algos = list(data.keys())
        time_elapsed = [data[algo]['time_elapsed'] for algo in algos]
        nodes_visited = [data[algo]['nodes_visited'] for algo in algos]
        colors = ['r', 'g', 'b']

        indices = np.arange(len(algos))
        bar_width = 0.3
        
        plt.figure(figsize=(6, 4))
        plt.bar(indices, time_elapsed, color=colors, width=bar_width)
        plt.xlabel('Algorithms')
        plt.ylabel('Time elapsed (ms)')
        plt.title('Time elapsed for each algorithm')
        plt.xticks(indices, algos)
        plt.show()

        plt.figure(figsize=(6, 4))
        plt.bar(indices, nodes_visited, color=colors, width=bar_width)
        plt.xlabel('Algorithms')
        plt.ylabel('Number of visited nodes')
        plt.title('Number of visited nodes for each algorithm')
        plt.xticks(indices, algos)
        plt.show()
