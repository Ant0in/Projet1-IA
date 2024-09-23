from lle import WorldState
from .problem import SearchProblem



class ExitProblem(SearchProblem[WorldState]):
    
    """
    A simple search problem where the agents must reach the exit **alive**.
    """

    def is_goal_state(self, state: WorldState) -> bool:
        
        # The goal state requires that the agent is alive and positioned on the exit tile.

        old: WorldState = self.world.get_state()
        self.world.set_state(state=state)
        self.check_if_only_one_agent()

        is_agent_alive: bool = state.agents_alive[0]
        has_arrived: bool = self.world.agents[0].has_arrived

        self.world.set_state(state=old)  # Restoring previous state.
        return has_arrived and is_agent_alive
    
    def heuristic(self, problem_state: WorldState) -> float:
        
        # In this instance of the problem (exit problem), we are focusing solely on the distance
        # between the agent's position and the exit. Therefore, we will use the Manhattan distance formula.
        return super().heuristic(problem_state=problem_state)
    
