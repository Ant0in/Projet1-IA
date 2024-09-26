

from dataclasses import dataclass
from typing import Generic, Optional, TypeVar
from lle import Action, WorldState, World
from priority_queue import PriorityQueue
from problem import SearchProblem, GemProblem, ExitProblem, CornerProblem
import cv2



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



def visualize_solution(w: World, solution: Solution) -> None:
    
    # Little method used to visualize solutions using openCV2
    if not isinstance(solution, Solution): print('No solution found!'); return

    def show_img(img, step: int, action: Action) -> None:
        cv2.imshow("Visualisation", img)
        cv2.waitKey(1)
        input(f'[Step {step}] Action : {action} ')

    show_img(img=w.get_image(), step=0, action='Initial state')
    for step, a in enumerate(solution.actions):
        w.step(action=a)
        show_img(img=w.get_image(), step=step+1, action=a)
    print(f'[G] Goal reached in {len(solution.actions)} steps.')

def dfs(problem: SearchProblem) -> Optional[Solution]:
    
    # DFS Method for algorithmic search in a graph.
    stack: list[SearchNode] = [SearchNode(state=problem.initial_state, parent=None, prev_action=None)]
    visited: set = set()

    # while we have element to explore / we did not find any solution ;
    while stack:

        current: SearchNode = stack.pop()
        if current not in visited:            
            visited.add(current)
    
            if problem.is_goal_state(state=current.state):
                return Solution.from_node(node=current)

            # We get every sucessors to current and add them to the stack
            successors: list = problem.get_successors(state=current.state)
            for s, a in successors: stack.append(SearchNode(state=s, parent=current, prev_action=a))

    return None

def bfs(problem: SearchProblem) -> Optional[Solution]:
    
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
                return Solution.from_node(node=current)

            # We get every sucessors to current and add them to the queue
            successors: list = problem.get_successors(state=current.state)
            for s, a in successors: queue.push(item=SearchNode(state=s, parent=current, prev_action=a), priority=0)

    return None

def astar(problem: SearchProblem) -> Optional[Solution]:
    
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

        if problem.is_goal_state(state=current.state): return Solution.from_node(node=current)

        for s, a in problem.get_successors(state=current.state):
    
            estimated_distance: float = 1 + problem.heuristic(problem_state=s)
            new_cost: float = current.cost + estimated_distance
            node = SearchNode(state=s, parent=current, prev_action=a, cost=new_cost)
            queue.push(item=node, priority=new_cost)

    return None



if __name__ == '__main__':

    world_map: str = \
    """
    . . . . . . . . . . . .
    .  . . . . . . . . G . .
    S0  . . . . . . . . . . .
    @  @ @ @ @ @ @ @ @ G . X
    G  . . . . . . . . . . .
    """

    w: World = World(map_str=world_map)
    p: SearchProblem = CornerProblem(world=w)
    s: Solution = astar(problem=p)
    visualize_solution(w=w, solution=s)