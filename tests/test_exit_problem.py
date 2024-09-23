from lle import World, WorldState, Action
from problem import ExitProblem


def test_goal_state():
    world = World("S0 . X")
    problem = ExitProblem(world)
    assert not problem.is_goal_state(problem.initial_state)
    end = WorldState([(0, 2)], [])
    assert problem.is_goal_state(end)


def test_goal_state_multiple_exits():
    world = World("S0 . X X")
    problem = ExitProblem(world)
    goal_state1 = WorldState([(0, 2)], [])
    goal_state2 = WorldState([(0, 3)], [])
    world.set_state(goal_state1)
    assert problem.is_goal_state(goal_state1)
    assert problem.is_goal_state(goal_state2)


def test_goal_state_dead():
    world = World("S0 V X")
    problem = ExitProblem(world)
    assert not problem.is_goal_state(problem.initial_state)
    end = WorldState([(0, 2)], [], agents_alive=[False])
    assert not problem.is_goal_state(end), "The agent is dead, it should not be a goal state"


def test_successors_one_agent():
    world = World(
        """
        S0 . X
        . . ."""
    )
    problem = ExitProblem(world)
    successors = list(problem.get_successors(problem.initial_state))
    assert len(successors) == 3
    world.reset()
    available = world.available_actions()[0]
    agent_pos = ((0, 0), (0, 1), (1, 0))
    for state, action in successors:
        assert action in available
        assert state.agents_positions[0] in agent_pos


def test_successors_one_agent_obstacle():
    world = World(
        """
        S0 . X
        @ . ."""
    )
    problem = ExitProblem(world)
    successors = list(problem.get_successors(problem.initial_state))
    assert len(successors) == 2
    world.reset()
    available = world.available_actions()[0]
    agent_pos = ((0, 0), (0, 1))
    for state, action in successors:
        assert action in available
        assert state.agents_positions[0] in agent_pos


def test_successors_agent_dead():
    world = World(
        """
        S0 V X
        . . ."""
    )
    problem = ExitProblem(world)
    world.step(Action.EAST)
    state = world.get_state()
    successors = list(problem.get_successors(state))
    assert len(successors) == 0, "The agent is dead, there should be no successor"
