#!/usr/bin/env python3

# example of using graphviz (with python module) to document a modbus flowchart
# sudo apt install python3-graphviz
import graphviz


# node names
API_3 = 'API-3'
API_7 = 'API-7'
API_G1 = 'API-G1'
FLX_DS1 = 'FLX serveur 1'
FLX_DS2 = 'FLX serveur 2'
FLX_PLC = 'FLX-PLC'
FLX_MW_TRA = 'FLX MW Troll A'
FLX_MW_TRB = 'FLX MW Troll B'
FLX_MW_EKA = 'FLX MW Eko A'
FLX_MW_EKB = 'FLX MW Eko B'
FLX_MW_GRA = 'FLX MW Gro A'
FLX_MW_GRB = 'FLX MW Gro B'
PSLS_BLA2 = 'PSLS Blaregnie 2'
PSLS_LAMB = 'PSLS laminage B'
PSLS_LAMH = 'PSLS laminage H'
SUP_CMP = 'Supervision compression'
SUP_CPT = 'Supervision comptage'
ACON_CPT = 'Aconcagua comptage'


# build directed graph (from modbus client to server)
g = graphviz.Digraph('mbus_flow')
g.attr('node', shape='rectangle', style='filled')

# node define
with g.subgraph(name='cluster_cmp') as c:
    c.attr(label='Compression')
    c.node(API_7)
    c.node(SUP_CMP)

with g.subgraph(name='cluster_cpt') as c:
    c.attr(label='Comptage')
    c.node(API_G1)
    c.node(API_3, color='darkorange')
    c.node(ACON_CPT)
    c.node(PSLS_BLA2)
    c.node(PSLS_LAMB)
    c.node(PSLS_LAMH)
    c.node(SUP_CPT)

with g.subgraph(name='cluster_bla') as c:
    c.attr(label='Blaregnies')
    c.node(FLX_DS1, shape='doublecircle')
    c.node(FLX_DS2, shape='doublecircle')
    c.node(FLX_MW_TRA)
    c.node(FLX_MW_TRB)
    c.node(FLX_MW_EKA)
    c.node(FLX_MW_EKB)
    c.node(FLX_MW_GRA)
    c.node(FLX_MW_GRB)
    c.node(FLX_PLC)

# edge define
g.edge(API_3, FLX_DS1, label='FO 1')
g.edge(FLX_DS1, FLX_MW_TRA)
g.edge(FLX_DS1, FLX_MW_TRB)
g.edge(FLX_DS1, FLX_MW_EKA)
g.edge(FLX_DS1, FLX_MW_EKB)
g.edge(FLX_DS1, FLX_MW_GRA)
g.edge(FLX_DS1, FLX_MW_GRB)
g.edge(API_3, FLX_DS2, label='FO 2')
g.edge(FLX_DS2, FLX_MW_TRA)
g.edge(FLX_DS2, FLX_MW_TRB)
g.edge(FLX_DS2, FLX_MW_EKA)
g.edge(FLX_DS2, FLX_MW_EKB)
g.edge(FLX_DS2, FLX_MW_GRA)
g.edge(FLX_DS2, FLX_MW_GRB)
g.edge(API_3, FLX_PLC, label='FO 3')
g.edge(API_3, ACON_CPT)
g.edge(API_3, API_G1)
g.edge(PSLS_BLA2, API_3)
g.edge(PSLS_LAMB, API_3)
g.edge(PSLS_LAMH, API_3)
g.edge(SUP_CMP, API_3)
g.edge(SUP_CPT, API_3)
g.edge(API_7, API_3, label='30p')
g.edge(API_7, API_3, label='GIN')
# build
g.view()
