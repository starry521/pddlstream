import os 
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pddlstream.language.generator import from_gen_fn, from_list_fn, from_fn, from_test
from pddlstream.language.constants import PDDLProblem, And, Equal, print_solution
from pddlstream.algorithms.constraints import PlanConstraints
from pddlstream.algorithms.meta import solve
from pddlstream.language.stream import StreamInfo, DEBUG, SHARED_DEBUG, PartialInputs
from pddlstream.utils import read, elapsed_time, INF, Verbose

DEFAULT_ALGORITHM = 'adaptive'

class PDDLStreamPlanner:
    """
    A class to encapsulate the task planning process using PDDLStream.
    """

    def __init__(self, domain_pddl_path=None, stream_pddl_path=None):
        """
        Initializes the PDDLStreamPlanner with paths to domain and stream PDDL files.

        Args:
            domain_pddl_path (str): Path to the domain PDDL file.
            stream_pddl_path (str): Path to the stream PDDL file.
        """
        
        # `domain_pddl`:
        # The domain PDDL file defines the static aspects of the problem domain. 
        # It includes:
        # - Types: Defines the object types (e.g., robots, cups, tables).
        # - Predicates: Describes the logical conditions to represent the state (e.g., "On", "Empty", "Holding").
        # - Actions: Defines the allowed actions, their preconditions, and their effects (e.g., "pick", "place").
        # 
        # The `domain_pddl` is essential for describing the "rules" and constraints of the planning problem.
        # Example: A robot can only pick an object if it is clear and the robot is empty-handed.
        self.domain_pddl = read(domain_pddl_path)   if domain_pddl_path is not None else None
        
        # `stream_pddl`:
        # The stream PDDL file complements the domain PDDL by defining the dynamic aspects of the problem. 
        # It includes:
        # - Streams: Describes how to dynamically generate objects or information required for planning (e.g., positions, free spaces).
        # - Conditions and Effects: Specifies the inputs, outputs, and logical effects of the streams.
        #
        # The `stream_pddl` enables the system to handle real-world uncertainty by generating information on demand.
        # Example: Dynamically generating the position of a cup or identifying if a coaster is clear.
        self.stream_pddl = read(stream_pddl_path)   if stream_pddl_path is not None else None

    def create_problem(self, init, goal, constant_map, stream_map):
        """
        Creates a PDDL problem.

        Args:
            init (list): Initial state of the problem.
            goal (list or And): Goal condition(s) for the problem.
            constant_map (dict): Mapping of constants in the PDDL problem.
            stream_map (dict): Mapping of streams to their generators or tests.

        Returns:
            PDDLProblem: The constructed PDDL problem.
        """
        return PDDLProblem(self.domain_pddl, constant_map, self.stream_pddl, stream_map, init, goal)

    def solve_problem(self, pddl_problem, **kwargs):
        """
        Solves a PDDL problem using PDDLStream.

        Args:
            args (Namespace): Command-line arguments or configuration object containing algorithm and unit cost settings.
            pddl_problem (PDDLProblem): The PDDL problem to solve, including domain and problem definitions.
            **kwargs: Additional keyword arguments for solving configuration.

        Returns:
            tuple: A tuple containing the plan, cost, and evaluations. If solving fails, returns (None, None, None).
        """
        
        # algorithm': 'adaptive',           # The algorithm to use for solving ('adaptive', 'incremental', 'focused', 'binding').
        # constraints: PlanConstraints(),   # The constraints for the planning problem.
        # stream_info: stream_info,         # Information about streams used in the problem.
        # replan_actions: set(),            # A set of actions that may need replanning.
        # unit_costs: False,                # If True, assumes unit costs for all actions.
        # success_cost: INF,                # The cost threshold to consider a plan successful.
        # max_time: INF,                    # The maximum time allowed for solving the problem.
        # max_iterations: INF,              # The maximum number of iterations for solving.
        # max_memory: INF,                  # The maximum memory usage allowed during solving.
        # initial_complexity: 0,            # The initial complexity level for solving.
        # complexity_step: 1,               # The increment in complexity level for each step.
        # max_complexity: INF,              # The maximum allowable complexity level.
        # max_skeletons: INF,               # The maximum number of plan skeletons to explore.
        # search_sample_ratio: 0,           # The ratio of search to sampling in planning.
        # max_failures: 0,                  # The maximum number of failures allowed during solving.
        # unit_efforts: False,              # If True, assumes unit efforts for all actions.
        # max_effort: INF,                  # The maximum effort allowed for solving.
        # effort_weight: None,              # The weight assigned to effort in the optimization.
        # reorder: True,                    # Whether to reorder actions in the plan.
        # visualize: False,                 # If True, enables visualization during solving.
        # verbose: True                     # If True, prints detailed logs during solving.
        solution = solve(pddl_problem, **kwargs)
        return solution

    def plan(self, init, goal, constant_map, stream_map, **kwargs):
        """
        Combines problem creation and solving into one function for planning tasks.

        Args:
            init (list): Initial state of the problem.
            goal (list or And): Goal condition(s) for the problem.
            constant_map (dict): Mapping of constants in the PDDL problem.
            stream_map (dict): Mapping of streams to their generators or tests.
            **kwargs: Additional keyword arguments for solving configuration.

        Returns:
            tuple: A tuple containing the plan, cost, and evaluations. If solving fails, returns (None, None, None).
        """
        pddl_problem = self.create_problem(init, goal, constant_map, stream_map)
        solution = self.solve_problem(pddl_problem, **kwargs)
        return solution
    
    def print_solution(self, solution):
        """
        Prints the solution generated by the planner.

        Args:
            solution (tuple): The solution tuple returned by the `solve` method. 
                Typically, it contains:
                - plan (list): A list of actions representing the solution plan.
                - cost (float): The cost associated with the solution plan.
                - evaluations (dict): Additional evaluation data (e.g., performance metrics).

        Behavior:
            This method utilizes the `pddlstream.language.constants.print_solution` function 
            to display the details of the solution in a human-readable format.
            The output may include:
            - The sequence of actions in the plan.
            - The total cost of the plan.
            - Any additional information related to evaluations.
        """
        print_solution(solution)