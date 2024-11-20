from Task_Planning.pddlstream import PDDLStreamPlanner, And, SHARED_DEBUG, StreamInfo, PartialInputs

ROBOT = 'gripper'
CUP = 'cup'
COASTER = 'block'
DEFAULT_ALGORITHM = 'adaptive'

DOMAIN_PATH = '../input/test2/domain.pddl'
STREAM_PATH = '../input/test2/stream.pddl'

# Initialize
planner = PDDLStreamPlanner(DOMAIN_PATH, STREAM_PATH)

initial_poses = {
    ROBOT: (0., 15., 0.),
    CUP: (7.5, 0., 0.),
    'sugar_cup': (-10., 0., 0.),
    'cream_cup': (15., 0, 0),
    'spoon': (0.5, 0.5, 0),
    'stirrer': (20, 0.5, 0),
    COASTER: (-20., 0, 0),
}

block_goal = (-25, 0, 0)

init = [
    ('IsPose', COASTER, block_goal),
    ('Empty', ROBOT),
    ('CanMove', ROBOT),
    ('HasSugar', 'sugar_cup'),
    ('HasCream', 'cream_cup'),
    ('IsPourable', 'cream_cup'),
    ('Stackable', CUP, COASTER),
    ('Clear', COASTER),
]

for name, pose in initial_poses.items():
    if 'gripper' in name:
        init += [('IsGripper', name)]
    if 'cup' in name:
        init += [('IsCup', name)]
    if 'spoon' in name:
        init += [('IsSpoon', name), ('IsStirrer', name)]
    if 'stirrer' in name:
        init += [('IsStirrer', name)]
    if 'block' in name:
        init += [('IsBlock', name)]
    init += [
        ('IsPose', name, pose),
        ('AtPose', name, pose),
        ('TableSupport', pose),
    ]

goal_literals = [
    ('AtPose', COASTER, block_goal),
    ('On', CUP, COASTER),
    ('HasCoffee', CUP),
    ('HasCream', CUP),
    ('HasSugar', CUP),
    ('Mixed', CUP),
    ('Empty', ROBOT),
]
goal = And(*goal_literals)

constant_map = {}
stream_map = SHARED_DEBUG

stream_info = {
    'sample-grasp-ctrl': StreamInfo(opt_gen_fn=PartialInputs(unique=False)),
}

kwargs = {
    'planner': 'ff-eager',
    'unit_costs': False,                # If True, assumes unit costs for all actions.
    'unit_efforts': True,              # If True, assumes unit efforts for all actions.
    'effort_weight': 1,              # The weight assigned to effort in the optimization.
}

# Plan
solution = planner.plan(init, goal, constant_map, stream_map, **kwargs)

# Print result
planner.print_solution(solution)