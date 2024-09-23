from lle import WorldState
from .problem import SearchProblem



class GemProblem(SearchProblem[WorldState]):

    """
    A 'less simple' search problem where the agents must reach the exit **alive** AND collect **every gems**.
    """

    def is_goal_state(self, state: WorldState) -> bool:

        # The goal state requires that the agent is alive, positioned on the exit tile,
        # and that all gems have been collected.

        old: WorldState = self.world.get_state()
        self.world.set_state(state=state)
        self.check_if_only_one_agent()

        is_agent_alive: bool = self.world.get_state().agents_alive[0]
        has_arrived: bool = self.world.agents[0].has_arrived
        gem_number: int = self.world.n_gems
        collected_gems_number: int = self.world.gems_collected
        
        self.world.set_state(state=old)  # Restoring previous state.

        return (gem_number == collected_gems_number and has_arrived and is_agent_alive)
    
    def find_gems_coordinates(self, problem_state: WorldState) -> list[tuple[int, int]]:

        old: WorldState = self.world.get_state()
        self.world.set_state(state=problem_state)
        gems: list[tuple[int, int]] = self.world.gems.keys()
        self.world.set_state(state=old)

        return list(gems)
    
    def heuristic(self, problem_state: WorldState) -> float:

        
        exit_dist: float = super().heuristic(problem_state=problem_state)
        gems_coords: list[tuple[int, int]] = self.find_gems_coordinates(problem_state=problem_state)
        
        if not gems_coords: return exit_dist
    
        current_pos: tuple[int, int] = problem_state.agents_positions[0]
        total_distance: float = 0.0

        while gems_coords:
            distances_obj = [(self.manhattan_distance(p1=current_pos, p2=obj), obj) for obj in gems_coords]
            min_dist, nearest_obj = min(distances_obj)
            total_distance += min_dist
            current_pos = nearest_obj
            gems_coords.remove(nearest_obj)
        
        total_distance += self.manhattan_distance(p1=current_pos, p2=self.world.exit_pos[0])
        
        return total_distance
    
