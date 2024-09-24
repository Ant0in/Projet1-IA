from lle import World
from search import bfs
from problem import ExitProblem, CornerProblem, GemProblem

from .utils import check_exit_problem, check_corner_problem, check_gem_problem, IMPOSSIBLE, EMPTY, ZIGZAG, GEMS


def test_exit_empty():
    world = World(EMPTY)
    problem = ExitProblem(world)
    solution = bfs(problem)
    assert solution is not None
    check_exit_problem(problem, solution)


def test_corner_empty():
    world = World(EMPTY)
    problem = CornerProblem(world)
    solution = bfs(problem)
    assert solution is not None
    check_corner_problem(problem, solution)


def test_gem_empty():
    world = World(EMPTY)
    problem = GemProblem(world)
    solution = bfs(problem)
    assert solution is not None
    check_gem_problem(problem, solution)


def test_exit_zigzag():
    world = World(ZIGZAG)
    problem = ExitProblem(world)
    solution = bfs(problem)
    assert solution is not None
    check_exit_problem(problem, solution)


def test_corner_zigzag():
    world = World(ZIGZAG)
    problem = CornerProblem(world)
    solution = bfs(problem)
    assert solution is None


def test_gem_zigzag():
    world = World(ZIGZAG)
    problem = GemProblem(world)
    solution = bfs(problem)
    assert solution is not None
    check_gem_problem(problem, solution)


def test_impossible():
    world = World(IMPOSSIBLE)
    problem = ExitProblem(world)
    assert bfs(problem) is None

    world = World(IMPOSSIBLE)
    problem = CornerProblem(world)
    assert bfs(problem) is None

    world = World(IMPOSSIBLE)
    problem = GemProblem(world)
    assert bfs(problem) is None


def test_exit_level1():
    world = World.level(1)
    problem = ExitProblem(world)
    solution = bfs(problem)
    assert solution is not None
    check_exit_problem(problem, solution)


def test_corner_level1():
    world = World.level(1)
    problem = CornerProblem(world)
    solution = bfs(problem)
    assert solution is not None
    check_corner_problem(problem, solution)


def test_gem():
    world = World(GEMS)
    problem = GemProblem(world)
    solution = bfs(problem)
    assert solution is not None
    check_gem_problem(problem, solution)
