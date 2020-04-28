#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dwavebinarycsp
from hybrid.reference.kerberos import KerberosSampler


# In[ ]:


import utilities_map


# In[ ]:


class Province:
    def __init__(self, name):
        self.name = name
        self.red = name + "_r" # name of binary variable for red
        self.green = name + "_g" # and so forth
        self.blue = name + "_b"
        self.yellow = name + "_y"


# Provinces in Canada
# AB, BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT

# In[ ]:


ab = Province('ab')
bc = Province('bc')
mb = Province('mb')
nb = Province('nb')
nl = Province('nl')
ns = Province('ns')
nt = Province('nt')
nu = Province('nu')
on = Province('on')
pe = Province('pe')
qc = Province('qc')
sk = Province('sk')
yt = Province('yt')

provinces = [ab, bc, mb, nb, nl, ns, nt, nu, on, pe, qc, sk, yt]


# Borders between provinces:
# 
# AB, BC  
# AB, NT  
# AB, SK  
# BC, NT  
# BC, YT  
# MB, NU  
# MB, ON  
# MB, SK  
# NB, NS  
# NB, QC  
# NL, QC  
# NT, NU  
# NT, SK  
# NT, YT  
# ON, QC

# In[ ]:


neighbours = [
    (ab, bc),
(ab, nt),
(ab, sk),
(bc, nt),
(bc, yt),
(mb, nu),
(mb, on),
(mb, sk),
(nb, ns),
(nb, qc),
(nl, qc),
(nt, nu),
(nt, sk),
(nt, yt),
(on, qc)
]


# In[ ]:


csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)


# In[ ]:


# Each province can only have 1 color !
# For each province, the following configs apply
only_one_color = {(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)}


# In[ ]:


for p in provinces:
    csp.add_constraint(only_one_color, {p.red, p.green, p.blue, p.yellow})


# In[ ]:


not_both = {(0, 0), (0, 1), (1, 0)}


# In[ ]:


for x, y in neighbours:
    csp.add_constraint(not_both, {x.red, y.red})
    csp.add_constraint(not_both, {x.green, y.green})
    csp.add_constraint(not_both, {x.blue, y.blue})
    csp.add_constraint(not_both, {x.yellow, y.yellow})


# In[ ]:


bqm = dwavebinarycsp.stitch(csp)


# In[ ]:


print("Sampling")
#response = sampler.sample(bqm, num_reads=1000)
response = KerberosSampler().sample(bqm)
print("Done")


# In[ ]:


print(response)


# In[ ]:


print(csp.check(response.first.sample))


# In[ ]:


nodes = [p.name for p in provinces]


# In[ ]:


edges = [(p1.name, p2.name) for p1, p2 in neighbours]


# In[ ]:


import networkx as nx

import matplotlib
#matplotlib.use("inline")   # select backend
import matplotlib.pyplot as plt


def visualize_map(nodes, edges, sample, node_positions=None):
    # Set up graph
    G = nx.Graph(edges)

    lone_nodes = set(nodes) - set(G.nodes)  # nodes without edges
    for lone_node in lone_nodes:
        G.add_node(lone_node)

    # Grab the colors selected by sample
    color_labels = [k for k, v in sample.items() if v == 1]

    # Get color order to match that of the graph nodes
    for label in color_labels:
        name, color = label.split("_")
        G.nodes[name]["color"] = color
    color_map = [color for name, color in G.nodes(data="color")]

    # Draw graph
    nx.draw_networkx(G, pos=node_positions, with_labels=True,
                     node_color=color_map, font_color="w", node_size=400)

    plt.show()


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
visualize_map(nodes, edges, response.first.sample)

