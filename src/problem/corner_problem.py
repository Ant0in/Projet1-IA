
from lle import WorldState, World, Action
from .problem import SearchProblem
import copy


class CornerState(WorldState):

    def __new__(cls, agents_positions: list[object], gems_collected: list[bool], agents_alive: list[bool] | None = None, *args, **kwargs) -> None:
        return super(CornerState, cls).__new__(cls, agents_positions, gems_collected, agents_alive)

    def __init__(self, agents_positions: list[object], gems_collected: list[bool], agents_alive: list[bool] | None = None, visited_corners: list[bool] | None = None) -> None:
        super().__init__(agents_positions, gems_collected, agents_alive)
        self.visited_corners: list[bool] = visited_corners or [False, False, False, False]

    def __hash__(self) -> int:
        return super().__hash__() + hash(tuple(self.visited_corners))


class CornerProblem(SearchProblem[CornerState]):
    
    def __init__(self, world: World) -> None:
        
        super().__init__(world)
        self.corners: list[tuple[int, int]] = [(0, 0), (0, world.width - 1), (world.height - 1, 0), (world.height - 1, world.width - 1)]

        self.initial_state: CornerState = CornerState(
            agents_positions=self.initial_state.agents_positions,
            gems_collected=self.initial_state.gems_collected,
            agents_alive=self.initial_state.agents_alive,
            visited_corners=None
        )

    def is_goal_state(self, state: CornerState) -> bool:

        self.load_state(state=state)
        self.check_if_only_one_agent(state=state)

        is_agent_alive: bool = self.world.get_state().agents_alive[0]
        has_arrived: bool = self.world.agents[0].has_arrived

        self.restore_initial_state()
        return (has_arrived and is_agent_alive and all(state.visited_corners))

    def get_successors(self, state: CornerState) -> list[tuple[CornerState, Action]]:
        
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
                state.visited_corners[idx] = True
            else: pass

    def heuristic(self, problem_state: CornerState) -> float:
        
        self.check_if_only_one_agent(state=problem_state)
        agent_pos: tuple[int, int] = problem_state.agents_positions[0]

        if all(problem_state.visited_corners):
            self.load_state(state=problem_state)
            exit_coords: list[tuple[int, int]] = self.world.exit_pos
            distances: list[float] = [self.manhattan_distance(p1=agent_pos, p2=ec) for ec in exit_coords]
            self.restore_initial_state()
            d: float = min(distances)
        
        else:
            corner_coords: list[tuple[int, int]] = [c for visited_bool, c in zip(problem_state.visited_corners, self.corners) if not visited_bool]
            distances_to_corners: list[float] = [self.manhattan_distance(p1=agent_pos, p2=cc) for cc in corner_coords]
            
            min_dist_to_corner = min(distances_to_corners)
            nearest_corner = corner_coords[distances_to_corners.index(min_dist_to_corner)]
            
            exit_coords: list[tuple[int, int]] = self.world.exit_pos
            distances_to_exit_from_corner: list[float] = [self.manhattan_distance(p1=nearest_corner, p2=ec) for ec in exit_coords]
            dist_corner_to_exit = min(distances_to_exit_from_corner)
            
            d: float = min_dist_to_corner + dist_corner_to_exit

        return d