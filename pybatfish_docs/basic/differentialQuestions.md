```python
import pandas as pd
from pybatfish.client.session import Session
from pybatfish.datamodel import *

pd.set_option("display.width", 300) 
pd.set_option("display.max_columns", 30) 
pd.set_option("display.max_rows", 1000) 
pd.set_option("display.max_colwidth", None)

# Configure all pybatfish loggers to use WARN level
import logging
logging.getLogger('pybatfish').setLevel(logging.WARN)
```


```python
bf = Session(host="localhost")


```

#### Differential Questions

Differential questions enable you to discover configuration and
behavior differences between two snapshot of the network.

Most of the Batfish questions can be run differentially by using
`snapshot=<current snapshot>` and `reference_snapshot=<reference snapshot>`
parameters in `.answer()`. For example, to view routing
table differences between `snapshot1` and `snapshot0`, run
`bf.q.routes().answer(snapshot="snapshot1", reference_snapshot="snapshot0")`.

Batfish also has two questions that are exclusively differential.


* [Compare Filters](#Compare-Filters)
* [Differential Reachability](#Differential-Reachability)


```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('filters-change')
```




    'filters-change'



##### Compare Filters

Compares filters with the same name in the current and reference snapshots. Returns pairs of lines, one from each filter, that match the same flow(s) but treat them differently (i.e. one permits and the other denies the flow).

This question can be used to summarize how a filter has changed over time. In particular, it highlights differences that cause flows to be denied when they used to be permitted, or vice versa. The output is a table that includes pairs of lines, one from each version of the filter, that both match at least one common flow, and have different action (permit or deny). This is a differential question and the reference snapshot to compare against must be provided in the call to answer().

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Only evaluate filters present on nodes matching this node specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
filters | Only evaluate filters that match this filter specifier. | [FilterSpec](../specifiers.md#filter-specifier) | True | 
ignoreComposites | Whether to ignore filters that are composed of multiple filters defined in the configs. | bool | True | False

###### **Invocation**


```python
result = bf.q.compareFilters(nodes='rtr-with-acl').answer(snapshot='filters-change',reference_snapshot='filters').frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Hostname. | str
Filter_Name | The filter name. | str
Line_Index | The index of the line in the current filter. | str
Line_Content | The current filter line content. | str
Line_Action | The current filter line action. | str
Reference_Line_Index | The index of the line in the reference filter. | str
Reference_Line_Content | The reference filter line content. | str

Print the first 5 rows of the returned Dataframe


```python
result.head(5)
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
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Node</th>
      <th>Filter_Name</th>
      <th>Line_Index</th>
      <th>Line_Content</th>
      <th>Line_Action</th>
      <th>Reference_Line_Index</th>
      <th>Reference_Line_Content</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>rtr-with-acl</td>
      <td>acl_in</td>
      <td>23</td>
      <td>462 permit tcp 10.10.10.0/24 18.18.18.0/26 eq 80</td>
      <td>PERMIT</td>
      <td>101</td>
      <td>2020 deny tcp any any</td>
    </tr>
    <tr>
      <th>1</th>
      <td>rtr-with-acl</td>
      <td>acl_in</td>
      <td>24</td>
      <td>463 permit tcp 10.10.10.0/24 18.18.18.0/26 eq 8080</td>
      <td>PERMIT</td>
      <td>101</td>
      <td>2020 deny tcp any any</td>
    </tr>
  </tbody>
</table>
</div>




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('forwarding-change')
```




    'forwarding-change'



##### Differential Reachability

Returns flows that are successful in one snapshot but not in another.

Searches across all possible flows in the network, with the specified header and path constraints, and returns example flows that are successful in one snapshot and not the other. This is a differential question and the reference snapshot to compare against must be provided in the call to answer().

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
pathConstraints | Constraint the path a flow can take (start/end/transit locations). | [PathConstraints](../datamodel.rst#pybatfish.datamodel.flow.PathConstraints) | True | 
headers | Packet header constraints. | [HeaderConstraints](../datamodel.rst#pybatfish.datamodel.flow.HeaderConstraints) | True | 
actions | Only return flows for which the disposition is from this set. | [DispositionSpec](../specifiers.md#disposition-specifier) | True | success
maxTraces | Limit the number of traces returned. | int | True | 
invertSearch | Search for packet headers outside the specified headerspace, rather than inside the space. | bool | True | 
ignoreFilters | Do not apply filters/ACLs during analysis. | bool | True | False

###### **Invocation**


```python
result = bf.q.differentialReachability().answer(snapshot='forwarding-change',reference_snapshot='forwarding').frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Flow | The flow | [Flow](../datamodel.rst#pybatfish.datamodel.flow.Flow)
Snapshot_Traces | The traces in the BASE snapshot | Set of [Trace](../datamodel.rst#pybatfish.datamodel.flow.Trace)
Snapshot_TraceCount | The total number traces in the BASE snapshot | int
Reference_Traces | The traces in the DELTA snapshot | Set of [Trace](../datamodel.rst#pybatfish.datamodel.flow.Trace)
Reference_TraceCount | The total number traces in the DELTA snapshot | int

Print the first 5 rows of the returned Dataframe


```python
result.head(5)
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
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Flow</th>
      <th>Snapshot_Traces</th>
      <th>Snapshot_TraceCount</th>
      <th>Reference_Traces</th>
      <th>Reference_TraceCount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>start=border1 [10.12.11.2:49152-&gt;2.128.1.1:33434 UDP]</td>
      <td>[((ORIGINATED(default), FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.12.12.2, Routes: [ibgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet2/0)), (RECEIVED(GigabitEthernet1/0), NULL_ROUTED(Discarded, Routes: [static (Network: 2.128.1.1/32, Next Hop: discard)])))]</td>
      <td>1</td>
      <td>[((ORIGINATED(default), FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.11.2, Routes: [ibgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet1/0)), (RECEIVED(GigabitEthernet0/0), FORWARDED(Forwarded out interface: GigabitEthernet3/0 with resolved next-hop IP: 2.23.12.3, Routes: [ibgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet3/0)), (RECEIVED(GigabitEthernet1/0), FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.34.201.4, Routes: [bgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet2/0)), (RECEIVED(GigabitEthernet1/0), PERMITTED(RESTRICT_NETWORK_TRAFFIC_IN (INGRESS_FILTER)), FORWARDED(Forwarded out interface: GigabitEthernet3/0, Routes: [connected (Network: 2.128.1.0/30, Next Hop: interface GigabitEthernet3/0)]), PERMITTED(RESTRICT_HOST_TRAFFIC_OUT (EGRESS_FILTER)), TRANSMITTED(GigabitEthernet3/0)), (RECEIVED(eth0), ACCEPTED(eth0)))]</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>start=border1 interface=GigabitEthernet0/0 [10.12.11.1:49152-&gt;2.128.1.1:33434 UDP]</td>
      <td>[((RECEIVED(GigabitEthernet0/0), PERMITTED(OUTSIDE_TO_INSIDE (INGRESS_FILTER)), FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.12.12.2, Routes: [ibgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet2/0)), (RECEIVED(GigabitEthernet1/0), NULL_ROUTED(Discarded, Routes: [static (Network: 2.128.1.1/32, Next Hop: discard)])))]</td>
      <td>1</td>
      <td>[((RECEIVED(GigabitEthernet0/0), PERMITTED(OUTSIDE_TO_INSIDE (INGRESS_FILTER)), FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.11.2, Routes: [ibgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet1/0)), (RECEIVED(GigabitEthernet0/0), FORWARDED(Forwarded out interface: GigabitEthernet3/0 with resolved next-hop IP: 2.23.12.3, Routes: [ibgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet3/0)), (RECEIVED(GigabitEthernet1/0), FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.34.201.4, Routes: [bgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet2/0)), (RECEIVED(GigabitEthernet1/0), PERMITTED(RESTRICT_NETWORK_TRAFFIC_IN (INGRESS_FILTER)), FORWARDED(Forwarded out interface: GigabitEthernet3/0, Routes: [connected (Network: 2.128.1.0/30, Next Hop: interface GigabitEthernet3/0)]), PERMITTED(RESTRICT_HOST_TRAFFIC_OUT (EGRESS_FILTER)), TRANSMITTED(GigabitEthernet3/0)), (RECEIVED(eth0), ACCEPTED(eth0)))]</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>start=border1 interface=GigabitEthernet1/0 [2.12.11.3:49152-&gt;2.128.1.1:33434 UDP]</td>
      <td>[((RECEIVED(GigabitEthernet1/0), FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.12.12.2, Routes: [ibgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet2/0)), (RECEIVED(GigabitEthernet1/0), NULL_ROUTED(Discarded, Routes: [static (Network: 2.128.1.1/32, Next Hop: discard)])))]</td>
      <td>1</td>
      <td>[((RECEIVED(GigabitEthernet1/0), FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.11.2, Routes: [ibgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet1/0)), (RECEIVED(GigabitEthernet0/0), FORWARDED(Forwarded out interface: GigabitEthernet3/0 with resolved next-hop IP: 2.23.12.3, Routes: [ibgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet3/0)), (RECEIVED(GigabitEthernet1/0), FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.34.201.4, Routes: [bgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet2/0)), (RECEIVED(GigabitEthernet1/0), PERMITTED(RESTRICT_NETWORK_TRAFFIC_IN (INGRESS_FILTER)), FORWARDED(Forwarded out interface: GigabitEthernet3/0, Routes: [connected (Network: 2.128.1.0/30, Next Hop: interface GigabitEthernet3/0)]), PERMITTED(RESTRICT_HOST_TRAFFIC_OUT (EGRESS_FILTER)), TRANSMITTED(GigabitEthernet3/0)), (RECEIVED(eth0), ACCEPTED(eth0)))]</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>start=border1 interface=GigabitEthernet2/0 [2.12.12.3:49152-&gt;2.128.1.1:33434 UDP]</td>
      <td>[((RECEIVED(GigabitEthernet2/0), FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.12.12.2, Routes: [ibgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet2/0)), (RECEIVED(GigabitEthernet1/0), NULL_ROUTED(Discarded, Routes: [static (Network: 2.128.1.1/32, Next Hop: discard)])))]</td>
      <td>1</td>
      <td>[((RECEIVED(GigabitEthernet2/0), FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.11.2, Routes: [ibgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet1/0)), (RECEIVED(GigabitEthernet0/0), FORWARDED(Forwarded out interface: GigabitEthernet3/0 with resolved next-hop IP: 2.23.12.3, Routes: [ibgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet3/0)), (RECEIVED(GigabitEthernet1/0), FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.34.201.4, Routes: [bgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet2/0)), (RECEIVED(GigabitEthernet1/0), PERMITTED(RESTRICT_NETWORK_TRAFFIC_IN (INGRESS_FILTER)), FORWARDED(Forwarded out interface: GigabitEthernet3/0, Routes: [connected (Network: 2.128.1.0/30, Next Hop: interface GigabitEthernet3/0)]), PERMITTED(RESTRICT_HOST_TRAFFIC_OUT (EGRESS_FILTER)), TRANSMITTED(GigabitEthernet3/0)), (RECEIVED(eth0), ACCEPTED(eth0)))]</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>start=border2 [10.23.21.2:49152-&gt;2.128.1.1:33434 UDP]</td>
      <td>[((ORIGINATED(default), FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.22.2, Routes: [ibgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet1/0)), (RECEIVED(GigabitEthernet0/0), NULL_ROUTED(Discarded, Routes: [static (Network: 2.128.1.1/32, Next Hop: discard)])))]</td>
      <td>1</td>
      <td>[((ORIGINATED(default), FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.12.21.2, Routes: [ibgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet2/0)), (RECEIVED(GigabitEthernet1/0), FORWARDED(Forwarded out interface: GigabitEthernet3/0 with resolved next-hop IP: 2.23.12.3, Routes: [ibgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet3/0)), (RECEIVED(GigabitEthernet1/0), FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.34.201.4, Routes: [bgp (Network: 2.128.1.0/30, Next Hop: ip 2.34.201.4)]), TRANSMITTED(GigabitEthernet2/0)), (RECEIVED(GigabitEthernet1/0), PERMITTED(RESTRICT_NETWORK_TRAFFIC_IN (INGRESS_FILTER)), FORWARDED(Forwarded out interface: GigabitEthernet3/0, Routes: [connected (Network: 2.128.1.0/30, Next Hop: interface GigabitEthernet3/0)]), PERMITTED(RESTRICT_HOST_TRAFFIC_OUT (EGRESS_FILTER)), TRANSMITTED(GigabitEthernet3/0)), (RECEIVED(eth0), ACCEPTED(eth0)))]</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>


