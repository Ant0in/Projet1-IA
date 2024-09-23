

from dataclasses import dataclass
from typing import Generic, Optional, TypeVar
from lle import Action, WorldState, World
from priority_queue import PriorityQueue
from problem import SearchProblem, GemProblem, ExitProblem, CornerProblem


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




def dfs(problem: SearchProblem) -> Optional[Solution]:
    
    init_node: SearchNode = SearchNode(state=problem.initial_state, parent=None, prev_action=None)
    stack: list = [init_node]
    visited: set = set()

    while stack:

        current: SearchNode = stack.pop()

        if current not in visited:
            
            visited.add(current)
        
            if problem.is_goal_state(state=current.state):
                # found a solution
                break

            accessibles: list = problem.get_successors(state=current.state)
            for s, a in accessibles: stack.append(SearchNode(state=s, parent=current, prev_action=a))

    return Solution.from_node(node=current)


def bfs(problem: SearchProblem) -> Optional[Solution]:
    
    init_node: SearchNode = SearchNode(state=problem.initial_state, parent=None, prev_action=None)
    queue: PriorityQueue = PriorityQueue()
    queue.push(item=init_node, priority=0)
    visited: set = set()

    while not queue.isEmpty():
        
        current: SearchNode = queue.pop()

        if current not in visited:
            
            visited.add(current)

            if problem.is_goal_state(state=current.state):
                # found a solution
                break

            accessibles: list = problem.get_successors(state=current.state)
            for s, a in accessibles: queue.push(item=SearchNode(state=s, parent=current, prev_action=a), priority=0)

    print(len(visited))
    return Solution.from_node(node=current)


def astar(problem: SearchProblem) -> Optional[Solution]:
    
    init_node: SearchNode = SearchNode(state=problem.initial_state, parent=None, prev_action=None, cost=0.0)
    queue: PriorityQueue = PriorityQueue()
    queue.push(item=init_node, priority=0)
    visited: set = set()

    while not queue.isEmpty():
        
        current: SearchNode = queue.pop()

        if current not in visited:

            visited.add(current)

            if problem.is_goal_state(state=current.state):
                # found a solution
                break

            else:

                accessibles: list = problem.get_successors(state=current.state)
                for s, a in accessibles:
                    new_cost: float = current.cost + problem.heuristic(problem_state=s)
                    node: SearchNode = SearchNode(state=s, parent=current, prev_action=a, cost=new_cost)
                    queue.push(item=node, priority=node.cost)

    return Solution.from_node(node=current)


def visualize_solution(w: World, solution: Solution) -> None:
    
    assert isinstance(solution, Solution)

    import cv2
    def show_img(img) -> None:
        cv2.imshow("Visualisation", img)
        cv2.waitKey(1)
        input("push enter")

    show_img(img=w.get_image())
    for a in solution.actions:
        w.step(action=a)
        show_img(img=w.get_image())




if __name__ == '__main__':

    world_map: str = \
    """
    S0 . . . . . . . . . . .
    .  . . . . . . . . . . .
    .  . . . . . . . . . . .
    .  . . . . . . . . . . .
    .  . . . . . . . . . . X
    """

    w: World = World(map_str=world_map)
    p: CornerProblem = CornerProblem(world=w)