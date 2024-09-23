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
    
    def heuristic(self, problem_state: WorldState) -> float:

        # not implemented yet
        return 0.0
    


