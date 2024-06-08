# Provably safe ACL and firewall rule changes

Changing ACLs or firewall rules is one of the riskiest updates to a network. Even a small error can block connectivity for a large set of critical services or open up sensitive resources to the world at large. 

This notebook shows a 3-step process that uses Batfish to make provably safe and correct changes to ACLs and firewall rules, which we generally call filters. For a broader view of Batfish's support for analyzing filters, check out the ["Analyzing ACLs and Firewall Rules" notebook](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/Analyzing%20ACLs%20and%20Firewall%20Rules.ipynb).

Check out a video demo of this notebook [here](https://www.youtube.com/watch?v=MJYLVL9UOWk).

We will primarily use the `searchFilters` question of Batfish in this process. This question searches within large spaces of flows (specified using packet headers) for flows that match the specified action ('permit' or 'deny'). See [here](https://pybatfish.readthedocs.io/en/latest/notebooks/filters.html#Search-Filters) for its documentation.

## Change scenario

Our goal is to update an ACL on one of our routers to permit HTTP traffic (ports 80 and 8080) from one subnet (10.10.10.0/24) to another (18.18.18.0/27). We will implement this by adding rules to permit this traffic to our ACLs, and we will then use Batfish to check if the implementation was correct.

## Initialization

We start by initializing the pre-change snapshot and variables that describe the change. Our example snapshot contains two devices, and we'll change the ACL **acl_in** on [**rtr-with-acl**](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/networks/example-filters/current/configs/rtr-with-acl.cfg). 


```python
# Import packages
%run startup.py 
bf = Session(host="localhost")

# Initialize a network and snapshot
CURRENT_SNAPSHOT_NAME = "current"
CURRENT_SNAPSHOT_PATH = "networks/example-filters/current"
bf.set_network("network-example-filters")
bf.init_snapshot(CURRENT_SNAPSHOT_PATH, name=CURRENT_SNAPSHOT_NAME, overwrite=True)
```




    'current'




```python
node_name = "rtr-with-acl"  # The router to change
filter_name = "acl_in"      # Name of the ACL to change

# The traffic to allow
change_traffic = HeaderConstraints(srcIps="10.10.10.0/24",
                                   dstIps="18.18.18.0/27",
                                   ipProtocols=["tcp"],
                                   dstPorts="80, 8080")
```

## Step 1:  Ensure that the intended traffic is not already permitted

Before we make the change to allow the intended traffic, we verify that that traffic is not already permitted — because if it is, we do not need to change anything. We accomplish this using the `searchFilters` question. Given a space of flows, specified using header fields such as source and destination addresses and ports, and a matching condition (e.g., permit, deny) as input, this question finds flows that satisfy the condition. If it reports no flows, then it is guaranteed that no flow within the space satisfies the condition. 


```python
# Check if the intended traffic is already permitted in the current snapshot
answer = bf.q.searchFilters(headers=change_traffic,
                           filters=filter_name,
                           nodes=node_name,
                           action="permit").answer(
                               snapshot=CURRENT_SNAPSHOT_NAME)
show(answer.frame())
```



Since the query above did not find any results, we know with certainty that no flow within the specified space is already permitted. We can now proceed. If some flow is returned as part of the query, we may want to delete the filter line(s) that permits that flow before we update the filter.

## Step 2: Ensure that the intended traffic is permitted in the candidate change

Assume that we implemented a candidate change, shown as the diff below.
```
diff -r networks/example-filters/current/configs/rtr-with-acl.cfg \ 
        networks/example-filters/candidate1/configs/rtr-with-acl.cfg
39a40,41
>   462 permit tcp 10.10.10.0/24 18.18.18.0/26 eq 80   
>   463 permit tcp 10.10.10.0/24 18.18.18.0/26 eq 8080   
```

We can load the snapshot with this change into Batfish and ensure that all flows within the intended traffic are permitted. We will do that by asking the same `searchFilters` question as before, except now searching for flows that are denied instead of permitted. If it produces no results, then we have the guarantee that all possible flows in the intended space are allowed.


```python
# Load the candidate1 change
CANDIDATE1_SNAPSHOT_NAME = "candidate1"
CANDIDATE1_SNAPSHOT_PATH = "networks/example-filters/candidate1"
bf.init_snapshot(CANDIDATE1_SNAPSHOT_PATH, name=CANDIDATE1_SNAPSHOT_NAME, overwrite=True)

# Check if any flow in the intended traffic is denied in candidate1
answer = bf.q.searchFilters(headers=change_traffic,
                           filters=filter_name,
                           nodes=node_name,
                           action="deny").answer(
                               snapshot=CANDIDATE1_SNAPSHOT_NAME)
show(answer.frame())
```



Since we got no results, we can be confident that our candidate change permits *all* traffic that we intended to permit. If there were any flow in the desired space that was not permitted by the change, the query above would have found it.

## Step 3: Ensure that no collateral damage has occurred

Typically, engineers will stop change validation after checking that the intended traffic has been successfully permitted by the change. However, for safety and correctness, we must also check that no traffic outside of the intended space has been impacted — that is, our change has not caused collateral damage.

We can verify this using a "differential" version of the `searchFilters` question that compares two snapshots. The query below compares the candidate1 and initial snapshots, and is asking Batfish if there is *any* flow outside of the intended traffic that the two snapshots treat differently (i.e., one of them permits and the other rejects, or vice versa). To search traffic outside the specified flow space, we use the `invertSearch` flag. If this query returns no result, then combined with the result above, we have ensured that the change is completely correct.


```python
# Check if traffic other than the intended traffic has been impacted
answer = bf.q.searchFilters(headers=change_traffic,
                           invertSearch=True,
                           filters=filter_name,
                           nodes=node_name).answer(snapshot=CANDIDATE1_SNAPSHOT_NAME,
                                                   reference_snapshot=CURRENT_SNAPSHOT_NAME)
show(answer.frame())
```



Unfortunately, we do get a result, indicating that at least one flow outside of the intended space will be treated differently than before. The column `Flow` shows a flow that the two snapshots treat differently. In particular, this flow has destination IP address 18.18.18.32, which is *outside* of the address range 18.18.18.0/27 that we wanted to permit. The columns that start with `Base_` show how `CANDIDATE1_SNAPSHOT` treats that flow, and those that start with `Delta_` show how `CURRENT_SNAPSHOT` treats the flow. As shown, the candidate snapshot permits the flow while the current snapshot denies it. That means we've accidentally opened up more space than we intended.

The root cause of the problem is apparent if we look at the diff above more carefully. The updated ACL permits destination prefix 18.18.18.0/26 rather than the intended 18.18.18.0/27. We need to fix this.

## Step 2 (again): Ensure that the intended traffic is permitted in the candidate change

Assume that we implemented another candidate change, shown by the diff below.
```
diff -r networks/example-filters/current/configs/rtr-with-acl.cfg \ 
        networks/example-filters/candidate2/configs/rtr-with-acl.cfg
39a40,41
>   462 permit tcp 10.10.10.0/24 18.18.18.0/27 eq 80   
>   463 permit tcp 10.10.10.0/24 18.18.18.0/27 eq 8080   
```

We will now load this change and repeat the same validation steps that we ran on the prior candidate change.


```python
# Load (another) candidate change
CANDIDATE2_SNAPSHOT_NAME = "candidate2"
CANDIDATE2_SNAPSHOT_PATH = "networks/example-filters/candidate2"
bf.init_snapshot(CANDIDATE2_SNAPSHOT_PATH, name=CANDIDATE2_SNAPSHOT_NAME, overwrite=True)

# Check if any part of the intended traffic is denied in candidate2
answer = bf.q.searchFilters(headers=change_traffic,
                           filters=filter_name,
                           nodes=node_name,
                           action="deny").answer(snapshot=CANDIDATE2_SNAPSHOT_NAME)
show(answer.frame())
```



As before, we get no results, which means that no flow in the intended space is being denied; we correctly permitted all intended traffic. 

## Step 3 (again): Ensure that no collateral damage has occurred

Now, let's also check again that no other traffic is impacted.


```python
# Check if traffic other than the intended traffic has been impacted
answer = bf.q.searchFilters(headers=change_traffic,
                           filters=filter_name,
                           nodes=node_name,
                           invertSearch=True).answer(snapshot=CANDIDATE2_SNAPSHOT_NAME,
                                                     reference_snapshot=CURRENT_SNAPSHOT_NAME)
show(answer.frame())
```


This time, we got no collateral damage results! That implies this change is completely correct: It allows all traffic that we meant to allow and has no impact on other traffic. Therefore we can apply it with full confidence that it will have the exact desired behavior.

## Summary

In this notebook, we showed how you can use Batfish to ensure that changes to filters are correct and permit or deny only the intended traffic. 

The steps for provably safe ACL and firewall changes are:
1. Check that the intended traffic does not already match the desired action (permit or deny)
2. Check that the intended traffic is treated correctly in the candidate change
3. Check that nothing but the intended traffic is impacted by the candidate change

For additional ways to analyze filter using Batfish, see the ["Analyzing ACLs and Firewall Rules" notebook](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/Analyzing%20ACLs%20and%20Firewall%20Rules.ipynb).
