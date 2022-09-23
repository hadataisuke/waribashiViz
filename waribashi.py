from graphviz import Digraph
import sys

sys.setrecursionlimit(18000)

class State:
    def __init__(self, is_first, f, s):
        self.is_first = is_first
        self.f = [max(f), min(f)]
        self.s = [max(s), min(s)]
        self.siblings = []
        self.is_drawn = False

    def params(self):
        return (self.is_first, self.f, self.s)

    def __eq__(self, other):
        return self.params() == other.params()

    def __str__(self):
        s = str(self.f) + "\n" + str(self.s)
        if self.is_first:
            return "f\n" + s
        else:
            return "s\n" + s

    def has(self, node):
        return node in self.siblings

    def next_state(self, fi, si):
        d = self.f[fi] + self.s[si]
        f2 = self.f.copy()
        s2 = self.s.copy()
        if d >= 5:
            d = d-5
        if self.is_first:
            s2[si] = d
        else:
            f2[fi] = d
        return State(not self.is_first, f2, s2)
    
    def bunretsu(self,fi,si):
        f2 = self.f.copy()
        s2 = self.s.copy()
        if self.is_first:
            if self.f[1] == 0 and self.f[0]%2 ==0:
                d = self.f[0]/2
                f2 =(d,d)
            elif self.s[1] == 0 and self.s[0]%2 ==0:
                d = self.s[0]/2
                s2 =(d,d)
        return State(not self.is_first, f2, s2)
        
def move(parent, index, is_first, nodes):
    fi, si = index
    if si == -1:        
        child = parent.bunretsu(fi, si)
    elif parent.f[fi] == 0 or parent.s[si] == 0:
        return
    else:
        child = parent.next_state(fi, si)
    if parent.has(child):
        return
    s = str(child)
    child = nodes.get(s, child)
    nodes[s] = child
    parent.siblings.append(child)
    for i in [(0, 0), (0, 1), (1, 0), (1, 1), (-1, -1)]:
        move(child, i, not is_first, nodes)


def make_tree():
    nodes = {}
    root = State(True, [1, 1], [1, 1])
    nodes[str(root)] = root
    move(root, (0, 0), True, nodes)
    return root


def make_graph(node, g):
    if node.is_drawn:
        return
    node.is_drawn = True
    ns = str(node)
    if max(node.f) == 0:
        g.node(ns, color="#FF9999", style="filled")
    elif max(node.s) == 0:
        g.node(ns, color="#9999FF", style="filled")
    else:
        g.node(ns)
    for n in node.siblings:
        g.edge(ns, str(n))
        make_graph(n, g)


def prune(node):
    if max(node.s) == 0:
        return True
    if node.is_first:
        for n in node.siblings:
            if prune(n):
                return True
        return False
    if not node.is_first:
        sib = node.siblings.copy()
        for n in sib:
            if prune(n):
                node.siblings.remove(n)
        if len(node.siblings) == 0:
            return True
    return False


def save(prunning):
    root = make_tree()
    g = Digraph(format="png")
    if prunning:
        prune(root)
        make_graph(root, g)
        g.render("ptree")
    else:
        make_graph(root, g)
        g.render("tree")


#save(True)
save(False)
