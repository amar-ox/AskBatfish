# Analyzing ACLs and firewall rules with Batfish

Network and security engineers are responsible for ensuring that the ACLs and firewall rules in their networks are permitting and denying traffic as intended. This task usually requires manual checking or loading rulesets onto a lab device in order to test behavior on example packets of interest. These methods are not only time consuming but also error-prone. 

Batfish makes it easy to deeply analyze ACLs and firewall rules, which we generally call *filters.* It can show what a filter will do with a given packet, right down to the line of the filter that matches the packet; it can provide guarantees on how a filter treats a large space of packets; and it can sanity check a filter to ensure that every line in it matches at least some packets.

In this notebook, we demonstrate these capabilities. In our ["Provably Safe ACL and Firewall Changes" notebook](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/Provably%20Safe%20ACL%20and%20Firewall%20Changes.ipynb), we show how Batfish can guarantee that filter changes are safe.

Check out a video demo of this notebook [here](https://youtu.be/KixQYEDh33s).

## Initialization

We use an example network with two devices, a router with ACLs and a firewall.  The device configurations can be seen [here](https://github.com/batfish/pybatfish/tree/master/jupyter_notebooks/networks/example-filters/current/configs). 


```python
# Import packages
%run startup.py
bf = Session(host="localhost")

# Initialize a network and a snapshot
bf.set_network("network-example-filters")

SNAPSHOT_NAME = "current"
SNAPSHOT_PATH = "networks/example-filters/current"
bf.init_snapshot(SNAPSHOT_PATH, name=SNAPSHOT_NAME, overwrite=True)
```




    'current'



## `testFilters`: Testing how filters treat a flow

The `testFilters` question shows what filters do with a particular flow and *why*. It takes as input the details of the flow and a set of filters to test. The answer provides a detailed view of how the flow is treated by each filter in the set.

Flows are specified using source and destination IP addresses and, optionally, other fields such as IP protocols, ports, and TCP flags. You may also specify the ingress interface which is factored in when the behavior of a filter depends on it. See [documentation](https://pybatfish.readthedocs.io/en/latest/notebooks/filters.html#Test-Filters) for details. The question will fill in any unspecified fields with reasonable defaults.

The set of filters to examine can be narrowed using various criteria, including regexes for node and filter names. Left unspecified, `testFilters` will give results for every filter in the network.

### Example 1: Test if hosts in a subnet can reach the DNS server

Suppose we wanted to test if our ACL **acl_in** in router **rtr-with-acl** allows hosts in a subnet to reach our DNS server. This check is easily expressed. If the subnet is 10.10.10.0/24 and the DNS server is at the IP address 218.8.104.58, then the query will be as shown below, where we have picked 10.10.10.1 as a representative source IP for the subnet.


```python
# Check if a representative host can reach the DNS server
dns_flow = HeaderConstraints(srcIps="10.10.10.1",
                             dstIps="218.8.104.58",
                             applications=["dns"])
answer = bf.q.testFilters(headers=dns_flow,
                         nodes="rtr-with-acl",
                         filters="acl_in").answer()
show(answer.frame())
```


<style type="text/css">
#T_pybfstyle_row0_col0, #T_pybfstyle_row0_col1, #T_pybfstyle_row0_col2, #T_pybfstyle_row0_col3, #T_pybfstyle_row0_col4, #T_pybfstyle_row0_col5 {
  text-align: left;
  vertical-align: top;
}
</style>
<table id="T_pybfstyle">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_pybfstyle_level0_col0" class="col_heading level0 col0" >Node</th>
      <th id="T_pybfstyle_level0_col1" class="col_heading level0 col1" >Filter_Name</th>
      <th id="T_pybfstyle_level0_col2" class="col_heading level0 col2" >Flow</th>
      <th id="T_pybfstyle_level0_col3" class="col_heading level0 col3" >Action</th>
      <th id="T_pybfstyle_level0_col4" class="col_heading level0 col4" >Line_Content</th>
      <th id="T_pybfstyle_level0_col5" class="col_heading level0 col5" >Trace</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_pybfstyle_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_pybfstyle_row0_col0" class="data row0 col0" >rtr-with-acl</td>
      <td id="T_pybfstyle_row0_col1" class="data row0 col1" >acl_in</td>
      <td id="T_pybfstyle_row0_col2" class="data row0 col2" >Start Location: rtr-with-acl<br>Src IP: 10.10.10.1<br>Src Port: 49152<br>Dst IP: 218.8.104.58<br>Dst Port: 53<br>IP Protocol: UDP</td>
      <td id="T_pybfstyle_row0_col3" class="data row0 col3" >PERMIT</td>
      <td id="T_pybfstyle_row0_col4" class="data row0 col4" >660 permit udp 10.10.10.0/24 218.8.104.58/32 eq domain</td>
      <td id="T_pybfstyle_row0_col5" class="data row0 col5" ><ul><li>Matched line 660 permit udp 10.10.10.0/24 218.8.104.58/32 eq domain</li></ul></td>
    </tr>
  </tbody>
</table>



The result above shows that the flow we tested is indeed permitted by the filter **acl_in** (in `Filter_Name` column) on device **rtr-with-acl** (in `Node` column). The `Flow` column shows the exact flow tested, including the default values chosen by Batfish for unspecified parameters. The remaining columns show how the flow is treated by the filter. The `Action` column shows the final outcome, `Line_Content` shows which line(s) led to that action, and `Trace` shows all the lines the packet matched. In this case, the trace is not deep, but it can be quite deep for filters that reference other structures such as policy maps and object groups.

### Example 2: Test that HTTP flows cannot go from one zone to another

Now suppose we want to test that our **firewall** blocks HTTP flows that cross the boundary from one zone to another. A query like the one below can help us do that. It is testing how output filters on interfaces in the second zone treat a packet with the specified header fields when it enters the firewall through interfaces in the first zone.

The arguments to `startLocation` and `filters` below use Batfish specifiers that enable easy specification of various concepts. `enter(firewall[Ethernet0/0/2])` specifies that the packet we want to test enters 'firewall' via 'Ethernet0/0/2' (the interface in the first zone) and `outFilterOf(Ethernet0/0/3)` specifies that the filter we want to test is the out filter on 'Ethernet0/0/3' (the interface in the second zone).


```python
# Test if a host can reach the DNS server
http_flow = HeaderConstraints(srcIps="10.114.64.1",
                              dstIps="10.114.60.10",
                              applications=["http"])
answer = bf.q.testFilters(headers=http_flow,
                         startLocation="@enter(firewall[GigabitEthernet0/0/2])",
                         filters="@out(GigabitEthernet0/0/3)").answer()
show(answer.frame())
```


<style type="text/css">
#T_pybfstyle_row0_col0, #T_pybfstyle_row0_col1, #T_pybfstyle_row0_col2, #T_pybfstyle_row0_col3, #T_pybfstyle_row0_col4, #T_pybfstyle_row0_col5 {
  text-align: left;
  vertical-align: top;
}
</style>
<table id="T_pybfstyle">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_pybfstyle_level0_col0" class="col_heading level0 col0" >Node</th>
      <th id="T_pybfstyle_level0_col1" class="col_heading level0 col1" >Filter_Name</th>
      <th id="T_pybfstyle_level0_col2" class="col_heading level0 col2" >Flow</th>
      <th id="T_pybfstyle_level0_col3" class="col_heading level0 col3" >Action</th>
      <th id="T_pybfstyle_level0_col4" class="col_heading level0 col4" >Line_Content</th>
      <th id="T_pybfstyle_level0_col5" class="col_heading level0 col5" >Trace</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_pybfstyle_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_pybfstyle_row0_col0" class="data row0 col0" >firewall</td>
      <td id="T_pybfstyle_row0_col1" class="data row0 col1" >~ZONE_OUTGOING_ACL~zone-z3~</td>
      <td id="T_pybfstyle_row0_col2" class="data row0 col2" >Start Location: firewall interface=GigabitEthernet0/0/2<br>Src IP: 10.114.64.1<br>Src Port: 49152<br>Dst IP: 10.114.60.10<br>Dst Port: 80<br>IP Protocol: TCP (SYN)</td>
      <td id="T_pybfstyle_row0_col3" class="data row0 col3" >DENY</td>
      <td id="T_pybfstyle_row0_col4" class="data row0 col4" >no-match</td>
      <td id="T_pybfstyle_row0_col5" class="data row0 col5" ><ul></ul></td>
    </tr>
  </tbody>
</table>



As we can see the HTTP flow is indeed denied, and the columns in the table show the reason for that denial.

## `searchFilters`: Verifying how filters treat a (very large) space of flows

While `testFilters` reasons about individual flows, the `searchFilters` question provides comprehensive guarantees by reasoning about (potentially very large) spaces of flows. The space of flows is specified using source and destination prefixes (where the default prefix 0.0.0.0/0 denotes all 4,294,967,296 possibilities), a list of protocols, a range of ports, and so on. Given a flow space and a match condition, which can be 'permit', 'deny', or 'matchLine <linenum>', `searchFilters` returns flows within this space that match the condition. If no flow is returned, it is guaranteed that no flow in the entire space satisfies the condition. 

### Example 1: Verify that *all* hosts in a subnet can reach the DNS server

Earlier we checked that a subnet could reach the DNS server using `testFilters` with a representative source IP address. Now, let's use `searchfilter` to ascertain that the entire subnet can reach the server.

The query below is asking if there is *any* flow from 10.10.10.0/24 to 218.8.104.58 that is *denied* by the filter **acl_in**. That is, we're asking for violations of the desired policy. An empty result means the policy is correctly implemented. Any flow returned by the query demonstrates that the policy is not correctly implemented.


```python
# Check if the subnet can reach the DNS server
dns_traffic = HeaderConstraints(srcIps="10.10.10.0/24",
                                dstIps="218.8.104.58",
                                applications=["dns"])
answer = bf.q.searchFilters(headers=dns_traffic,
                           action="deny",
                           filters="acl_in").answer()
show(answer.frame())
```


<style type="text/css">
#T_pybfstyle_row0_col0, #T_pybfstyle_row0_col1, #T_pybfstyle_row0_col2, #T_pybfstyle_row0_col3, #T_pybfstyle_row0_col4, #T_pybfstyle_row0_col5 {
  text-align: left;
  vertical-align: top;
}
</style>
<table id="T_pybfstyle">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_pybfstyle_level0_col0" class="col_heading level0 col0" >Node</th>
      <th id="T_pybfstyle_level0_col1" class="col_heading level0 col1" >Filter_Name</th>
      <th id="T_pybfstyle_level0_col2" class="col_heading level0 col2" >Flow</th>
      <th id="T_pybfstyle_level0_col3" class="col_heading level0 col3" >Action</th>
      <th id="T_pybfstyle_level0_col4" class="col_heading level0 col4" >Line_Content</th>
      <th id="T_pybfstyle_level0_col5" class="col_heading level0 col5" >Trace</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_pybfstyle_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_pybfstyle_row0_col0" class="data row0 col0" >rtr-with-acl</td>
      <td id="T_pybfstyle_row0_col1" class="data row0 col1" >acl_in</td>
      <td id="T_pybfstyle_row0_col2" class="data row0 col2" >Start Location: rtr-with-acl<br>Src IP: 10.10.10.42<br>Src Port: 49152<br>Dst IP: 218.8.104.58<br>Dst Port: 53<br>IP Protocol: UDP</td>
      <td id="T_pybfstyle_row0_col3" class="data row0 col3" >DENY</td>
      <td id="T_pybfstyle_row0_col4" class="data row0 col4" >460 deny udp 10.10.10.42/32 218.8.104.58/32 eq domain</td>
      <td id="T_pybfstyle_row0_col5" class="data row0 col5" ><ul><li>Matched line 460 deny udp 10.10.10.42/32 218.8.104.58/32 eq domain</li></ul></td>
    </tr>
  </tbody>
</table>



As we can see, we did get a flow that matches the search condition and thus violates our desired guarantee of the entire subnet being able to reach the DNS server. The columns carry the same information as those for `testFilters` and provide insight into the violation. In particular, we see that a flow with source IP 10.10.10.42 is denied by an earlier line in the ACL. Such needles in the haystack are impossible to find with tools like pen testing. 

### Example 2: Verify that the *only* TCP traffic that can go from one zone to another is NFS traffic 

In the second example for `testFilters` we used an example flow to test if **firewall** denied HTTP flows from one zone to another. Now, suppose that we wanted a stricter condition—that only TCP-based NFS flows are allowed from one zone to another. With `searchFilters` we can verify this condition by searching for violations in the large space of non-NFS flows, as below.


```python
# Check if any non-NFS, TCP flow can go from one zone to another
non_nfs_tcp_traffic = HeaderConstraints(srcIps="101.164.101.231",
                                        dstIps="101.164.9.0/24",
                                        ipProtocols=["tcp"],
                                        dstPorts="!2049")  # exclude NFS port (2049)
answer = bf.q.searchFilters(headers=non_nfs_tcp_traffic,
                           startLocation="@enter(firewall[GigabitEthernet0/0/2])",
                           filters="@out(GigabitEthernet0/0/3)",
                           action="permit").answer()
show(answer.frame())
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe tex2jax_ignore">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Node</th>
      <th>Filter_Name</th>
      <th>Flow</th>
      <th>Action</th>
      <th>Line_Content</th>
      <th>Trace</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>


Since we got back an empty answer, we can be certain that no non-NFS flow can go from one zone to another. 

*Such strong guarantees are impossible with any other tool today.*

## `filterLineReachability`: Analyzing reachability of filter lines 

When debugging or editing filters, it can be useful to confirm that every line is reachable—that is, each line can match some packets that do not match earlier lines. Unreachable filter lines are often symptomatic of bugs and past edits that did not achieve policy intent. Even when they do not represent bugs, they represent opportunities to reduce the length of the filter. 

The `filterLineReachability` question identifies unreachable filter lines. Given no parameters, it will check every filter in the network, but its scope can be narrowed  using `filters` and `nodes` parameters (see [documentation](https://pybatfish.readthedocs.io/en/latest/notebooks/filters.html#Filter-Line-Reachability)).


```python
# Find unreachable lines in filters of rtr-with-acl
aclAns = bf.q.filterLineReachability(nodes="rtr-with-acl").answer()
show(aclAns.frame().sort_values(by="Unreachable_Line"))
```


<style type="text/css">
#T_pybfstyle_row0_col0, #T_pybfstyle_row0_col1, #T_pybfstyle_row0_col2, #T_pybfstyle_row0_col3, #T_pybfstyle_row0_col4, #T_pybfstyle_row0_col5, #T_pybfstyle_row0_col6, #T_pybfstyle_row1_col0, #T_pybfstyle_row1_col1, #T_pybfstyle_row1_col2, #T_pybfstyle_row1_col3, #T_pybfstyle_row1_col4, #T_pybfstyle_row1_col5, #T_pybfstyle_row1_col6 {
  text-align: left;
  vertical-align: top;
}
</style>
<table id="T_pybfstyle">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_pybfstyle_level0_col0" class="col_heading level0 col0" >Sources</th>
      <th id="T_pybfstyle_level0_col1" class="col_heading level0 col1" >Unreachable_Line</th>
      <th id="T_pybfstyle_level0_col2" class="col_heading level0 col2" >Unreachable_Line_Action</th>
      <th id="T_pybfstyle_level0_col3" class="col_heading level0 col3" >Blocking_Lines</th>
      <th id="T_pybfstyle_level0_col4" class="col_heading level0 col4" >Different_Action</th>
      <th id="T_pybfstyle_level0_col5" class="col_heading level0 col5" >Reason</th>
      <th id="T_pybfstyle_level0_col6" class="col_heading level0 col6" >Additional_Info</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_pybfstyle_level0_row0" class="row_heading level0 row0" >1</th>
      <td id="T_pybfstyle_row0_col0" class="data row0 col0" >rtr-with-acl: acl_in</td>
      <td id="T_pybfstyle_row0_col1" class="data row0 col1" >670 permit ip 166.146.58.184 any</td>
      <td id="T_pybfstyle_row0_col2" class="data row0 col2" >PERMIT</td>
      <td id="T_pybfstyle_row0_col3" class="data row0 col3" >540 deny ip 166.144.0.0/12 any</td>
      <td id="T_pybfstyle_row0_col4" class="data row0 col4" >True</td>
      <td id="T_pybfstyle_row0_col5" class="data row0 col5" >BLOCKING_LINES</td>
      <td id="T_pybfstyle_row0_col6" class="data row0 col6" >None</td>
    </tr>
    <tr>
      <th id="T_pybfstyle_level0_row1" class="row_heading level0 row1" >0</th>
      <td id="T_pybfstyle_row1_col0" class="data row1 col0" >rtr-with-acl: acl_in</td>
      <td id="T_pybfstyle_row1_col1" class="data row1 col1" >790 deny ip 54.203.159.1/32 any</td>
      <td id="T_pybfstyle_row1_col2" class="data row1 col2" >DENY</td>
      <td id="T_pybfstyle_row1_col3" class="data row1 col3" >500 deny ip 54.0.0.0/8 any</td>
      <td id="T_pybfstyle_row1_col4" class="data row1 col4" >False</td>
      <td id="T_pybfstyle_row1_col5" class="data row1 col5" >BLOCKING_LINES</td>
      <td id="T_pybfstyle_row1_col6" class="data row1 col6" >None</td>
    </tr>
  </tbody>
</table>



Each line in the answer above identifies an unreachable line in a filter. Let's take a closer look at the first one. It shows that the line `670 permit ip 166.146.58.184 any` is unreachable because it is blocked by the line `540` shown in the `Blocking_Lines` column. The `Different_Action` column indicates that the blocking line `540` has the opposite action as the blocked line `670`, a more worrisome situation than if actions were the same.

The `Reason` column shows that the line is unreachable because of it has other lines that block it, Lines can also be independently unreachable (i.e., no packet will ever match it) or may be unreachable because of circular references. The `filterLineReachability` question identifies such cases as well, and provides more information about them in the `Additional_Info` column.

## Summary

In this notebook, we showed how you can use Batfish to: 
  1. Test how filters in the network treat a flow (`testFilters`)
  2. Verify how filters treat a large space of flows (`searchFilters`)
  3. Find filter lines that will never match any packet (`filterLineReachability`)

If you found these capabilities useful, check out our ["Provably Safe ACL and Firewall Changes" notebook](https://github.com/batfish/pybatfish/blob/master/jupyter_notebooks/Provably%20Safe%20ACL%20and%20Firewall%20Changes.ipynb) that shows how to change filters in a *provably* safe manner.

***
### Get involved with the Batfish community

Join our community on [Slack](https://join.slack.com/t/batfish-org/shared_invite/enQtMzA0Nzg2OTAzNzQ1LTcyYzY3M2Q0NWUyYTRhYjdlM2IzYzRhZGU1NWFlNGU2MzlhNDY3OTJmMDIyMjQzYmRlNjhkMTRjNWIwNTUwNTQ) and [GitHub](https://github.com/batfish/batfish). 
