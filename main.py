import numpy as np
from ortools.graph.python import min_cost_flow

Teams = {
    7:"A",
    8:"B",
    9:"C",
    10:"D",
    11:"E",
    12:"F",
}

# Instantiate a SimpleMinCostFlow solver.
smcf = min_cost_flow.SimpleMinCostFlow()

# Define three parallel arrays: start_nodes, end_nodes, and the capacities
start_nodes = np.array([
    0,0,0,0,0,0, # From S
    1,1,1,1, # From 1
    2,2,2, # From 2
    3,3,3, # From 3
    4,4,4, # From 4
    5,5,5,5, # From 5
    6,6,6, # From 6
    7, # ...
    8,
    9,
    10,
    11,
    12, # ...
])

end_nodes = np.array([ # 7-A 8-B 9-C 10-D 11-E 12-F
    1,2,3,4,5,6, # To 1 2 3 4 5 6
    7,9,10,12, # To A C D F
    8,9,11, # To B C E
    7,8,10, # To A B D
    8,9,11, # To B C E
    7,9,10,12, # To A C D F
    7,11,12, # To A E F
    13, # To T ...
    13, 
    13,
    13,
    13,
    13, # To T 
])

capacities = np.array([ # For all edges capatity 1
    1,1,1,1,1,1,
    1,1,1,1,
    1,1,1,
    1,1,1,
    1,1,1,
    1,1,1,1,
    1,1,1,
    1,
    1,
    1,
    1,
    1,
    1,
])

costs = np.array([ 
    0,0,0,0,0,0,
    15,14,9,12,
    12,16,10,
    11,14,12,
    16,11,12,
    13,17,13,15,
    11,16,18,
    0,
    0,
    0,
    0,
    0,
    0,
])

source = 0
sink = 13
tasks = 6

supplies = [tasks]
for i in range(0,12):
    supplies.append(0)
supplies.append(-tasks)

# Add each arc.
for i in range(len(start_nodes)):
    smcf.add_arc_with_capacity_and_unit_cost(
        start_nodes[i], end_nodes[i], capacities[i], costs[i]
    )
# Add node supplies.
for i in range(len(supplies)):
    smcf.set_node_supply(i, supplies[i])

# Find the minimum cost flow between node 0 and node 10.
status = smcf.solve()

if status == smcf.OPTIMAL:
    print("Total cost = ", smcf.optimal_cost())
    print()
    for arc in range(smcf.num_arcs()):
        # Can ignore arcs leading out of source or into sink.
        if smcf.tail(arc) != source and smcf.head(arc) != sink:
            # Arcs in the solution have a flow value of 1. Their start and end nodes
            # give an assignment of worker to task.
            if smcf.flow(arc) > 0:
                print(f"Task {smcf.tail(arc)} assigned to team {Teams[smcf.head(arc)]}.  Cost = {smcf.unit_cost(arc)}")

else:
    print("There was an issue with the min cost flow input.")
    print(f"Status: {status}")