
from lle import WorldState, World, Action
from .problem import SearchProblem
import copy


class CornerState(WorldState):

    def __new__(cls, agents_positions: list[object], gems_collected: list[bool], agents_alive: list[bool] | None = None, *args, **kwargs):
        return super(CornerState, cls).__new__(cls, agents_positions, gems_collected, agents_alive)

    def __init__(self, agents_positions: list[object], gems_collected: list[bool], agents_alive: list[bool] | None = None, visited_corners: list[bool] | None = None):
        super().__init__(agents_positions, gems_collected, agents_alive)
        self.visited_corners = visited_corners or [False, False, False, False]

    def __hash__(self) -> int:
        return super().__hash__() + hash(tuple(self.visited_corners))


class CornerProblem(SearchProblem[CornerState]):
    
    def __init__(self, world: World):
        
        super().__init__(world)
        self.corners: list[tuple[int, int]] = [(0, 0), (0, world.width - 1), (world.height - 1, 0), (world.height - 1, world.width - 1)]

        self.initial_state: CornerState = CornerState(
            agents_positions=self.initial_state.agents_positions,
            gems_collected=self.initial_state.gems_collected,
            agents_alive=self.initial_state.agents_alive,
            visited_corners=None
        )

    def is_goal_state(self, state: CornerState) -> bool:

        old: WorldState = self.world.get_state()
        self.world.set_state(state=state)
        self.check_if_only_one_agent()

        is_agent_alive: bool = self.world.get_state().agents_alive[0]
        has_arrived: bool = self.world.agents[0].has_arrived

        self.world.set_state(state=old)  # Rétablir l'état précédent.

        return (has_arrived and is_agent_alive and all(state.visited_corners))

    def get_successors(self, state: CornerState):
        
        ret: list[tuple[CornerState, Action]] = list() 

        for s, a in super().get_successors(state=state):
            
            corner_compatible_s: CornerState = CornerState(
                agents_positions=s.agents_positions,
                gems_collected=s.gems_collected,
                agents_alive=s.agents_alive,
                visited_corners=copy.deepcopy(state.visited_corners))
            
            self.update_corner_visited(state=corner_compatible_s)
            ret.append((corner_compatible_s, a))

        return ret

    def update_corner_visited(self, state: CornerState) -> list[bool]:
    
        agent_pos: tuple[int, int] = state.agents_positions[0]

        for idx, c in enumerate(self.corners):
            if c == agent_pos:
                state.visited_corners[idx] = True  # Mise à jour directe de la liste
            else: pass

