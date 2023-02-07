# PCE
## Run with python

### Input
Input includes two main parts: Network Topology and Connections\
\
Both input json file is stored under `./tests/data`
#### Network Topology
%The connection will be a list of list stored in /test/data/connection.json.
\
The Network Topology should be generated in the format of NetworkX graph. For each link, three attributes need to be assigned: cost, bandwidth and latency. The current unit of each attribute is abstract, but the unit in the Network Topology should be consistent with the unit in Connections.\
\
Currently, the graph is randomly generated by using NetworkX and all the attributes are randomly assigned based on the users setting. 
#### Connection
The connection will be a list of list stored in `./tests/data/connection.json`. \
\
The format of the input connection is `[Source node, Destination node, Bandwidth required, Latency required]`.  \
Here is an example of a random connection.json:
```
[[1,10,8,20],[2,9,10,15],[15,10,6,22]]
```
There are three queries in this connection.json, the first one is `[1,10,15,20]`.\
It means this connection query is to route traffic from Node 1 to Node 10, requring a bandwith of 8 and maximum latency of 20.\
\
For testing, a random connection generator is located at `Utility/RandomConnectionGen.py`. It can randomly generate one or multiple queries in one connection.json.

### Connection Generation (use bullet just for random generation)
Random connection generator is located at Utility/RandomConnectionGen.py. 
```
RandomConnectionGenerator(nodes, querynum, bw, latencylimit)
```
This will randomly generate one or multiple queries in one connection.json stored in `tests/data/connection.json`. 
### Where to Input
Connection is called at the beginning of lbnxgraphgenerator() using GetConnection() in `/LoadBalancing/RandomTopologyGenerator`
\

g will be the input NetworkX format topology. The current random topology is get from GetNetworkToplogy() .

### Output
To get the optimal path and related objective value:
#### MC_Solver (how I split the function and call the input)
For Minimizing the total path cost, do `from LoadBalancing.MC_Solver import runMC_Solver`:
```
runMC_Solver()
```
This will output a tuple of 2 elements: (Path List Dict, Total Cost).\
For example, using the previous connection.json, the output will be:
```
({1: [[1, 13], [13, 19], [19, 8], [8, 2], [2, 10]], 2: [[2, 10], [10, 9]], 3: [[15, 10]]}, 27401516.0)
```
The first element is a dict which has the connection# as key and path list as value, for the first connection, the traffic will be routed from Node 1 to Node 10, the path will be 1->13->19->8->2->10, and the total cost for applying all the three connections will be 27401516 in total.\

#### LB_Solver
For Minimizing the total path utilization, do `from LoadBalancing.LB_Utilization_Solver import runLB_UT_Solver`:
```
runLB_UT_Solver()
```
This will output a tuple of 2 elements: (Path List Dict, Total Utilization).\
Still using the previous connection.json, this time output will be:
```
({1: [[1, 14], [14, 10]], 2: [[2, 9]], 3: [[15, 10]]}, 0.08040263457045238)
```
The first element is same as in MC_Solver, but the second element will be the total utilization of all links which is around 0.08.


## Working with PCE code

The network topology is generated by NetworkX and the traffic matrix
computation is executed by Google OrTools Solver. 

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
$ tox -- [-s] ests/test_te_manager.py::TestTEManager::test_generate_solver_input
```

The test that depend on pygraphviz are skipped by default.  If you are
able to install pygraphviz in your setup, you can run that test too
with:

```console
$ tox -e extras
```

Test data is stored in `test/data` as JSON files.  You might want to
be in the top-level directory when running tests.

<!-- URLS -->

[tox]: https://tox.wiki/en/latest/index.html
