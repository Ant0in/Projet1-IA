from lle import WorldState
from .problem import SearchProblem



class ExitProblem(SearchProblem[WorldState]):
    
    """
    A simple search problem where the agents must reach the exit **alive**.
    """

    def is_goal_state(self, state: WorldState) -> bool:
        
        # The goal state requires that the agent is alive and positioned on the exit tile.
        self.load_state(state=state)
        self.check_if_only_one_agent(state=state)

        is_agent_alive: bool = state.agents_alive[0]
        has_arrived: bool = self.world.agents[0].has_arrived

        self.restore_initial_state()
        return has_arrived and is_agent_alive
    
    def heuristic(self, problem_state: WorldState) -> float:
        
        # In this instance of the problem (exit problem), we are focusing solely on the distance
        # between the agent's position and the nearest exit. 
        # Therefore, we will use the Manhattan distance formula.
        
        self.check_if_only_one_agent(state=problem_state)
        self.load_state(state=problem_state)
        
        agent_position: tuple[int, int] = problem_state.agents_positions[0]
        exit_pos: list[tuple[int, int]] = self.world.exit_pos

        distances: list[float] = [self.manhattan_distance(p1=agent_position, p2=ep) for ep in exit_pos]
        self.restore_initial_state()
        return min(distances)
