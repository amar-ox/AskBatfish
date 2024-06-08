# Introduction to Forwarding Change Validation


Network engineers frequently have to make changes to network that can impact forwarding behavior: add new routes, open or close flows, route traffic  through different devices, etc. These changes are often hard to get right and hard to validate. 

This notebook will show how Batfish can help validate changes to network forwarding _before_ you deploy them. We will do this using Batfish's *reachability* and *differentialReachability* questions that can provide guarantees that our changes are correct and have no unintended side-effects. As we will see, these anaylses are a powerful way to understand, test, and validate changes to the network. 

Check out a video demo of this notebook [here](https://youtu.be/Yje70Q8R79w).



```python
# Import packages
%run startup.py
bf = Session(host="localhost")
```

In this notebook we will use the network shown in the diagram below. You can view and download the device configuration files [here](https://github.com/batfish/pybatfish/tree/master/jupyter_notebooks/networks/forwarding-change-validation/base).

![example-network](https://raw.githubusercontent.com/batfish/pybatfish/master/jupyter_notebooks/networks/forwarding-change-validation/differential%20forwarding%20network.png)





## Change Scenario 1: Costing out a core router

The network is overprovisioned with failover redundancy for the core routers. All traffic is normally routed through `core1` but will automatically switch to  `core2` in case of a failure or during maintenance. In this scenario, we want to service `core1` and thus want to shift traffic to `core2`. We'll implement a change to cost out `core1`, and verify that it does not affect end-to-end reachability. In general, we care about three classes of end-to-end traffic: external-to-host, host-to-external, and host-to-host. For simplicity, we focus on the external-to-host traffic in this notebook but similar queries can cover other classes.

### Step 1: Test current behavior


Before beginning, let's check that the network is working as expected (i.e., routing through `core1`). First we load our snapshot into Batfish.


```python
NETWORK_NAME = "forwarding-change-validation"
BASE_NAME = "base"
BASE_PATH = "networks/forwarding-change-validation/base"

bf.set_network(NETWORK_NAME)
bf.init_snapshot(BASE_PATH, name=BASE_NAME, overwrite=True)
```

Batfish will automatically compute the RIBs and FIBs from the configuration files in the snapshot, allowing us to test the forwarding behavior offline. Let's do that now, by using the `traceroute` question to see how external-to-host traffic is routed. The parameter `startLocation="@enter(/border/[GigabitEthernet0/0])"` says to start the trace entering the external border router interfaces. The parameter `dstIps="/host/)"` indicates that the flow should be addressed to one of the internal hosts. These two parameters are using [specifier grammar](https://github.com/batfish/batfish/blob/master/questions/Parameters.md).


```python
answer = bf.q.traceroute(
    startLocation="@enter(/border/[GigabitEthernet0/0])",
    headers=HeaderConstraints(dstIps="/host/")
).answer(snapshot=BASE_NAME)
show(answer.frame())
```


The `traceroute` results include a flow from each border router, and all possible paths of each flow. As we can see in the `Traces` column, both flows are routed through `core1`.  For more detail on `traceroute` question, see the notebook [Introduction to Forwarding Analysis](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/Introduction%20to%20Forwarding%20Analysis.ipynb).


Next, we'll cost out `core1` and cause all traffic to start being routed through `core2`. Below you can see the configuration changes we're going to make. We add the command `ip ospf cost 500` to each interface on `core1`, increasing its OSPF cost from the previous value of `1`. This will cause the lower-cost routes through `core2` to be preferred.


```
$ diff -r base/ change1/
diff -r base/configs/core1.cfg change1/configs/core1.cfg
68c68
<  ip ospf cost 1
---
>  ip ospf cost 500
73c73
<  ip ospf cost 1
---
>  ip ospf cost 500
78c78
<  ip ospf cost 1
---
>  ip ospf cost 500
83c83
<  ip ospf cost 1
---
>  ip ospf cost 500
```

We implemented this change offline in a new snapshot, and will validate that the change doesn't affect reachability. Having done so, we will be able to push the change to the network with complete confidence.

We'll validate the change using a two-step process, verifying that it has the intended effect, and that it causes no collateral damage. More specifically, the change must:
1. Ensure that no traffic is routed through `core1`.
1. Have no effect on external-to-host traffic.


### Step 2: Ensure that no traffic is routed through `core1`


The following commands will load our change snapshot into batfish:



```python
CHANGE1_NAME = "change"
CHANGE1_PATH = "networks/forwarding-change-validation/change1"

bf.init_snapshot(CHANGE1_PATH, name=CHANGE1_NAME, overwrite=True)
```




    'change'



To verify that **no** outside-to-host traffic is routed through `core1`, we need to search for counterexamples: outside-to-host traffic that *is* routed through `core1`. If no counterexamples are found, we have *proven* that `core1` is never used. We do this by running the `reachability` question with the `transitLocations` parameter to search for flows that transit `core1`. We set the `actions` parameter to `SUCCESS,FAILURE` to include dropped flows as well as those that are successfully delivered.


```python
# Search for any traffic routed through core1
answer = bf.q.reachability(
    pathConstraints=PathConstraints(
        startLocation="@enter(/border/[GigabitEthernet0/0])",
        transitLocations="core1"),
    headers=HeaderConstraints(dstIps="/host/"),
    actions="SUCCESS,FAILURE"
).answer(snapshot=CHANGE1_NAME)
show(answer.frame())
```



Good! Since we found no counter-examples, we are guaranteed that no outside-to-host traffic from will be routed through `core1`. This verifies the first requirement of the change. Having done so, let's check our second requirement -- that end-to-end reachability is completely unchanged.



### Step 3: Outside-to-host traffic is unaffected.


In this step, we'll compare the forwarding behavior of the candidate change snapshot against the original using the `differentialReachability` question. In particular, we'll use the question to search for flows that are successfully delivered in one snapshot but not the other. If the change is correct, no such flows will be found, because costing out `core1` should have no effect on end-to-end reachability.


```python
answer = bf.q.differentialReachability(
    pathConstraints=PathConstraints(startLocation="@enter(/border/[GigabitEthernet0/0])"),
    headers=HeaderConstraints(dstIps="/host/")
).answer(
    snapshot=CHANGE1_NAME,
    reference_snapshot=BASE_NAME)
show(answer.frame())
```



As we can see, moving traffic from `core1` to `core2` does affect reachability: some traffic that was being delivered in the reference snapshot (before the change) is being *null routed* in the change snapshot (after the change). This means if we deploy the change now, there will be a loss of connectivity. Fortunately the `differentialReachability` question was able to identify that bug before we deployed the change. 

The results include an example flow from each start location that has traffic affected by the change. Each flow comes with detailed traces of all the paths it can take through the network, which helps us diagnose the problem: `core2` has a rogue static route for `2.180.0.0/24` that should have been removed. A similar problem could occur with rogue ACLs along the backup path (which Batfish will find as well)

### Step 2 (again): Ensure that no traffic is routed through core1

We remove the bad static route and load the updated change snapshot into batfish. Then we perform the same validation steps again.


```python
CHANGE1_FIXED_NAME = "change-fixed"
CHANGE1_FIXED_PATH = "networks/forwarding-change-validation/change1-fixed"
bf.init_snapshot(CHANGE1_FIXED_PATH, name=CHANGE1_FIXED_NAME, overwrite=True)
```




    'change-fixed'




```python
# Requirement 1: No traffic is routed through core1.
answer = bf.q.reachability(
    pathConstraints=PathConstraints(
        startLocation="@enter(/border/[GigabitEthernet0/0])",
        transitLocations="core1"),
    headers=HeaderConstraints(dstIps="/host/"),
    actions="SUCCESS,FAILURE"
).answer(snapshot=CHANGE1_FIXED_NAME)
show(answer.frame())

```



Again, we find no traffic being routed through `core1`, so it is still correctly costed-out. 



### Step 3 (again): Outside-to-host traffic is unaffected.


We now move on to check that after removing the bad null route, costing out `core1` has no impact on the reachability matrix:


```python
# Requirement 2: Outside-to-host traffic is unaffected.
answer = bf.q.differentialReachability(
    pathConstraints=PathConstraints(startLocation="@enter(/border/[GigabitEthernet0/0])"),
    headers=HeaderConstraints(dstIps="/host/")
).answer(
    snapshot=CHANGE1_FIXED_NAME,
    reference_snapshot=BASE_NAME)
show(answer.frame())
```


Success! We have now verified that our change will correctly cost-out `core1` without affecting reachability. We are ready to deploy the change and do the maintenance work for `core1` with complete confidence. 



### Summary


Let's recap the steps we took to verify this change:
1. First, we verified that the primary intent of the change is achieved: traffic is moved from `core1` to `core2`. We used the `reachability` query to search *all* outside-to-host flows in the network and verify that none will transit `core1` after the change.
1. Second, we verified that moving the traffic did not affect reachability. For this, we used the `differentialReachability` query to compare the forwarding behavior of two snapshots. This verified that *no flow* is affected by the change.

## Change Scenario 2: Validating the end-to-end impact of an ACL change

In this second part of this notebook, we'll validate another change to the same network. Unlike the previous scenario, this time we do want to alter end-to-end reachability, and we will verify that our change has the intended effect. As before, we will also verify that it has no *unintended* effects.

In this scenario, we have developed and tested a new web service on host `host-www`, and are now ready to open it to HTTP traffic from the outside world. The service is running on the hosts behind `leaf1`, which has an ACL in place that filters traffic to each host. The change we'll make and validate will open traffic to the host subnet in the border router ACLs that filter traffic entering the network. 

### Step 1: Test current behavior

We start by using the `traceroute` question to verify that `host-www` is not accessible via HTTP from outside the network. The parameter `dstIps=ofLocation(host-www)` tells traceroute to pick any IP belonging to `host-www` as the destination IP.


```python
answer = bf.q.traceroute(
    startLocation="@enter(/border/[GigabitEthernet0/0])",
    headers=HeaderConstraints(dstIps="host-www", applications="HTTP")
).answer(snapshot=BASE_NAME)
show(answer.frame())
```




As you can see, the flow is dropped by the ingress ACL `OUTSIDE_TO_INSIDE` on each border router. This is where we'll make our change. The following snippet shows the original ACL definition:


```
ip access-list extended OUTSIDE_TO_INSIDE
 permit tcp any 2.128.0.0 0.0.1.255 eq ssh
 permit udp any 2.0.0.0 0.255.255.255
 deny ip any any
```

The first line permits SSH traffic to host subnet. We'll create a similar rule for HTTP, since the `leaf1` already does the required per-host filtering. Here's the updated version of the ACL: 

```
ip access-list extended OUTSIDE_TO_INSIDE
 permit tcp any 2.128.0.0 0.0.1.255 eq ssh
 permit tcp any 2.128.0.0 0.0.1.255 eq www
 permit udp any 2.0.0.0 0.255.255.255
 deny ip any any
```

Next we load the snapshot with our change into batfish so we can validate it before deployment.


```python
CHANGE2_NAME = "change2"
CHANGE2_PATH = "networks/forwarding-change-validation/change2"
bf.init_snapshot(CHANGE2_PATH, name=CHANGE2_NAME, overwrite=True)
```




    'change2'



We can test our change by running the above `traceroute` command on the change snapshot:


```python
answer = bf.q.traceroute(
    startLocation="@enter(/border/[GigabitEthernet0/0])",
    headers=HeaderConstraints(dstIps="host-www", applications="HTTP")
).answer(snapshot=CHANGE2_NAME)
show(answer.frame())
```



Good. We now see that HTTP traffic can reach `host-www` from outside the network. We may be tempted to call it good and ship the change. However, batfish gives us the ability to do much more to ensure complete correctness.  

Following the steps outlined in the [Provably Safe ACL and Firewall Changes](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/Provably%20Safe%20ACL%20and%20Firewall%20Changes.ipynb) notebook, we can independently validate the change to each border router ACL. We omit those steps from this notebook, and proceed to validating the end-to-end network behavior. 

As before, end-to-end validation has two requirements:
1. The change has the intended effect: HTTP traffic from outside the network can reach `host-www`.
1. The change has no unintended effects: No other traffic is affected.

### Step 2: External HTTP traffic can now reach `host-www` 

The `traceroute` results above show that *some* HTTP traffic can now reach `host-www` from outside the network. However, this doesn't ensure that *all* such traffic can reach `host-www`. For that, we use the `reachability` query to search for counterexamples of the requirement: HTTP flows from the outside that *cannot* reach `host-www`. 


```python
answer = bf.q.reachability(
    pathConstraints=PathConstraints(startLocation="@enter(/border/[GigabitEthernet0/0])"),
    headers=HeaderConstraints(
        dstIps="host-www",
        srcIps="0.0.0.0/0",
        applications="HTTP"),
    actions="FAILURE"
).answer(snapshot=CHANGE2_NAME)
show(answer.frame())
```



Good! Since batfish's comprehensive search found no counterexamples, we are guaranteed that none exist. In other words, the requirement is met.

### Step 3: No unintended consequences

Next, we check the second requirement -- that the change has no unintended effects. As before, we'll use the `differentialReachability` question to compare the reachability of our change snapshot against the original network. We search all flows entering the border routers *that are not* HTTP traffic addressed to `host-www`. The `invertSearch=True` parameter causes batfish to search outside the specified header space instead of within it.


```python
answer = bf.q.differentialReachability(
    pathConstraints=PathConstraints(startLocation="@enter(/border/[GigabitEthernet0/0])"),
    headers=HeaderConstraints(dstIps="host-www", applications="HTTP"),
    invertSearch=True
).answer(snapshot=CHANGE2_NAME, reference_snapshot=BASE_NAME)
show(answer.frame())
```



Unfortunately, our change had a broader impact than we intended. It turns out that `leaf1` was not properly filtering traffic to `host-db`: it permits HTTP to both hosts, rather than just `host-www`.

### Step 2 (again): Verify HTTP traffic can now reach `host-www`

We fix the buggy ACL on `leaf1`, load the fixed change snapshot into batfish and begin the validation process again. Here is the difference relative the first change attempt:

```
$ diff -r change2/ change2-fixed/
diff -r change2/configs/leaf1.cfg change2-fixed/configs/leaf1.cfg
119c119
<  permit tcp any 2.128.0.0 0.0.255.255 eq www
---
>  permit tcp any 2.128.1.0 0.0.0.255 eq www
```


```python
CHANGE2_FIXED_NAME = "change2-fixed"
CHANGE2_FIXED_PATH = "networks/forwarding-change-validation/change2-fixed"
bf.init_snapshot(CHANGE2_FIXED_PATH, name=CHANGE2_FIXED_NAME, overwrite=True)
```




    'change2-fixed'




```python
answer = bf.q.reachability(
    pathConstraints=PathConstraints(startLocation="@enter(/border/[GigabitEthernet0/0])"),
    headers=HeaderConstraints(dstIps="host-www", applications="HTTP"),
    actions="FAILURE"
).answer(snapshot=CHANGE2_FIXED_NAME)
show(answer.frame())
```


As before, the requirement is met: since we did not find any dropped HTTP flows to `host-www`, we are guaranteed that all will be delivered successfully. Our first requirement is still met.

### Step 3 (again): No unintended consequences


```python
answer = bf.q.differentialReachability(
    pathConstraints=PathConstraints(startLocation="@enter(/border/[GigabitEthernet0/0])"),
    headers=HeaderConstraints(dstIps="host-www", applications="HTTP"),
    invertSearch=True
).answer(snapshot=CHANGE2_FIXED_NAME, reference_snapshot=BASE_NAME)
show(answer.frame())
```



Success! This time `differentialReachability` returns no results, which means no traffic was affected by the changes other than external HTTP traffic to `host-www`. Our second requirement is now met.

### Summary

Let's recap the steps we took to verify this change:
1. First, we verified that the primary intent of the change is achieved: it allows external HTTP traffic to reach `host-www`.
1. Second, we verified that there were no other changes to external-to-host reachability. We used the `differentialReachability` query to compare the forwarding behavior of two snapshots. This verified that *only* external HTTP traffic to `host-www` is affected by the change.

## Conclusion

In this notebook, you saw how batfish can help you validate changes to forwarding behavior *before* you deploy them to the network. Using batfish's differential analysis of forwarding behavior, you can guarantee that your change does exactly what you intend -- no more and no less. 

Want to learn more? Come find us on [Slack](https://join.slack.com/t/batfish-org/shared_invite/enQtMzA0Nzg2OTAzNzQ1LTcyYzY3M2Q0NWUyYTRhYjdlM2IzYzRhZGU1NWFlNGU2MzlhNDY3OTJmMDIyMjQzYmRlNjhkMTRjNWIwNTUwNTQ) and [GitHub](https://github.com/batfish/batfish).
