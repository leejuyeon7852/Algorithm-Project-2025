def clean(n):
    return n.split("(")[0]

def line_of(n):
    return n.split("(")[1].replace(")", "")

def is_transfer(u, v):
    return clean(u) == clean(v) and line_of(u) != line_of(v)

def find_all_nodes(G, name):
    return [n for n in G.nodes() if n.startswith(f"{name}(")]

def pretty(path):
    out = []
    for i in range(len(path)):
        out.append(f"{clean(path[i])}({line_of(path[i])})")
        if i < len(path) - 1 and clean(path[i]) == clean(path[i+1]):
            out.append(" ↳ [환승]")
    return "\n → ".join(out)

def station_exists(G, name):
    return any(n.startswith(f"{name}(") for n in G.nodes())
