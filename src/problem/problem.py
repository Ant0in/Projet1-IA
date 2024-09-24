
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from lle import World, Action, WorldState



S = TypeVar("S", bound=WorldState)


class SearchProblem(ABC, Generic[S]):
    
    """
    A Search Problem is a problem that can be solved by a search algorithm.

    The generic parameter S is the type of the problem state.
    """

    def __init__(self, world: World) -> None:
        
        self.world: World = world
        self.world.reset()
        self.initial_state: WorldState = world.get_state()
        self.check_if_only_one_agent(state=self.initial_state)

    def load_state(self, state: S) -> None:
        self.world.set_state(state=state)

    def restore_initial_state(self) -> None:
        self.load_state(state=self.initial_state)

    def check_if_only_one_agent(self, state: S) -> None:
        cond: bool = (len(state.agents_positions) == 1 and len(state.agents_alive) == 1)
        assert cond, f'[E] This search problem ({type(self)}) is designed for 1 agent only.'

    def get_successors(self, state: S) -> list[tuple[WorldState, Action]]:
        
        """
        Returns a list of successor states from the given state, along with the corresponding actions taken to reach them.

        This function simulates the possible actions the agent can take from the current state, returning a list of
        (WorldState, Action) pairs. It ensures that only one agent is present and explores the consequences of each action 
        by copying the world state, performing the action, and storing the resulting state-action pair.

        Args:
            state (S): The current state of the world, including the agent's position.

        Returns:
            list[tuple[WorldState, Action]]: A list of tuples, where each tuple contains a resulting world state and the 
            action that led to it.

        Raises:
            AssertionError: If there is more than one agent in the given state.
        """

        self.load_state(state=state)
        self.check_if_only_one_agent(state=state)

        ret: list = list()
        available_actions: list[Action] = self.world.available_actions()[0]
        if self.world.agents[0].is_dead: return ret  # We're returning no actions if the agent is dead

        # Simulate each action by restoring the world state 'state', applying the action, and storing the resulting state-action pair.
        for a in available_actions:
            self.load_state(state=state)
            self.world.step(action=a)
            ret.append((self.world.get_state(), a))

        self.restore_initial_state()
        return ret
    
    @staticmethod
    def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
        return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

    @abstractmethod
    def is_goal_state(self, problem_state: S) -> bool:
        """Whether the given state is the goal state"""

    @abstractmethod
    def heuristic(self, problem_state: S) -> float:
        """Heuristic made to check viability of state nodes"""

