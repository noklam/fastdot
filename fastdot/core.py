# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['pydot', 'Dot', 'uniq_name', 'quote', 'graph_objects', 'object_names', 'add_mapping', 'node_defaults',
           'Node', 'object2graph', 'obj2node_color', 'graph_colors1', 'graph_colors2', 'cluster_defaults', 'Cluster',
           'graph_items', 'object_connections', 'graph_edges_seq', 'seq_cluster', 'Point', 'is_listy']

# Cell
from fastcore.all import *
import pydot, matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex, hex2color
from uuid import uuid4
from typing import Collection

# Cell
#nbdev_comment _all_ = ['pydot']

# Cell
def Dot(defaults=None, rankdir='LR', directed=True, compound=True, **kwargs):
    "Create a `pydot.Dot` graph with fastai/fastdot style defaults"
    return pydot.Dot(rankdir=rankdir, directed=directed, compound=compound, **kwargs)

# Cell
def uniq_name(o): return 'n'+(uuid4().hex)

def quote(x, q='"'):
    'Surround `x` with `"`'
    return f'"{x}"'

@patch
def _repr_svg_(self:pydot.Dot):
    return self.create_svg().decode('utf-8')

# Cell
graph_objects = {}
object_names = {}

# Cell
def add_mapping(graph_item, obj):
    graph_objects[graph_item.get_name()] = graph_item
    object_names[id(obj)] = graph_item.get_name()
    return graph_item

# Cell
def _pydot_create(f, obj, **kwargs):
    for k,v in kwargs.items():
        if callable(v): v = kwargs[k] = v(obj)
        if k not in ('name','graph_name'): kwargs[k] = quote(v)
    return add_mapping(f(**kwargs), obj)

# Cell
node_defaults = dict(label=str, tooltip=str, name=uniq_name, shape='box', style='rounded, filled', fillcolor='white')

# Cell
def Node(obj, **kwargs):
    "Create a `pydot.Node` with a unique name"
    if not isinstance(obj,str) and isinstance(obj, Collection) and len(obj)==2:
        obj,kwargs['tooltip'] = obj
    kwargs = merge(node_defaults, kwargs)
    return _pydot_create(pydot.Node, obj, **kwargs)

# Cell
def object2graph(o):
    "Get graph item representing `o`"
    return graph_objects[object_names[id(o)]]

# Cell
def obj2node_color(cm, minalpha, rangealpha, o):
    "Create a consistent mapping from objects to colors, using colormap `cm`"
    h = hash(o)
    i = float(h % 256) / 256
    alpha = (h^hash('something')) % rangealpha + minalpha
    return rgb2hex(cm(i)) + f'{alpha:02X}'

# Cell
graph_colors1 = partial(obj2node_color, plt.get_cmap('rainbow'), 30, 160)
graph_colors2 = partial(obj2node_color, plt.get_cmap('tab20'), 30, 160)

# Cell
node_defaults['fillcolor'] = graph_colors1

# Cell
cluster_defaults = dict(label=str, tooltip=str, graph_name=uniq_name, style='rounded, filled', fillcolor='#55555522')

# Cell
def Cluster(obj='', **kwargs):
    "Create a `pydot.Cluster` with a unique name"
    kwargs = merge(cluster_defaults, kwargs)
    return _pydot_create(pydot.Cluster, obj, **kwargs)

# Cell
@patch
def nodes(self:pydot.Graph):
    "`i`th node in `Graph`"
    return L(o for o in self.get_nodes() if o.get_label() is not None)

# Cell
@patch
def __getitem__(self:pydot.Graph, i):
    "`i`th node in `Graph`"
    return self.nodes()[i]

# Cell
@patch
def add_item(self:pydot.Graph, item, **kwargs):
    "Add a `Cluster`, `Node`, or `Edge` to the `Graph`"
    if not isinstance(item, (pydot.Edge,pydot.Node,pydot.Graph)): item = Node(item, **kwargs)
    f = self.add_node     if isinstance(item, pydot.Node ) else \
        self.add_subgraph if isinstance(item, pydot.Graph) else \
        self.add_edge     if isinstance(item, pydot.Edge ) else None
    f(item)
    return item

# Cell
@patch
def add_items(self:pydot.Graph, *items, **kwargs):
    "Add `items` the `Graph`"
    return L(self.add_item(it, **kwargs) for it in items)

# Cell
def graph_items(*items, **kwargs):
    "Add `items` to a new `pydot.Dot`"
    g = Dot()
    g.add_items(*items, **kwargs)
    return g

# Cell
@patch
def first(self:pydot.Graph):
    "First node in `Graph`, searching subgraphs recursively as needed"
    nodes = self.nodes()
    if nodes: return nodes[0]
    for subg in self.get_subgraphs():
        res = subg.first()
        if res: return res

# Cell
@patch
def last(self:pydot.Graph):
    "Lastt node in `Graph`, searching subgraphs recursively as needed"
    nodes = self.nodes()
    if nodes: return nodes[-1]
    for subg in reversed(self.get_subgraphs()):
        res = subg.last()
        if res: return res

# Cell
@patch
def with_compass(self:(pydot.Node,pydot.Graph), compass=None):
    r = self.get_name()
    return f'{r}:{compass}' if compass else r

# Cell
@patch
def connect(self:(pydot.Node,pydot.Graph), item, compass1=None, compass2=None, **kwargs):
    "Connect two nodes or clusters"
    a,b,ltail,lhead = self,item,'',''
    if isinstance(self,pydot.Graph):
        a = self.last()
        ltail=self.get_name()
    if isinstance(item,pydot.Graph):
        b = item.first()
        lhead=item.get_name()
    a,b = a.with_compass(compass1),b.with_compass(compass2)
    return pydot.Edge(a, b, lhead=lhead, ltail=ltail, **kwargs)

# Cell
def object_connections(conns):
    "Create connections between all pairs in `conns`"
    return [object2graph(a).connect(object2graph(b)) for a,b in conns]

# Cell
def graph_edges_seq(items):
    "Add edges between each pair of nodes in `items`"
    return L(items[i].connect(items[i+1]) for i in range(len(items)-1))

# Cell
@patch
def add_edges_seq(self:pydot.Graph, items):
    "Add edges between each pair of nodes in `items`"
    return self.add_items(*graph_edges_seq(items))

# Cell
def seq_cluster(items, cluster_label='', **kwargs):
    sg = Cluster(cluster_label)
    its = sg.add_items(*items, **kwargs)
    sg.add_edges_seq(its)
    return sg

# Cell
def Point(label='pnt', **kwargs):
    "Create a `Node` with a 'point' shape"
    return (Node('pnt', shape='point'))

# Cell
@patch
def __add__(self:pydot.Graph, item, **kwargs):
    "Add a `Cluster`, `Node`, or `Edge` to the `Graph` with operator"
    # if not is_listy(item):
    #     item = L(item)
    if not is_listy(item):
        return self.add_item(item, **kwargs)
    else:
        return self.add_items( *item, **kwargs)

@patch
def __rshift__(self:(pydot.Node,pydot.Graph), item, compass1=None, compass2=None, **kwargs):
    return self.connect(item, compass1, compass2, **kwargs)


def is_listy(x)->bool:
    return isinstance(x, (tuple,list))