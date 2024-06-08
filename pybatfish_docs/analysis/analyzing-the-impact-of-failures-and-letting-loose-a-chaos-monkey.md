# Analyzing the Impact of Failures (and letting loose a Chaos Monkey)


## Initialization

We will use the example network shown below with three autonomous systems (ASes) spread that connect via eBGP. Within each AS  iBGP and OSPF is used. The configurations of these devices are available [here](https://github.com/batfish/pybatfish/tree/master/jupyter_notebooks/networks/failure-analysis).

![example-network](https://raw.githubusercontent.com/batfish/pybatfish/master/jupyter_notebooks/networks/failure-analysis/failure-network.png)

***


```python
# Import packages
%run startup.py
bf = Session(host="localhost")

# Initialize the example network and snapshot
NETWORK_NAME = "example_network"
BASE_SNAPSHOT_NAME = "base"

SNAPSHOT_PATH = "networks/failure-analysis"

bf.set_network(NETWORK_NAME)
bf.init_snapshot(SNAPSHOT_PATH, name=BASE_SNAPSHOT_NAME, overwrite=True)
```




    'base'



## `bf.fork_snapshot`: Simulating network failures
To simulate network failures, Batfish offers a simple API `bf.fork_snapshot` that clones the original snapshot to a new one with the specified failure scenarios.

Suppose we want to analyze the scenario where node `London` fails. We can use `bf.fork_snapshot` to simulate this failure as shown below.


```python
# Fork a new snapshot with London deactivated
FAIL_LONDON_SNAPSHOT_NAME = "fail_london"
bf.fork_snapshot(BASE_SNAPSHOT_NAME, FAIL_LONDON_SNAPSHOT_NAME, deactivate_nodes=["london"], overwrite=True)
```




    'fail_london'



In the code, `bf.fork_snapshot` accepts four parameters: `BASE_SNAPSHOT_NAME` indicates the original snapshot name, `FAIL_LONDON_SNAPSHOT_NAME` is the name of the new snapshot, `deactivate_nodes` is a list of nodes that we wish to fail, and `overwrite=True` indicates that we want to reinitialize the snapshot if it already exists.

In addition to `deactivate_nodes`, `bf.fork_snapshot` can also take `deactivate_interfaces` as a parameter to simulate interface failures. Combining these functions, Batfish allows us to simulate complicated failure scenarios involving interfaces and nodes, for example: `bf.fork_snapshot(BASE_SNAPSHOT_NAME, FAIL_SNAPSHOT_NAME, deactivate_nodes=FAIL_NODES, deactivate_interfaces=FAIL_INTERFACES, overwrite=True))`.

To understand network behavior under the simulated failure, we can run any Batfish question on the newly created snapshot.  As an example, to ensure that the flows from `Paris` would still reach `PoP` even if `London` failed, we can run the traceroute question on the snapshot in which London has failed, as shown below. (See the [Introduction to Forwarding Analysis using Batfish](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/Introduction%20to%20Forwarding%20Analysis.ipynb) notebook for more forwarding analysis questions).


```python
# Get the answer of a traceroute question from Paris to the PoP's prefix
pop_prefix = "2.128.0.0/24"
tr_answer = bf.q.traceroute(
    startLocation="paris",
    headers=HeaderConstraints(dstIps=pop_prefix),
    maxTraces=1
).answer(FAIL_LONDON_SNAPSHOT_NAME)

# Display the result in a pretty form
show(tr_answer.frame())
```

Great! We have confirmed that `Paris` can still reach `PoP` via `Asia` even when `London` has failed. 

## `differentialReachability`: Checking changes of forwarding behavior for *all* flows

Above, we saw how Batfish can create new snapshots that simulate failure scenarios and run analysis on them. This capability is useful to *test* the forwarding behavior under interesting failure scenarios. In some cases, we may also want to *verify* that certain network failures have no impact to the network, i.e., the forwarding behavior of *all* flows would not be changed by those failures. 

We now show a powerful question `differentialReachability` of Batfish, which allows us to analyze changes of *any* flow between two snapshots. This question will report any flow that was successfully delivered in the base snapshot but will not be delivered in failure snapshot or the other way around---not delivered in the base snapshot but delivered in the failure snapshot. 

Let us revisit the scenario where `London` fails. To understand if this failure impacts any flow to the PoP in the `US`, we can run the differential reachability question as below, by scoping the search to flows destined to the `PoP`(from anywhere) and comparing `FAIL_LONDON_SNAPSHOT_NAME` with `BASE_SNAPSHOT_NAME` as the reference. Leaving the headers field unscoped would search across flows to all possible destinations. 


```python
# Get the answer to the differential reachability question given two snapshots
diff_reachability_answer = bf.q.differentialReachability(
    headers=HeaderConstraints(dstIps=pop_prefix), maxTraces=1).answer(
    snapshot=FAIL_LONDON_SNAPSHOT_NAME,
    reference_snapshot=BASE_SNAPSHOT_NAME)

# Display the results
show(diff_reachability_answer.frame())
```

We see from the result that the failures of `London` would in fact permit a flow that was originally being blocked by the `AS1_TO_AS2` ACL on `New York`. This difference reveals a potential security vulnerability! Luckily, Batfish allows us to catch and fix it before something bad happens in production. Similarly, if there were flows that were carried in `BASE_SNAPSHOT_NAME` but dropped in `FAIL_LONDON_SNAPSHOT_NAME` (an availability issue), Batfish would have caught it.  

Check out our [Introduction to Forwarding Change Validation](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/Introduction%20to%20Forwarding%20Change%20Validation.ipynb) notebook for more use cases of differential reachability queries.

## Chaos Monkey Testing

Chaos Monkey style testing is a common method to to build highly reliable software systems. In it, different components of the system are randomly failed to see what impact it has on the service performance. Such testing is known to be highly effective but is not possible to do in the networking context. Until now.

Batfish can easily enable Chaos Monkey testing for networks. Using the basic functions shown above, we can compose more complicated functions that randomly fail links and identify potential vulnerabilities in the network. 

Suppose we wanted our network to be robust to any possible 2-link failures. The example below shows how to perform Chaos Monkey testing to identify 2-link-failures that can cause an outage. Specifically, we will fail a pair of links picked at random and check whether the forwarding behavior would be changed by the failure using the `differentialReachability` question. 

Next, we run Chaos Monkey testing, shown as below.


```python
# Fix for demonstration purpose
random.seed(0)

max_iterations = 5

# Get all links in the network
links = bf.q.edges().answer(BASE_SNAPSHOT_NAME).frame()

for i in range(max_iterations):
    # Get two links at random
    failed_link1_index = random.randint(0, len(links) - 1)
    failed_link2_index = random.randint(0, len(links) - 1)

    # Fork a snapshot with the link failures
    FAIL_SNAPSHOT_NAME = "fail_snapshot"
    bf.fork_snapshot(
        BASE_SNAPSHOT_NAME,
        FAIL_SNAPSHOT_NAME,
        deactivate_interfaces=[links.loc[failed_link1_index].Interface,
                               links.loc[failed_link2_index].Interface],
        overwrite=True)

    # Run a differential reachability question
    answer = bf.q.differentialReachability(
        headers=HeaderConstraints(dstIps=pop_prefix)
    ).answer(
        snapshot=FAIL_SNAPSHOT_NAME,
        reference_snapshot=BASE_SNAPSHOT_NAME
    )

    # A non-empty returned answer means changed forwarding behavior
    # We print the bad failure scenario and exit
    if len(answer.frame()) > 0:
        show(links.iloc[[failed_link1_index, failed_link2_index]])
        break
```

We see that there is a failure scenario under to which the network is not robust, that is, the failure will lead to a change in the forwarding behavior of at least some flows.  This scenario is the failure of two links that connect `Seattle` to `Philadelphia` and `San Francisco`. This is unexpected because `Seattle` has another link that connects it to the rest of the network and should generally be available for traffic. 

Let us diagnose this situation to understand the problem. To begin, we first see which flows are impacted. 


```python
show(answer.frame())
```

We see that when the links fail,  if we ignore flows that end in `Seattle` (whose links have failed), a general pattern is that `Asia` loses connectivity to `US`. Given the network topology, this is quite surprising because after those failure we would have expected `Asia` to be able to reach `US` via `Europe`. 

To investigate further into the root cause, we ask Batfish to show how the BGP RIB in the two cases differ. We do so using the `bgpRib` question and comparing the two snapshots as in the differential reachability question. We focus on the impacted destination prefix `2.128.0.0/16`. 


```python
diff_routes = bf.q.bgpRib(network="2.128.0.0/16").answer(snapshot=FAIL_SNAPSHOT_NAME, 
                                                         reference_snapshot=BASE_SNAPSHOT_NAME)
diff_routes
```


We see that routers in `Asia` (`Hongkong`, `Singapore`, and `Tokyo`) and `Seattle` do not have any BGP routes to the prefix in the failure snapshot, which they did in the reference snapshot. The missing route in `Seattle` can be explained via missing routes in `Asia` since `Seattle` depended on `Asia` after losing its two other links. 

That `Europe` still has the routes after the failure alerts us to the possibility of improper filtering of incoming routes in `Asia`. So, we should check on that. There are many ways to analyze the incoming route filters; we'll use the `definedStructures` question of Batfish to extract necessary definitions that we need to view.


```python
# View defined structures of type 'route-map' on 'hongkong'
bf.q.definedStructures(types='route-map', nodes="hongkong").answer()
```


We see the route map `as1_to_as3` is defined on line 119 and 120. Now we can quickly navigate to the lines in the config file, as showing below.


```python
# See the config lines where the route map as1_to_as3 is defined
!cat networks/failure-analysis/configs/hongkong.cfg | head -121 | tail -4
```

    !
    route-map as1_to_as3 deny 100
     match ip address 102
    !


We see that the route map is denying routes that match the access-list '102.' Let's look at the definition of this list, which is on lines 115-117 per the defined structures list above. 


```python
# See the config lines where the access list '102' is defined
!cat networks/failure-analysis/configs/hongkong.cfg | head -118 | tail -5
```

    !
    access-list 102 permit ip host 1.0.1.0 host 255.255.255.0
    access-list 102 permit ip host 1.0.2.0 host 255.255.255.0
    access-list 102 permit ip host 2.128.0.0 host 255.255.0.0
    !


We see that this list includes the prefix of interest, which is `2.128.0.0/16` on the last line. Thus, the route map inadvertently blocks the prefix, thus disconnecting `Asia` from `US` when `Seattle` or its links fail. 

Without Batfish, it would have been hard to find this vulnerability, but the Chaos Monkey style testing enabled by Batfish makes it easy to find such vulnerabilities before they cause a service outage.

## Summary 
This notebook demonstrates how Batfish help analyze forwarding behavior in network failures. Specifically,
  1. `bf.fork_snapshot` can clone a snapshot from another with deactivated interfaces and nodes;
  2. `differentialReachability` can check all forwarding behavior changes for all flows between two snapshots;
  3. We can build on top of the basic functions to create more involved analysis such as Chaos Monkey testing.
