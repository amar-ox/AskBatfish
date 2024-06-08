## Introduction to Route Computation and Analysis using Batfish

Network engineers routinely need to validate routing and forwarding in the network. They often do that by connecting to multiple network devices and executing a series of `show route` commands. This distributed debugging is highly complex even in a moderately-sized network. Batfish makes this task extremely simple by providing an easy-to-query, centralized view of routing tables in the network. 

In this notebook, we will look at how you can extract routing information from Batfish.

Check out a video demo of this notebook [here](https://www.youtube.com/watch?v=AutkFa0xUxg).


```python
# Import packages
%run startup.py
bf = Session(host="localhost")
```

### Initializing the Network and Snapshot

`SNAPSHOT_PATH` below can be updated to point to a custom snapshot directory, see the [Batfish instructions](https://github.com/batfish/batfish/wiki/Packaging-snapshots-for-analysis) for how to package data for analysis.<br>
More example networks are available in the [networks](https://github.com/batfish/batfish/tree/master/networks) folder of the Batfish repository.


```python
# Initialize a network and snapshot
NETWORK_NAME = "example_network"
SNAPSHOT_NAME = "example_snapshot"

SNAPSHOT_PATH = "networks/example"

bf.set_network(NETWORK_NAME)
bf.init_snapshot(SNAPSHOT_PATH, name=SNAPSHOT_NAME, overwrite=True)
```




    'example_snapshot'



The network snapshot that we initialized above is illustrated below. You can download/view devices' configuration files [here](https://github.com/batfish/pybatfish/tree/master/jupyter_notebooks/networks/example).

![example-network](https://raw.githubusercontent.com/batfish/pybatfish/master/jupyter_notebooks/networks/example/example-network.png)

All of the information we will show you in this notebook is dynamically computed by Batfish based on the configuration files for the network devices.

### View Routing Tables for ALL devices and ALL VRFs
Batfish makes **all** routing tables in the network easily accessible. Let's take a look at how you can retrieve the specific information you want.


```python
# Get routing tables for all nodes and VRFs
routes_all = bf.q.routes().answer().frame()
```

We are not going to print this table as it has a large number of entries. 

### View Routing Tables for default VRF on AS1 border routers

There are 2 ways that we can get the desired subset of data: 

Option 1) Only request that information from Batfish by passing in parameters into the `routes()` question. This is useful to do when you need to reduce the amount of data being returned, but is limited to regex filtering based on VRF, Node, Protocol and Network.

Option 2) Filter the output of the `routes()` question using the Pandas [APIs](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.filter.html).


```python
?bf.q.routes
```


```python
# Get the routing table for the 'default' VRF on border routers of as1
# using BF parameters
routes_as1border = bf.q.routes(nodes="/as1border/", vrfs="default").answer().frame()
```


```python
# Get the routing table for the 'default' VRF on border routers of as1
# using Pandas filtering
routes_as1border = routes_all[(routes_all['Node'].str.contains('as1border')) & (routes_all['VRF'] == 'default')]
routes_as1border
```



### View BGP learnt routes for default VRF on AS1 border routers


```python
# Getting BGP routes in the routing table for the 'default' VRF on border routers of as1
# using BF parameters
routes_as1border_bgp = bf.q.routes(nodes="/as1border/", vrfs="default", protocols="bgp").answer().frame()
```


```python
# Geting BGP routes in the routing table for the 'default' VRF on border routers of as1
# using Pandas filtering
routes_as1border_bgp = routes_all[(routes_all['Node'].str.contains('as1border')) & (routes_all['VRF'] == 'default') & (routes_all['Protocol'] == 'bgp')]
routes_as1border_bgp
```



### View BGP learnt routes for ALL VRFs on ALL routers with Metric >=50
We cannot pass in `metric` as a parameter to Batfish, so this task is best handled with the Pandas API.


```python
routes_filtered = routes_all[(routes_all['Protocol'] == 'bgp') & (routes_all['Metric'] >= 50)]
routes_filtered
```


### View the routing entries for network 1.0.2.0/24 on ALL routers in ALL VRFs


```python
# grab the route table entry for network 1.0.2.0/24 from all routers in all VRFs
# using BF parameters
routes_filtered = bf.q.routes(network="1.0.2.0/24").answer().frame()
```


```python
# grab the route table entry for network 1.0.2.0/24 from all routers in all VRFs
# using Pandas filtering
routes_filtered = routes_all[routes_all['Network'] == "1.0.2.0/24"]
routes_filtered
```



Using Panda's filtering it is easy to retrieve the list of nodes which have the network in the routing table for at least 1 VRF. This type of processing should always be done using the Pandas APIs.


```python
# Get the list of nodes that have the network 1.0.2.0/24 in at least 1 VRF
# the .unique function removes duplicate entries that would have been returned if the network was in multiple VRFs on a node or there were
# multiple route entries for the network (ECMP)
print(sorted(routes_filtered["Node"].unique()))
```

    ['as1border1', 'as1border2', 'as1core1', 'as2border1', 'as2border2', 'as2core1', 'as2core2', 'as2dept1', 'as2dist1', 'as2dist2', 'as3border1', 'as3border2', 'as3core1']


Now we will retrieve the list of nodes that do NOT have this prefix in their routing table. This is easy to do with the Pandas [groupby](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.groupby.html) and [filter](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.core.groupby.DataFrameGroupBy.filter.html) functions.


```python
# Group all routes by Node and filter for those that don't have '1.0.2.0/24'
routes_filtered = routes_all.groupby('Node').filter(lambda x: all(x['Network'] != '1.0.2.0/24'))

# Get the unique node names and sort the list
print(sorted(routes_filtered["Node"].unique()))
```

    ['host1', 'host2']


The only devices that do not have a route to **1.0.2.0/24** are the 2 hosts in the snapshot. This is expected, as they should just have a default route. Let's verify that.


```python
routes_all[routes_all['Node'].str.contains('host')]
```


With Batfish and Pandas you can easily retrieve the exact information you are looking for from the routing tables on ANY or ALL network devices for ANY or ALL VRFs.

This concludes the notebook. To recap, in this notebook we covered the foundational tasks for route analysis:

1. How to get routes at all nodes in the network or only at a subset of them
2. How to retrieve routing entries that match a specific protocol or metric
3. How to find which nodes have an entry for a prefix or which ones do not


We hope you found this notebook useful and informative. Future notebooks will dive into more advanced topics like path analysis, debugging ACLs and firewall rules, validating routing policy, etc.. so stay tuned! 

### Want to know more? 

Reach out to us through [Slack](https://join.slack.com/t/batfish-org/shared_invite/enQtMzA0Nzg2OTAzNzQ1LTcyYzY3M2Q0NWUyYTRhYjdlM2IzYzRhZGU1NWFlNGU2MzlhNDY3OTJmMDIyMjQzYmRlNjhkMTRjNWIwNTUwNTQ`) or [GitHub](https://github.com/batfish/batfish) to learn more, or send feedback.
