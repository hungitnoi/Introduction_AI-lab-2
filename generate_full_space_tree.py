from collections import deque
import pydot
import argparse
import os

# Set PATH to the bin folder of Graphviz
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin'
options = [(1, 0), (0, 1), (1, 1), (0, 2), (2, 0)]
Parent = dict()

graph = pydot.Dot(graph_type='graph', strict=False, bgcolor="fff3af",
                  label="fig : missionaries and cannibal state space tree",
                  fontcolor="red", fontsize="24", overlap="true")
# to track node
i = 0

# Command-line argument parsing
arg = argparse.ArgumentParser()
arg.add_argument("-d", "--depth", type=int, default=20,
                 help="Max depth up to which you want to generate space state tree")
args = arg.parse_args()

# This will correctly fetch the max_depth as an integer
max_depth = args.depth


def is_Valid_Move(number_missionaries, number_cannibals):
    return (0 <= number_missionaries <= 3) and (0 <= number_cannibals <= 3)


def write_image(file_name="state_space"):
    try:
        graph.write_png(file_name + ".png")
    except Exception as e:
        print("Error in writing file", e)
    else:
        print(f"File {file_name}_{max_depth}.png is written successfully")


def draw_edge(number_missionaries, number_cannibals, side, depth_level, node_num):
    u, v = None, None
    if Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)] is not None:
        u = pydot.Node(str(Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)]),
                       label=str(Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)][:3]))
        graph.add_node(u)
        v = pydot.Node(str((number_missionaries, number_cannibals, side, depth_level, node_num)),
                       label=str((number_missionaries, number_cannibals, side)))
        graph.add_node(v)

        edge = pydot.Edge(str(Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)]),
                          str((number_missionaries, number_cannibals, side, depth_level, node_num)), dir='forward')
        graph.add_edge(edge)

    else:
        v = pydot.Node(str((number_missionaries, number_cannibals, side, depth_level, node_num)),
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
    return (number_missionaries > 0 and number_missionaries < number_cannibals) \
           or (number_missionaries_right > 0 and number_missionaries_right < number_cannibals_right)


def generate():
    global i
    q = deque()
    node_num = 0
    q.append((3, 3, 1, 0, node_num))
    Parent[(3, 3, 1, 0, node_num)] = None

    while q:
        number_missionaries, number_cannibals, side, depth_level, node_num = q.popleft()
        u, v = draw_edge(number_missionaries, number_cannibals, side, depth_level, node_num)

        if is_goal_state(number_missionaries, number_cannibals, side):
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
            return True

        op = -1 if side == 1 else 1
        can_be_expanded = False

        for x, y in options:
            next_m, next_c, next_side = number_missionaries + op * x, number_cannibals + op * y, int(not side)
            if Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)] is None or \
                    (next_m, next_c, next_side, depth_level + 1, i) != Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)][:3]:
                if is_Valid_Move(next_m, next_c):
                    can_be_expanded = True
                    i += 1
                    q.append((next_m, next_c, next_side, depth_level + 1, i))
                    Parent[(next_m, next_c, next_side, depth_level + 1, i)] = \
                        (number_missionaries, number_cannibals, side, depth_level, node_num)
        if not can_be_expanded:
            v.set_style("filled")
            v.set_fillcolor("gray")
    return False


if __name__ == "__main__":
    if generate():
        write_image()
