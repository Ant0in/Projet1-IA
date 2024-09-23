from lle import Action, World, WorldState

from problem import GemProblem
from search import astar, dfs, bfs

from .utils import check_gem_problem, GEMS


def test_goal_state_no_gems():
    world = World("S0 . X")
    problem = GemProblem(world)
    assert not problem.is_goal_state(problem.initial_state)
    end = WorldState([(0, 2)], [])
    assert problem.is_goal_state(end)


def test_goal_state():
    world = World("S0 G G G G G G G X")
    problem = GemProblem(world)
    assert not problem.is_goal_state(problem.initial_state)
    end = WorldState([(0, world.width - 1)], [True] * world.n_gems)
    assert problem.is_goal_state(end)


def test_goal_state_multiple_exits():
    world = World("S0 G X X")
    problem = GemProblem(world)
    goal_state1 = WorldState([(0, 2)], [True])
    goal_state2 = WorldState([(0, 3)], [True])
    world.set_state(goal_state1)
    assert problem.is_goal_state(goal_state1)
    assert problem.is_goal_state(goal_state2)


def test_goal_state_dead():
    world = World("S0 G X")
    problem = GemProblem(world)
    assert not problem.is_goal_state(problem.initial_state)
    end = WorldState([(0, 2)], [True], agents_alive=[False])
    assert not problem.is_goal_state(end), "The agent is dead, it should not be a goal state"


def test_successors_one_agent():
    world = World(
        """
        S0 . X
        . . ."""
    )
    problem = GemProblem(world)
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
    problem = GemProblem(world)
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
    problem = GemProblem(world)
    world.step(Action.EAST)
    state = world.get_state()
    successors = list(problem.get_successors(state))
    assert len(successors) == 0, "The agent is dead, there should be no successor"


def test_dfs():
    world = World(GEMS)
    problem = GemProblem(world)
    solution = dfs(problem)
    assert solution is not None
    check_gem_problem(problem, solution)
    if world.n_gems != world.gems_collected:
        raise AssertionError("Your is_goal_state method is likely erroneous beacuse some gems have not been collected")


def test_astar():
    world = World(GEMS)
    problem = GemProblem(world)
    solution = astar(problem)
    assert solution is not None
    check_gem_problem(problem, solution)
    if world.n_gems != world.gems_collected:
        raise AssertionError("Your is_goal_state method is likely erroneous beacuse some gems have not been collected")


def test_bfs():
    world = World(GEMS)
    problem = GemProblem(world)
    solution = bfs(problem)
    assert solution is not None
    check_gem_problem(problem, solution)
    if world.n_gems != world.gems_collected:
        raise AssertionError("Your is_goal_state method is likely erroneous beacuse some gems have not been collected")
