
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from lle import World, Action, WorldState



S = TypeVar("S", bound=WorldState)


class SearchProblem(ABC, Generic[S]):
    
    """
    A Search Problem is a problem that can be solved by a search algorithm.

    The generic parameter S is the type of the problem state.
    """

    def __init__(self, world: World):
        
        self.world: World = world
        self.world.reset()
        self.initial_state: WorldState = world.get_state()

    @abstractmethod
    def is_goal_state(self, problem_state: S) -> bool:
        """Whether the given state is the goal state"""

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

        old: WorldState = self.world.get_state()
        self.world.set_state(state=state)
        self.check_if_only_one_agent()

        ret: list = list()
        available_actions: list[list[Action]] = self.world.available_actions()[0]
        if self.world.agents[0].is_dead: return ret  # We're returning no actions if the agent is dead

        # Simulate each action by restoring the world state 'state', applying the action, and storing the resulting state-action pair.
        for a in available_actions:
            self.world.set_state(state=state)
            self.world.step(action=a)
            ret.append((self.world.get_state(), a))

        # Restoring previous world state.
        self.world.set_state(state=old)
        return ret
    
    @staticmethod
    def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
        return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
    
    def check_if_only_one_agent(self) -> None:
        assert len(self.world.agents) == 1, f'[E] This search problem ({type(self)}) is designed for 1 agent only. (got {len(self.world.agents)})'

    def heuristic(self, problem_state: S) -> float:
        # Manhattan distance heuristic.
        agent_pos: tuple[int, int] = problem_state.agents_positions[0]
        exit_pos: tuple[int, int] = self.world.exit_pos[0]
        return self.manhattan_distance(p1=agent_pos, p2=exit_pos)

