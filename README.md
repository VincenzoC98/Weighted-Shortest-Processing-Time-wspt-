# Weighted-Shortest-Processing-Time-wspt-
A scheduling problem solved with heuristic and meta-heuristic algorithms and the mathematical model.

**Project Description and Code Explanation**

### Project Overview
The project focuses on solving a complex scheduling problem involving multiple machines and jobs while minimizing the total weighted completion time. The study utilizes advanced mathematical formulations, particularly the Arc-Flow (AF) model, to achieve efficient scheduling. The project also explores enhanced versions of AF models to optimize computational efficiency and reduce the number of variables and constraints.

### Code Structure and Explanation

#### 1. **Mathematical Formulations**
The core of the project revolves around different mathematical models to represent and solve the scheduling problem:
   - **Time-Indexed Formulation (TI)**: Uses binary variables to determine job start times within a defined time horizon.
   - **Convex Integer Quadratic Programming (CIQP)**: Adapts an integer quadratic program to scheduling.
   - **Set Covering (SC) Formulation**: Defines the problem as a covering problem with exponential schedules.
   - **Arc-Flow (AF) Formulation**: Uses graph-based models where paths in a network represent machine schedules.
   - **Enhanced Arc-Flow (EAF) Formulation**: Implements variable reduction techniques to optimize AF.

#### 2. **Algorithm Implementation**
The scheduling problem is tackled through a computational approach coded in Python and executed using Jupyter Notebook:
   
   - **Data Initialization**:
     - Imports necessary libraries (`pandas`, `numpy`, `matplotlib.pyplot`, `seaborn`, `random`, `pulp`).
     - Initializes machine and job parameters.
     - Defines lists of processing times (`tempi`) and weights (`pesi`).
   
   - **Mathematical Model**:
     - Defines the list of jobs (`J`) and machines (`M`).
     - Creates a `pulp.LpProblem` model to minimize scheduling cost.
     - Introduces binary decision variables `x[j,t]` to indicate job start times.
     - Defines the objective function to minimize total weighted completion time.
     - Implements constraints:
       - Each job starts exactly once.
       - Concurrent jobs do not exceed machine capacity.
       - Decision variables must be binary.
     - Solves the problem and prints the solution status and objective value.
   
   - **Heuristic Algorithm**:
     - Selects a random job order.
     - Allocates jobs to machines to minimize completion time.
     - Evaluates whether the heuristic solution satisfies the scheduling horizon `T`.
   
   - **Local Search Swap**:
     - Implements a swap-based local search to refine job assignments.
     - Iteratively exchanges jobs between machines to improve scheduling efficiency.
   
   - **Multi-Start Algorithm**:
     - Generates multiple initial solutions using different job orders.
     - Applies heuristic and local search methods to each initial solution.
     - Selects the best solution based on the objective function.
   
   - **Genetic Metaheuristic**:
     - Implements a genetic algorithm to optimize job scheduling.
     - Uses crossover and mutation operators to explore the solution space.
     - Evaluates populations over multiple iterations to find the best schedule.

#### 3. **Computational Experiments and Results**
The notebook includes:
   - Benchmark testing with different machine-job configurations.
   - Performance comparison between different formulations.
   - Execution time analysis to evaluate the efficiency of each method.
   - Visualization of scheduling results and job allocation.

### Conclusion
The project successfully optimizes the scheduling problem by employing advanced mathematical techniques and computational algorithms. The enhanced AF model (EAF) significantly reduces computational complexity, making it a viable solution for large-scale scheduling problems. Future improvements may include heuristic approaches and further variable reduction techniques.

