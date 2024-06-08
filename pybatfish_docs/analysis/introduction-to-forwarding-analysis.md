# Introduction to Forwarding Analysis using Batfish

Analyzing how the network forwards packets is one of the most common tasks for network engineers. Typically, it is performed by running `traceroute` between multiple sources and destinations. This process is highly complex even in a moderately-sized network. It also fails to provide strong assurance as only some of the source-destination pairs and some of the packets can be feasibly tested.  

Batfish makes forwarding analysis extremely simple by providing 1) easy-to-use queries over a centralized view of the network; and 2) ability to reason comprehensively about entire spaces of flows. Further,  it can perform this analysis proactively, that is, analyze the impact of configuration changes *before* they are pushed to the network. 

In this notebook, we will show you how to perform forwarding analysis with Batfish.

Check out a video demo of this notebook [here](https://youtu.be/yaJBH3ZZ5Dw).


```python
# Import packages
%run startup.py
bf = Session(host="localhost")
```

## Setup: Initializing the Network and Snapshot

`SNAPSHOT_PATH` below can be updated to point to a custom snapshot directory. See the [Batfish instructions](https://github.com/batfish/batfish/wiki/Packaging-snapshots-for-analysis) for how to package data for analysis.

More example networks are available in the [networks](https://github.com/batfish/batfish/tree/master/networks) folder of the Batfish repository.


```python
NETWORK_NAME = "example_network"
SNAPSHOT_NAME = "example_snapshot"

SNAPSHOT_PATH = "networks/example"

bf.set_network(NETWORK_NAME)
bf.init_snapshot(SNAPSHOT_PATH, name=SNAPSHOT_NAME, overwrite=True)
```




    'example_snapshot'



The network snapshot that we initialized above is illustrated below. You can view or download the devices' configuration files [here](https://github.com/batfish/pybatfish/tree/master/jupyter_notebooks/networks/example).

![example-network](https://raw.githubusercontent.com/batfish/pybatfish/master/jupyter_notebooks/networks/example/example-network.png)

All of the information we will show you in this notebook is dynamically computed by Batfish based on the configuration files for the network devices.

---



## Batfish Smart Traceroute: Detailed analysis of path(s) of a flow

In this section, we will use the [traceroute question](https://pybatfish.readthedocs.io/en/latest/notebooks/forwarding.html#Traceroute) to find the path taken by AS3 core routers to reach the DNS Server (`host1`) in AS2. Traceroute has three (composite) parameters that you can specify, allowing for a variety of queries. We will focus on the two main ones:

* `startLocation` - where in the network the flow starts
* `headers` - [packet headers](https://pybatfish.readthedocs.io/en/latest/datamodel.html#pybatfish.datamodel.flow.HeaderConstraints) for the flow you are interested in tracing. This is **not** just limited to UDP or ICMP.

We want the trace to start from the `Loopback0` interface on `as3core1`, and we want to use the IP address of that interface as the source address. For this we set the `startLocation` to `as3core1[Loopback0]`. Batfish automatically chooses the IP address of `Loopback0` as the source IP.

We set the destination IP address of our virtual packet by specifying `dstIps='ofLocation(host1)'`. Batfish will automatically pick *one of the* IP addresses for `host1` as the destination IP address.  See the `ofLocation` function (see [documentation](https://github.com/batfish/batfish/blob/master/questions/Parameters.md#ip-specifier) for more detail).

To run the query:


```python
# start the traceroute from the Loopback0 interface of as3core1 to host1
headers = HeaderConstraints(dstIps='host1')
tracert = bf.q.traceroute(startLocation="as3core1[Loopback0]", headers=headers).answer().frame()
```

To pretty-print the traces in HTML use the `display_html` function. We will show you how to extract more detailed information below.


```python
show(tracert)
```

The `Flow` column describes the packet being traced: it starts at `as3core1` using source IP  `3.10.1.1` (of `Loopback0`) and and destination IP `2.128.0.101`. By default, `bf.q.traceroute` uses the standard UDP traceroute to destination port `33434`, and Batfish arbitrarily picks the lowest ephemeral source port of  `49152`.


```python
tracert['Flow'][0]
```


Start Location: as3core1<br>Src IP: 3.10.1.1<br>Src Port: 49152<br>Dst IP: 2.128.0.101<br>Dst Port: 33434<br>IP Protocol: UDP



The `Trace` column contains the detailed information provided by Batfish about the paths through the network for each flow. Let's look in detail on the first path:


```python
tracert['Traces'][0][0]  # Get the trace for the first path of the first flow
```


This flow starts at `as3core1` and crosses from AS3 into AS2 via the border routers `as3border1` and `as2border2`; on `as2border2`, the flow is permitted by the inbound ACL `OUTSIDE_TO_INSIDE`. Once inside AS2, the flow is forwarded through AS2's core and distribution servers to the department router. The flow does reach `host1`, but is blocked by that server iptables rule `filter::INPUT` on `eth0`.

The `TraceCount` column reports the total number of paths for each flow. In this example, the count `4` matches the four paths we saw in the `Traces` column. These are all the best-cost paths inside AS2 -- the flow can go through either `as2core1` or `as2core2` and either `as2dist1` or `as2dist2`.

<small>Detail: `TraceCount` may not always match the `TracesColumn`: in networks with high ECMP, there may be hundreds or even thousands of traces even for a single flow, in which case the `Traces` column will produce fewer results.</small>


```python
tracert['TraceCount'][0]
```


To programmatically get the _detailed_ information about the final hop of the first trace in pure Python form:


```python
last_hop = tracert['Traces'][0][0].hops[-1]
repr(last_hop)
```


Note that compared to running traceroute on a router, **Batfish is able to provide much more detail about the trace**:

1. All active parallel paths between the source and destination
1. The reason why each hop in a path is taken (the specific routing entry that was matched)
1. All processing steps inside each hop on the path
1. All interfaces visited and filters encountered during the trace
1. The disposition of the flow for each path

## Batfish Reachability: Search for forwarding behaviors in (large) spaces of flows

Batfish's smart traceroute provides detailed information about all paths taken by a specified flow through the network, which is a powerful capability for exploring and testing network behavior. However, network engineers often need information about some *type* of flow, without being able to specify a particular flow of that type. For example, we may want to know what TCP flows can (or cannot) reach a particular host. In other words, we want to search within the (huge!) space of TCP flows addressed to that host. Batfish's
[reachability question](https://pybatfish.readthedocs.io/en/latest/notebooks/forwarding.html#Reachability) 
is an easy and efficient way to perform exactly this kind of search.

### Example 1: Search for DNS flows that reach the DNS server
Continuing with our running example, let's search for DNS flows within AS2 that reach our DNS server `host1`.  The parameter `srcIps='0.0.0.0/0'` tells Batfish to search within the entire space of source IP addresses. 

<small>Detail: In traceroute `ofLocation(host1)` specified a single IP address of `host1` (chosen arbitrarily). In reachability, it specifies to search over *all* IP addresses of `host1`.</small>


```python
path = PathConstraints(startLocation="/as2/")
headers = HeaderConstraints(srcIps="0.0.0.0/0", dstIps="host1", applications="DNS")
reach = bf.q.reachability(pathConstraints=path, headers=headers, actions="success").answer().frame()
show(reach)
```


As you can see, this query found *some* DNS flow entering the network at *each* `as2...` node destined for `host1` that would be delivered. This guarantees that DNS is at least partially available (some authorized nodes can reach `host1`). 

## Using Batfish Reachability as a verification tool

Batfish's reachability analysis performs an *exhaustive* search, considering every possible flow. This makes it a very powerful tool for finding bugs, and when no bugs are found, it provides **strong guarantees** about the network behavior. It allows you to **verify** essential network properties like availability or security (i.e., presence or absence of reachability). In the following examples shows we'll use reachability to verify the intended availability and security properties of our DNS server.

### Example 2: Verify that the DNS server is available *everywhere* inside AS2 
To verify DNS is available inside of AS2, we search for flows that would demonstrate a lack of availability -- i.e. DNS flows to `host1` that would **fail** to be delivered.  Our intent in this case is that no such flows should exist in the network, and this is where we see the power of exhaustive search. If Batfish does not find any dropped DNS flows to `host1`,  we have **verified** availability. 




```python
path = PathConstraints(startLocation="/as2/")
headers = HeaderConstraints(dstIps="host1", applications="DNS")
reach = bf.q.reachability(pathConstraints=path, headers=headers, actions="failure").answer().frame()
show(reach)
```


The fact that Batfish returned 0 flows guarantees that `host1` is reachable via DNS from everywhere within AS2. This guarantees that DNS is available to all authorized nodes.

### Example 3: No UDP traffic except DNS is accessible on host1
Next, let's verify a security property: that no UDP traffic other than DNS will reach `host1`. We do this by searching for any UDP flows **accepted** by `host1` that are **not DNS**:


```python
path = PathConstraints(startLocation="/as2/")
headers = HeaderConstraints(srcIps="0.0.0.0/0", dstIps="host1", ipProtocols="UDP", dstPorts="!53")
reach = bf.q.reachability(pathConstraints=path, headers=headers, actions="accepted").answer().frame()
show(reach)
```



Success! Since Batfish returned 0 flows, we are guaranteed that no unauthorized UDP flows will reach `host1`.

### Example 4: Verify that the DNS server is not reachable from *anywhere* outside AS2 
Next, let's verify that no DNS traffic from *outside* of AS2 can reach `host1`. We can do this by searching for flows starting from the border interfaces (`GigabitEthernet0/0` on AS2 border routers).

<small>_Details_: We use the [enter function](https://github.com/batfish/batfish/blob/master/questions/Parameters.md#interface-specifier) to model that traffic is received on the interface rather than starting from a border router. If we did not relax source IP to `0.0.0.0/0`, only source IP addresses within the connected subnet of the border interfaces would be included in the search.</small>


```python
path = PathConstraints(startLocation="@enter(/as2border/[GigabitEthernet0/0])")
headers = HeaderConstraints(srcIps="0.0.0.0/0", dstIps="host1", applications="DNS")
reach = bf.q.reachability(pathConstraints=path, headers=headers, actions="success").answer().frame()
show(reach)
```



We found that the DNS server is **not** secure: external DNS traffic can reach `host1`! However, we did find where to look: in all likelihood, the `OUTSIDE_TO_INSIDE` ACL on the border router should be blocking more DNS traffic.

## Multipath Consistency: Verify consistent treatment of a flow across all paths

Finally, we will demonstrate an **experimental** feature to detect an important class of reachability bugs in any network with *no* user input: the `multipathconsistency` check. This question will report find flows with multipath routing where some paths reach the destination and some paths fail. Multipath inconsistencies are almost always bugs, and may be a sign that the network is not robust to failures.

In this example network there are mutiple multipath consistencies; for conciseness we show only the first result.


```python
multipath = bf.q.multipathConsistency().answer().frame()
first_result = multipath.head(1)  # this check returns many results, just show 1
show(first_result)
```


The above trace shows that traffic from `as2core2` to `as2core1` can take four paths: through either of the two border routers or through either distribution router. However, telnet traffic will be blocked for only two of these four paths: the ones that traverse the distribution layer.



## Wrap-up

This concludes the notebook. To recap, we covered the foundational tasks for path analysis:

1. We performed a traceroute to check connectivity to `host1`
2. Analyzed detailed path & hop information for the traceroute
3. Explored a space of flows with the reachablity question and found an ACL bug that allows some external clients to reach the DNS server
4. Perfomed a security check that ensures that only SSH and DNS traffic can reach `host1`
5. Found multipath inconsistency in the network, for which only some paths result in successful communication

We hope you found this notebook useful and informative. Future notebooks will dive into more advanced topics ensuring planned configuration changes do not have unintended consequences. Stay tuned!

### Want to learn more? 

Reach out to us through [Slack](https://join.slack.com/t/batfish-org/shared_invite/enQtMzA0Nzg2OTAzNzQ1LTcyYzY3M2Q0NWUyYTRhYjdlM2IzYzRhZGU1NWFlNGU2MzlhNDY3OTJmMDIyMjQzYmRlNjhkMTRjNWIwNTUwNTQ) or [GitHub](https://github.com/batfish/batfish) to learn more, or send feedback.
