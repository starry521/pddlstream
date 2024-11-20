from Task_Planning.pddlstream import PDDLStreamPlanner
from pddlstream.language.generator import from_gen_fn, from_list_fn, from_fn, from_test
from pddlstream.language.constants import PDDLProblem, And, Equal, print_solution
from pddlstream.algorithms.constraints import PlanConstraints
from pddlstream.algorithms.meta import solve
from pddlstream.language.stream import StreamInfo, DEBUG, SHARED_DEBUG, PartialInputs
from pddlstream.utils import read, elapsed_time, INF, Verbose

DEFAULT_ALGORITHM = 'adaptive'

DOMAIN_PATH = 'input/test1/domain.pddl'
# STREAM_PATH = 'input/test/problem.pddl'

# Initialize
planner = PDDLStreamPlanner(DOMAIN_PATH)

init = [
    ('on-table', 'a'),
    ('on', 'b', 'a'),
    ('clear', 'b'),
    ('arm-empty',),
]
goal = ('on', 'a', 'b')

constant_map = {}
stream_map = {}

kwargs = {
    'algorithm': DEFAULT_ALGORITHM,     # The algorithm to use for solving ('adaptive', 'incremental', 'abstract_focused', 'focused', 'binding').
    'constraints': PlanConstraints(),   # The constraints for the planning problem.
    'stream_info': {},                  # Information about streams used in the problem.
    'replan_actions': set(),            # A set of actions that may need replanning.
    'unit_costs': False,                # If True, assumes unit costs for all actions.
    'success_cost': INF,                # The cost threshold to consider a plan successful.
    'max_time': INF,                    # The maximum time allowed for solving the problem.
    'max_iterations': INF,              # The maximum number of iterations for solving.
    'max_memory': INF,                  # The maximum memory usage allowed during solving.
    'initial_complexity': 0,            # The initial complexity level for solving.
    'complexity_step': 1,               # The increment in complexity level for each step.
    'max_complexity': INF,              # The maximum allowable complexity level.
    'max_skeletons': INF,               # The maximum number of plan skeletons to explore.
    'search_sample_ratio': 0,           # The ratio of search to sampling in planning.
    'max_failures': 0,                  # The maximum number of failures allowed during solving.
    'unit_efforts': False,              # If True, assumes unit efforts for all actions.
    'max_effort': INF,                  # The maximum effort allowed for solving.
    'effort_weight': None,              # The weight assigned to effort in the optimization.
    'reorder': True,                    # Whether to reorder actions in the plan.
    'visualize': False,                 # If True, enables visualization during solving.
    'verbose': True                     # If True, prints detailed logs during solving.
}

# Plan
solution = planner.plan(init, goal, constant_map, stream_map, **kwargs)

# Print result
print_solution(solution)