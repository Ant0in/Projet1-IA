
from lle import WorldState, World, Action
from .problem import SearchProblem


class CornerState(WorldState):

    def __init__(self, agents_positions: list[tuple[int, int]], gems_collected: list[bool], corner_visited: list[bool], agents_alive: list[bool] | None) -> None:

        super().__init__(agents_positions, gems_collected, agents_alive)
        self.corner_visited: list[bool] = corner_visited


class CornerProblem(SearchProblem[CornerState]):
    
    def __init__(self, world: World):
        
        super().__init__(world)
        self.corners: list[tuple[int, int]] = [(0, 0), (0, world.width - 1), (world.height - 1, 0), (world.height - 1, world.width - 1)]
        
        cs = CornerState(agents_positions=self.initial_state.agents_positions,
                                         gems_collected=self.initial_state.gems_collected,
                                         corner_visited=[False] * 4,
                                         agents_alive=self.initial_state.agents_alive)
        self.initial_state = cs


    def is_goal_state(self, state: CornerState) -> bool:
        raise NotImplementedError()

    def get_successors(self, state: CornerState):
        raise NotImplementedError()
