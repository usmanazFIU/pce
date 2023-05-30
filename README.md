# Path Computation Element

[![pce-ci-badge]][pce-ci] [![pce-cov-badge]][pce-cov]

Path Computation Element, also called PCE, is a component of
[Atlanticwave SDX][aw-sdx] project.

The problem PCE solves is this: given a network topology and a set of
connection requests that must satisfy some requirements (bandwidth,
latency, number of hops, packet loss,...) how do you find the right
path between nodes?

## Using PCE

PCE's API is still evolving, but in general the usage is like this:

```python
from sdx.pce.load_balancing.te_solver import TESolver
from sdx.pce.topology.temanager import TEManager

temanager = TEManager(initial_topology, connection_request)
for topology in topologies:
    temanager.add_topology(topology)
    
graph = temanager.generate_graph_te()
traffic_matrix = temanager.generate_connection_te()

solution = TESolver(graph, traffic_matrix).solve()
```

The network topology is generated by NetworkX and the traffic matrix
computation is executed by Google OrTools Solver.

## Input

PCE requires two inputs: network topology and connection requests.


### Network Topology

The Network Topology should be in the format of NetworkX graph. For
each link, three attributes need to be assigned: cost, bandwidth and
latency. The current unit of each attribute is abstract, but the unit
in the Network Topology should be consistent with the unit in
Connections.

Currently, the graph is randomly generated by using NetworkX and all
the attributes are randomly assigned based on the users setting.


### Connection Requests

Format of a connection request is in the form of [[Source node,
Destination node, Bandwidth required, Latency required],..].  Here is
an example of a random connection request:

```
[[1,10,8,20],[2,9,10,15],[15,10,6,22]]
```

There are three queries in this connection request.  The first one is
`[1,10,8,20]`, and it means this connection query is to route traffic
from Node 1 to Node 10, requring a bandwith of 8 and maximum latency
of 20.

For testing, a random topology generator and a random connection
request generator is available.


## Working with PCE code

Working with PCE in a virtual environment is a good idea, with a
workflow like this:

```console
$ git clone https://github.com/atlanticwave-sdx/pce.git
$ cd pce
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install .[test]
```

Please note that editable installs does not work currently, due to the
shared top-level `sdx` module in datamodel.

PCE can read topology data from Graphviz dot files, if the optional
pygraphviz dependency is installed with:

```console
$ pip install .[pygraphviz]
```

In order to be able to install pygraphviz, you will also need a C
compiler and development libraries and headers of graphviz installed.


### Running tests

To run tests, using [tox] is recommended:

```console
$ tox
```

With tox, you can run single tests like so:

```console
$ tox -- [-s] tests/test_te_manager.py::TestTEManager::test_generate_solver_input
```

The test that depend on pygraphviz are skipped by default.  If you are
able to install pygraphviz in your setup, you can run that test too
with:

```console
$ tox -e extras
```

Test data is stored in `test/data` as JSON files.


<!-- URLs -->

[aw-sdx]: https://www.atlanticwave-sdx.net/ (Atlanticwave-SDX)

[pce-ci-badge]: https://github.com/atlanticwave-sdx/pce/actions/workflows/test.yml/badge.svg
[pce-ci]: https://github.com/atlanticwave-sdx/pce/actions/workflows/test.yml


[pce-cov-badge]: https://coveralls.io/repos/github/atlanticwave-sdx/pce/badge.svg?branch=main (Coverage Status)
[pce-cov]: https://coveralls.io/github/atlanticwave-sdx/pce?branch=main

[tox]: https://tox.wiki/en/latest/index.html
