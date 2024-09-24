
from lle import WorldState
from .problem import SearchProblem
from .exit_problem import ExitProblem


class GemProblem(SearchProblem[WorldState]):

    """
    A 'less simple' search problem where the agents must reach the exit **alive** AND collect **every gems**.
    """

    def is_goal_state(self, state: WorldState) -> bool:
        
        # The goal state requires that the agent is alive, positioned on the exit tile,
        # and that all gems have been collected.
        self.load_state(state=state)
        self.check_if_only_one_agent(state=state)

        is_agent_alive: bool = state.agents_alive[0]
        has_arrived: bool = self.world.agents[0].has_arrived
        gem_number: int = self.world.n_gems
        collected_gems_number: int = self.world.gems_collected

        self.restore_initial_state()
        return (gem_number == collected_gems_number and has_arrived and is_agent_alive)
 
    def find_gems_coordinates(self, problem_state: WorldState) -> list[tuple[int, int]]:

        bckup: WorldState = self.world.get_state()
        self.load_state(state=problem_state)
        gems: list[tuple[int, int]] = [c for c, gem in self.world.gems.items() if not gem.is_collected]
        self.load_state(state=bckup)
        return list(gems)
    
    def heuristic(self, problem_state: WorldState) -> float:

        self.check_if_only_one_agent(state=problem_state)
        agent_pos: tuple[int, int] = problem_state.agents_positions[0]

        if all(problem_state.gems_collected):
            self.load_state(state=problem_state)
            exit_coords: list[tuple[int, int]] = self.world.exit_pos
            distances: list[float] = [self.manhattan_distance(p1=agent_pos, p2=ec) for ec in exit_coords]
            self.restore_initial_state()
            d: float = min(distances)
        
        else:
            gems_coords: list[tuple[int, int]] = self.find_gems_coordinates(problem_state=problem_state)
            distances_to_gems: list[float] = [self.manhattan_distance(p1=agent_pos, p2=gc) for gc in gems_coords]
            
            min_dist_to_gem = min(distances_to_gems)
            nearest_gem = gems_coords[distances_to_gems.index(min_dist_to_gem)]
            
            exit_coords: list[tuple[int, int]] = self.world.exit_pos
            distances_to_exit_from_gem: list[float] = [self.manhattan_distance(p1=nearest_gem, p2=ec) for ec in exit_coords]
            dist_gem_to_exit = min(distances_to_exit_from_gem)
            
            d: float = min_dist_to_gem + dist_gem_to_exit

        return d
    
