# Safely refactoring ACLs and firewall rules

Changing ACLs or firewall rules (or *filters*) is one of the riskiest updates to a network. Even a small error can block connectivity for a large set of critical services or open up sensitive resources to the world at large. Earlier notebooks showed how to [analyze filters for what they do and do not allow](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/Analyzing%20ACLs%20and%20Firewall%20Rules.ipynb) and how to [make specific changes in a provably safe manner](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/Provably%20Safe%20ACL%20and%20Firewall%20Changes.ipynb).

This notebook shows how to refactor complex filters in a way that the full impact of refactoring can be understood and analyzed for correctness *before* refactored filters are pushed to the network. 

## Original ACL

We will use the following ACL as a running example in this notebook. The ACL can be read as a few separate sections:

* Line 10: Deny ICMP redirects
* Lines 20, 23: Permit BFD traffic on certain blocks
* Lines 40-80: Permit BGP traffic
* Lines 90-100: Permit DNS traffic a /24 subnet while denying it from a /32 within that
* Lines 110-500: Permit or deny IP traffic from certain subnets
* Line 510: Permit ICMP echo reply
* Lines 520-840: Deny IP traffic to certain subnets
* Lines 850-880: Deny all other types of traffic

(The IP address space in the ACL appears all over the place because it has been anonymized via [Netconan](https://github.com/intentionet/netconan). Netconan preserves the super- and sub-prefix relationships when anonymizing IP addresses and prefixes.)


## Compressed ACL

Now, assume that we want to compress this ACL to make it more manageable. We do the following operations:

* Merge the two BFD permit statements on lines 20-30 into one statement using the range directive.
* Remove the BGP session on line 80 because it has been decommissioned
* Remove lines 180 and 250 because they are shadowed by earlier lines and will never match a packet. Such lines can be found via the `filterLineReachability` question, as shown [here](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/Analyzing%20ACLs%20and%20Firewall%20Rules.ipynb#filterLineReachability:-Analyzing-reachability-of-filter-lines).
* Merge pairs of lines (190, 200), (210, 220), and (260, 270) by combining their prefixes into a less specific prefix.
* Remove all deny statements on lines 520-870. They are not needed given the final deny on line 880.

The result of these actions, which halve the ACL size, is shown below. To enable easy observation of changes, we have preserved the line numbers. 



The challenge for us is to find out if and how this compressed ACL differs from the original. That is, is there is traffic that is treated differently by the two ACLs, and if so, which lines are responsible for the difference.

This task is difficult to get right through manual reasoning alone, which is why we developed the `compareFilters` question in Batfish.

## Comparing filters

We can compare the two ACLs above as follows. To initialize snapshots, we will use Batfish's `init_snapshot_from_text` function which creates a snapshot with a single device who configuration is the provided text. The analysis shown below can be done even when the filters are embedded within bigger device configurations. 


```python
# Import packages 
%run startup.py
bf = Session(host="localhost")

# Initialize a snapshot with the original ACL
original_snapshot = bf.init_snapshot_from_text(
    original_acl, 
    platform="cisco-nx", 
    snapshot_name="original", 
    overwrite=True)

# Initialize a snapshot with the compressed ACL
compressed_snapshot = bf.init_snapshot_from_text(
    compressed_acl, 
    platform="cisco-nx", 
    snapshot_name="compressed", 
    overwrite=True)

# Now, compare the two ACLs in the two snapshots
answer = bf.q.compareFilters().answer(snapshot=compressed_snapshot, reference_snapshot=original_snapshot)
show(answer.frame())
```


The `compareFilters` question compares two filters and returns pairs of lines, one from each filter, that match the same flow(s) but treat them differently. If it reports no output, the filters are guaranteed to be identical. The analysis is exhaustive and considers *all possible* flows.

As we can see from the output above, our compressed ACL is not the same as the original one. In particular, line 210 of the compressed ACL will deny some flows that were being permitted by line 510 of the original; and line 510 of the compressed ACL will permit some flows that were being denied by line 220 of the original ACL. Because the permit statements correspond to ICMP traffic, we can tell that the traffic treated by the two filters is ICMP. To narrow learn specific source and destination IPs that are impacted, one may run the `searchFilters` question, as shown [here](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/Provably%20Safe%20ACL%20and%20Firewall%20Changes.ipynb#Step-3:-Ensure-that-no-collateral-damage-has-occurred). 

By looking at the output above, we can immediately understand the difference: 

* The first line is showing that the compressed ACL is denying some traffic on line 210 (with index 16) that the original ACL was permitting via line 510, and the compressed ACL is permitting some traffic on line 510 that the original ACL was denying via line 220. 

  It turns out that the address space merger we did for lines 210 and 220 in the original ACL, where we combined 218.67.72.0/24 and 218.67.71.0/24 into  218.67.71.0/23, was not correct. The other similar mergers of 218.66.57.0/24 and 218.66.56.0/24 into 218.66.56.0/23 and of 218.8.104.0/25 and 218.8.104.128/25 into 218.8.104.0/24 were correct.


* The third line is showing that the compressed ACL is denying some traffic at the end of the ACL that the original ACL was permitting via line 80. This is an expected change of decommissioning the BGP session on line 80. 

  It is not always the case that refactoring is semantics preserving. Where `compareFilters` helps is succinctly enumerating *all* differences. Engineers can look at the differences and decide if the refactored filter meets their intent.

## Splitting ACLs

Compressing large ACLs is one type of refactoring engineers do; another one is splitting a large ACL into multiple smaller ACLs and composing them on the same device or spreading across multiple devices in the network. Smaller ACLs are easier to maintain and evolve. However, the split operation is risky. We may forget to include in the smaller ACLs some protections that exist in the original ACL. We show how such splits can be safely done using Batfish.

Suppose we want to split the compressed ACL above into multiple smaller ACLs that handle different concerns. So, we should have different ACLs for different types of traffic and different ACLs for different logical groups of nodes in the network. The result of such splitting is shown below. For ease of exposition, we have retained the line numbers from the original ACL and mimic a scenario in which all ACLs live on the same device.



Given the split ACLs above, one analysis may be to figure out if each untrusted source subnet was included in a smaller ACL. Otherwise, we have lost protection that was present in the original ACL. We can accomplish this analysis via the `findMatchingFilterLines` question, as shown below. 

Once we are satisfied with analysis of filters, for an end-to-end safety guarantee, we should also analyze if there are new flows that the network will allow (or disallow) after the change. Such an analysis can be done via the `differentialReachability` question, as shown [here](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/Introduction%20to%20Forwarding%20Change%20Validation.ipynb#Change-Scenario-2:-Validating-the-end-to-end-impact-of-an-ACL-change). 


```python
# Initialize a snapshot with the smaller ACLs
smaller_snapshot = bf.init_snapshot_from_text(
    smaller_acls, 
    platform="cisco-nx", 
    snapshot_name="smaller", 
    overwrite=True)

# All untrusted subnets
untrusted_source_subnets = ["54.0.0.0/8", 
                            "163.157.0.0/16", 
                            "166.144.0.0/12", 
                            "198.170.50.0/24", 
                            "198.120.0.0/16", 
                            "11.36.192.0/19", 
                            "11.125.64.0/19", 
                            "218.66.56.0/24", 
                            "218.66.57.0/24", 
                            "218.67.71.0/23", 
                            "218.67.96.0/22", 
                            "8.89.120.0/22"
                           ]

for subnet in untrusted_source_subnets:
    # Find which ACLs match traffic from this source subnet
    answer = bf.q.findMatchingFilterLines(
        headers=HeaderConstraints(srcIps=subnet),
        filters="/deny-untrusted/").answer(snapshot=smaller_snapshot)

    # Each source subnet should match exactly one ACL
    af = answer.frame()
    if len(af) == 1:
        print("{} .... OK".format(subnet))
    elif len(af) == 0:
        print("{} .... ABSENT".format(subnet))
    else:
        print("{} .... Multiply present".format(subnet))
        show(af)
```

    54.0.0.0/8 .... OK
    163.157.0.0/16 .... OK
    166.144.0.0/12 .... OK
    198.170.50.0/24 .... OK
    198.120.0.0/16 .... OK
    11.36.192.0/19 .... Multiply present


    11.125.64.0/19 .... ABSENT
    218.66.56.0/24 .... OK
    218.66.57.0/24 .... OK
    218.67.71.0/23 .... OK
    218.67.96.0/22 .... OK
    8.89.120.0/22 .... OK


In the code above, we first enumerate all untrusted subnets in the network. The granularity of this specification need not be the same as that in the ACL. For instance, we enumerate 218.66.56.0/24 and 218.66.57.0/24 as untrusted subnets but the ACL has a less specific prefix 218.66.56.0/23. Batfish understands such relationships and provides an accurate analysis that is not possible with simple string matching.

The **for** loop above uses the `findMatchingFilterLines` question to find out which lines across all ACLs whose names contain "deny-untrusted" will match packets starting the the specified subnet. Our expectation is that each subnet should match exactly one line in exactly one ACL, and the output shows "OK" against such subnets. It shows "Absent" for subnets that do not match any line and shows the multiple matching lines for subnets where that happens.

We see that during the split above, we ended up matching the subnet 11.36.192.0/19 twice, once as a /19 in ACL deny-untrusted-sources-group1 and then as /20 in ACL deny-untrusted-sources-group2. More dangerously, we completely forgot to match the 11.125.64.0/19, which will open a security hole in the network if these smaller ACLs were applied.

## Summary

In this notebook, we showed how to use the `compareFilters` and `findMatchingFilterLines` questions of Batfish to safely refactor complex filters. 

* `compareFilters` analyzes the original and revised filter to enumerate all cases that will treat *any* flow differently. 
* `findMatchingFilterLines` enumerates all lines across all specified filters that match the given space of flows.

For additional ways to analyze filter using Batfish, see the ["Analyzing ACLs and Firewall Rules"](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/Analyzing%20ACLs%20and%20Firewall%20Rules.ipynb) and the ["Provably Safe ACL and Firewall Changes"](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/Provably%20Safe%20ACL%20and%20Firewall%20Changes.ipynb) notebooks.
