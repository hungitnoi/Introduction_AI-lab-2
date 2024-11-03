from collections import deque
import pydot_ng as pydot
import argparse
import os

# Update this path if needed to point to your Graphviz 'bin' folder
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin'

options = [(1, 0), (0, 1), (1, 1), (0, 2), (2, 0)]
Parent = dict()
graph = pydot.Dot(graph_type='graph', strict=False, bgcolor="#fff3af",
                  label="fig: Missionaries and Cannibal State Space Tree",
                  fontcolor="red", fontsize="24", overlap="true")

# To track node
i = 0

arg = argparse.ArgumentParser()
arg.add_argument("-d", "--depth", required=False,
                 help="Maximum depth up to which you want to generate Space State Tree")

args = vars(arg.parse_args())
max_depth = int(args.get("depth", 20))

def is_valid_move(number_missionaries, number_cannibals):
    return (0 <= number_missionaries <= 3) and (0 <= number_cannibals <= 3)

def write_image(file_name="state_space"):
    try:
        graph.write_png(f"{file_name}_{max_depth}.png")
        print(f"File {file_name}_{max_depth}.png successfully written.")
    except Exception as e:
        print("Error while writing file:", e)

def draw_edge(number_missionaries, number_cannibals, side, depth_level, node_num):
    u, v = None, None
    parent_key = (number_missionaries, number_cannibals, side, depth_level, node_num)
    if Parent[parent_key] is not None:
        u = pydot.Node(str(Parent[parent_key]),
                       label=str(Parent[parent_key][:3]))
        graph.add_node(u)
        v = pydot.Node(str(parent_key),
                       label=str((number_missionaries, number_cannibals, side)))
        graph.add_node(v)
        edge = pydot.Edge(str(Parent[parent_key]),
                          str(parent_key), dir='forward')
        graph.add_edge(edge)
    else:
        v = pydot.Node(str(parent_key),
                       label=str((number_missionaries, number_cannibals, side)))
        graph.add_node(v)
    return u, v

def is_start_state(number_missionaries, number_cannibals, side):
    return (number_missionaries, number_cannibals, side) == (3, 3, 1)

def is_goal_state(number_missionaries, number_cannibals, side):
    return (number_missionaries, number_cannibals, side) == (0, 0, 0)

def number_of_cannibals_exceeds(number_missionaries, number_cannibals):
    number_missionaries_right = 3 - number_missionaries
    number_cannibals_right = 3 - number_cannibals
    return (number_missionaries > 0 and number_cannibals > number_missionaries) \
        or (number_missionaries_right > 0 and number_cannibals_right > number_missionaries_right)

def generate():
    global Parent
    q = deque()
    node_num = 0
    q.append((3, 3, 1, 0, node_num))
    Parent[(3, 3, 1, 0, node_num)] = None

    while q:
        number_missionaries, number_cannibals, side, depth_level, node_num = q.popleft()
        u, v = draw_edge(number_missionaries, number_cannibals, side, depth_level, node_num)
        
        if is_start_state(number_missionaries, number_cannibals, side):
            v.set_fontcolor("white")
        elif is_goal_state(number_missionaries, number_cannibals, side):
            v.set_style("filled")
            v.set_fillcolor("green")
            continue
        elif number_of_cannibals_exceeds(number_missionaries, number_cannibals):
            v.set_style("filled")
            v.set_fillcolor("red")
            continue
        else:
            v.set_style("filled")
            v.set_fillcolor("orange")

        if depth_level == max_depth:
            continue
        
        op = -1 if side == 1 else 1
        can_be_expanded = False
        i = node_num
        for x, y in options:
            next_m, next_c, next_s = number_missionaries + op * x, number_cannibals + op * y, int(not side)
            if Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)] is None or (next_m, next_c, next_s) != Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)][:3]:
                if is_valid_move(next_m, next_c):
                    can_be_expanded = True
                    i += 1
                    q.append((next_m, next_c, next_s, depth_level + 1, i))
                    Parent[(next_m, next_c, next_s, depth_level + 1, i)] = (number_missionaries, number_cannibals, side, depth_level, node_num)

        if not can_be_expanded:
            v.set_style("filled")
            v.set_fillcolor("grey")
    
    return True

if __name__ == "__main__":
    if generate():
        print("Generation complete. Writing image...")
        write_image()
    else:
        print("Failed to generate the state space tree.")
