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

#### Packet Forwarding

This category of questions allows you to query how different types of
traffic is forwarded by the network and if endpoints are able to
communicate. You can analyze these aspects in a few different ways.


* [Traceroute](#Traceroute)
* [Bi-directional Traceroute](#Bi-directional-Traceroute)
* [Reachability](#Reachability)
* [Bi-directional Reachability](#Bi-directional-Reachability)
* [Loop detection](#Loop-detection)
* [Multipath Consistency for host-subnets](#Multipath-Consistency-for-host-subnets)
* [Multipath Consistency for router loopbacks](#Multipath-Consistency-for-router-loopbacks)


```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Traceroute

Traces the path(s) for the specified flow.

Performs a virtual traceroute in the network from a starting node. A destination IP and ingress (source) node must be specified. Other IP headers are given default values if unspecified.
Unlike a real traceroute, this traceroute is directional. That is, for it to succeed, the reverse connectivity is not needed. This feature can help debug connectivity issues by decoupling the two directions.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
startLocation | Location (node and interface combination) to start tracing from. | [LocationSpec](../specifiers.md#location-specifier) | False | 
headers | Packet header constraints. | [HeaderConstraints](../datamodel.rst#pybatfish.datamodel.flow.HeaderConstraints) | False | 
maxTraces | Limit the number of traces returned. | int | True | 
ignoreFilters | If set, filters/ACLs encountered along the path are ignored. | bool | True | 

###### **Invocation**


```python
result = bf.q.traceroute(startLocation='@enter(as2border1[GigabitEthernet2/0])', headers=HeaderConstraints(dstIps='2.34.201.10', srcIps='8.8.8.8')).answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Flow | The flow | [Flow](../datamodel.rst#pybatfish.datamodel.flow.Flow)
Traces | The traces for this flow | Set of [Trace](../datamodel.rst#pybatfish.datamodel.flow.Trace)
TraceCount | The total number traces for this flow | int

Retrieving the flow definition


```python
result.Flow
```




    0    start=as2border1 interface=GigabitEthernet2/0 [8.8.8.8:49152->2.34.201.10:33434 UDP]
    Name: Flow, dtype: object



Retrieving the detailed Trace information


```python
len(result.Traces)
```




    1




```python
result.Traces[0]
```




<span style="color:#019612; text-weight:bold;">DELIVERED_TO_SUBNET</span><br><strong>1</strong>. node: as2border1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.11.2, Routes: [ospfE2 (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet1/0 ip 2.12.11.2)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>2</strong>. node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet3/0 with resolved next-hop IP: 2.23.12.3, Routes: [ospfE2 (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet3/0 ip 2.23.12.3)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet3/0)<br><strong>3</strong>. node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0, Routes: [connected (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet2/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br>&nbsp;&nbsp;DELIVERED_TO_SUBNET(Output Interface: GigabitEthernet2/0, Resolved Next Hop IP: 2.34.201.10)<br><br><span style="color:#019612; text-weight:bold;">DELIVERED_TO_SUBNET</span><br><strong>1</strong>. node: as2border1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.12.12.2, Routes: [ospfE2 (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet2/0 ip 2.12.12.2)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>2</strong>. node: as2core2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.23.22.3, Routes: [ospfE2 (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet2/0 ip 2.23.22.3)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>3</strong>. node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0, Routes: [connected (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet2/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br>&nbsp;&nbsp;DELIVERED_TO_SUBNET(Output Interface: GigabitEthernet2/0, Resolved Next Hop IP: 2.34.201.10)



Evaluating the first Trace


```python
result.Traces[0][0]
```




<span style="color:#019612; text-weight:bold;">DELIVERED_TO_SUBNET</span><br><strong>1</strong>. node: as2border1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.11.2, Routes: [ospfE2 (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet1/0 ip 2.12.11.2)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>2</strong>. node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet3/0 with resolved next-hop IP: 2.23.12.3, Routes: [ospfE2 (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet3/0 ip 2.23.12.3)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet3/0)<br><strong>3</strong>. node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0, Routes: [connected (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet2/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br>&nbsp;&nbsp;DELIVERED_TO_SUBNET(Output Interface: GigabitEthernet2/0, Resolved Next Hop IP: 2.34.201.10)



Retrieving the disposition of the first Trace


```python
result.Traces[0][0].disposition
```




    'DELIVERED_TO_SUBNET'



Retrieving the first hop of the first Trace


```python
result.Traces[0][0][0]
```




node: as2border1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.11.2, Routes: [ospfE2 (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet1/0 ip 2.12.11.2)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)



Retrieving the last hop of the first Trace


```python
result.Traces[0][0][-1]
```




node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0, Routes: [connected (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet2/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br>&nbsp;&nbsp;DELIVERED_TO_SUBNET(Output Interface: GigabitEthernet2/0, Resolved Next Hop IP: 2.34.201.10)




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Bi-directional Traceroute

Traces the path(s) for the specified flow, along with path(s) for reverse flows.

This question performs a virtual traceroute in the network from a starting node. A destination IP and ingress (source) node must be specified. Other IP headers are given default values if unspecified.
If the trace succeeds, a traceroute is performed in the reverse direction.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
startLocation | Location (node and interface combination) to start tracing from. | [LocationSpec](../specifiers.md#location-specifier) | False | 
headers | Packet header constraints. | [HeaderConstraints](../datamodel.rst#pybatfish.datamodel.flow.HeaderConstraints) | False | 
maxTraces | Limit the number of traces returned. | int | True | 
ignoreFilters | If set, filters/ACLs encountered along the path are ignored. | bool | True | 

###### **Invocation**


```python
result = bf.q.bidirectionalTraceroute(startLocation='@enter(as2border1[GigabitEthernet2/0])', headers=HeaderConstraints(dstIps='2.34.201.10', srcIps='8.8.8.8')).answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Forward_Flow | The forward flow. | [Flow](../datamodel.rst#pybatfish.datamodel.flow.Flow)
Forward_Traces | The forward traces. | List of [Trace](../datamodel.rst#pybatfish.datamodel.flow.Trace)
New_Sessions | Sessions initialized by the forward trace. | List of str
Reverse_Flow | The reverse flow. | [Flow](../datamodel.rst#pybatfish.datamodel.flow.Flow)
Reverse_Traces | The reverse traces. | List of [Trace](../datamodel.rst#pybatfish.datamodel.flow.Trace)

Retrieving the Forward flow definition


```python
result.Forward_Flow
```




    0    start=as2border1 interface=GigabitEthernet2/0 [8.8.8.8:49152->2.34.201.10:33434 UDP]
    Name: Forward_Flow, dtype: object



Retrieving the detailed Forward Trace information


```python
len(result.Forward_Traces)
```




    1




```python
result.Forward_Traces[0]
```




<span style="color:#019612; text-weight:bold;">DELIVERED_TO_SUBNET</span><br><strong>1</strong>. node: as2border1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.11.2, Routes: [ospfE2 (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet1/0 ip 2.12.11.2)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>2</strong>. node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet3/0 with resolved next-hop IP: 2.23.12.3, Routes: [ospfE2 (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet3/0 ip 2.23.12.3)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet3/0)<br><strong>3</strong>. node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0, Routes: [connected (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet2/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br>&nbsp;&nbsp;DELIVERED_TO_SUBNET(Output Interface: GigabitEthernet2/0, Resolved Next Hop IP: 2.34.201.10)<br><br><span style="color:#019612; text-weight:bold;">DELIVERED_TO_SUBNET</span><br><strong>1</strong>. node: as2border1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.12.12.2, Routes: [ospfE2 (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet2/0 ip 2.12.12.2)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>2</strong>. node: as2core2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.23.22.3, Routes: [ospfE2 (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet2/0 ip 2.23.22.3)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>3</strong>. node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0, Routes: [connected (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet2/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br>&nbsp;&nbsp;DELIVERED_TO_SUBNET(Output Interface: GigabitEthernet2/0, Resolved Next Hop IP: 2.34.201.10)



Evaluating the first Forward Trace


```python
result.Forward_Traces[0][0]
```




<span style="color:#019612; text-weight:bold;">DELIVERED_TO_SUBNET</span><br><strong>1</strong>. node: as2border1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.11.2, Routes: [ospfE2 (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet1/0 ip 2.12.11.2)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>2</strong>. node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet3/0 with resolved next-hop IP: 2.23.12.3, Routes: [ospfE2 (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet3/0 ip 2.23.12.3)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet3/0)<br><strong>3</strong>. node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0, Routes: [connected (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet2/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br>&nbsp;&nbsp;DELIVERED_TO_SUBNET(Output Interface: GigabitEthernet2/0, Resolved Next Hop IP: 2.34.201.10)



Retrieving the disposition of the first Forward Trace


```python
result.Forward_Traces[0][0].disposition
```




    'DELIVERED_TO_SUBNET'



Retrieving the first hop of the first Forward Trace


```python
result.Forward_Traces[0][0][0]
```




node: as2border1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.11.2, Routes: [ospfE2 (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet1/0 ip 2.12.11.2)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)



Retrieving the last hop of the first Forward Trace


```python
result.Forward_Traces[0][0][-1]
```




node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0, Routes: [connected (Network: 2.34.201.0/24, Next Hop: interface GigabitEthernet2/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br>&nbsp;&nbsp;DELIVERED_TO_SUBNET(Output Interface: GigabitEthernet2/0, Resolved Next Hop IP: 2.34.201.10)



Retrieving the Return flow definition


```python
result.Reverse_Flow
```




    0    start=as2dist2 interface=GigabitEthernet2/0 [2.34.201.10:33434->8.8.8.8:49152 UDP]
    Name: Reverse_Flow, dtype: object



Retrieving the detailed Return Trace information


```python
len(result.Reverse_Traces)
```




    1




```python
result.Reverse_Traces[0]
```




<span style="color:#7c020e; text-weight:bold;">NO_ROUTE</span><br><strong>1</strong>. node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;NO_ROUTE(Discarded)



Evaluating the first Reverse Trace


```python
result.Reverse_Traces[0][0]
```




<span style="color:#7c020e; text-weight:bold;">NO_ROUTE</span><br><strong>1</strong>. node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;NO_ROUTE(Discarded)



Retrieving the disposition of the first Reverse Trace


```python
result.Reverse_Traces[0][0].disposition
```




    'NO_ROUTE'



Retrieving the first hop of the first Reverse Trace


```python
result.Reverse_Traces[0][0][0]
```




node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;NO_ROUTE(Discarded)



Retrieving the last hop of the first Reverse Trace


```python
result.Reverse_Traces[0][0][-1]
```




node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;NO_ROUTE(Discarded)




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Reachability

Finds flows that match the specified path and header space conditions.

Searches across all flows that match the specified conditions and returns examples of such flows. This question can be used to ensure that certain services are globally accessible and parts of the network are perfectly isolated from each other.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
pathConstraints | Constraint the path a flow can take (start/end/transit locations). | [PathConstraints](../datamodel.rst#pybatfish.datamodel.flow.PathConstraints) | True | 
headers | Packet header constraints. | [HeaderConstraints](../datamodel.rst#pybatfish.datamodel.flow.HeaderConstraints) | True | 
actions | Only return flows for which the disposition is from this set. | [DispositionSpec](../specifiers.md#disposition-specifier) | True | success
maxTraces | Limit the number of traces returned. | int | True | 
invertSearch | Search for packet headers outside the specified headerspace, rather than inside the space. | bool | True | 
ignoreFilters | Do not apply filters/ACLs during analysis. | bool | True | 

###### **Invocation**


```python
result = bf.q.reachability(pathConstraints=PathConstraints(startLocation = '/as2/'), headers=HeaderConstraints(dstIps='host1', srcIps='0.0.0.0/0', applications='DNS'), actions='SUCCESS').answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Flow | The flow | [Flow](../datamodel.rst#pybatfish.datamodel.flow.Flow)
Traces | The traces for this flow | Set of [Trace](../datamodel.rst#pybatfish.datamodel.flow.Trace)
TraceCount | The total number traces for this flow | int

Retrieving the flow definition


```python
result.Flow
```




    0    start=as2border1 [10.0.0.0:49152->2.128.0.101:53 UDP]
    1    start=as2border2 [10.0.0.0:49152->2.128.0.101:53 UDP]
    2      start=as2core1 [10.0.0.0:49152->2.128.0.101:53 UDP]
    3      start=as2core2 [10.0.0.0:49152->2.128.0.101:53 UDP]
    4      start=as2dept1 [10.0.0.0:49152->2.128.0.101:53 UDP]
    5      start=as2dist1 [10.0.0.0:49152->2.128.0.101:53 UDP]
    6      start=as2dist2 [10.0.0.0:49152->2.128.0.101:53 UDP]
    Name: Flow, dtype: object



Retrieving the detailed Trace information


```python
len(result.Traces)
```




    7




```python
result.Traces[0]
```




<span style="color:#019612; text-weight:bold;">ACCEPTED</span><br><strong>1</strong>. node: as2border1<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.11.2, Routes: [ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.101.4),ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.201.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>2</strong>. node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.23.11.3, Routes: [ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.101.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>3</strong>. node: as2dist1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.34.101.4, Routes: [bgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.101.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>4</strong>. node: as2dept1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0, Routes: [connected (Network: 2.128.0.0/24, Next Hop: interface GigabitEthernet2/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>5</strong>. node: host1<br>&nbsp;&nbsp;RECEIVED(eth0)<br>&nbsp;&nbsp;PERMITTED(filter::INPUT (INGRESS_FILTER))<br>&nbsp;&nbsp;ACCEPTED(eth0)<br><br><span style="color:#019612; text-weight:bold;">ACCEPTED</span><br><strong>1</strong>. node: as2border1<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.11.2, Routes: [ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.101.4),ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.201.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>2</strong>. node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet3/0 with resolved next-hop IP: 2.23.12.3, Routes: [ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.201.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet3/0)<br><strong>3</strong>. node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.34.201.4, Routes: [bgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.201.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>4</strong>. node: as2dept1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0, Routes: [connected (Network: 2.128.0.0/24, Next Hop: interface GigabitEthernet2/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>5</strong>. node: host1<br>&nbsp;&nbsp;RECEIVED(eth0)<br>&nbsp;&nbsp;PERMITTED(filter::INPUT (INGRESS_FILTER))<br>&nbsp;&nbsp;ACCEPTED(eth0)<br><br><span style="color:#019612; text-weight:bold;">ACCEPTED</span><br><strong>1</strong>. node: as2border1<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.12.12.2, Routes: [ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.101.4),ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.201.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>2</strong>. node: as2core2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.23.22.3, Routes: [ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.201.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>3</strong>. node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.34.201.4, Routes: [bgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.201.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>4</strong>. node: as2dept1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0, Routes: [connected (Network: 2.128.0.0/24, Next Hop: interface GigabitEthernet2/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>5</strong>. node: host1<br>&nbsp;&nbsp;RECEIVED(eth0)<br>&nbsp;&nbsp;PERMITTED(filter::INPUT (INGRESS_FILTER))<br>&nbsp;&nbsp;ACCEPTED(eth0)<br><br><span style="color:#019612; text-weight:bold;">ACCEPTED</span><br><strong>1</strong>. node: as2border1<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.12.12.2, Routes: [ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.101.4),ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.201.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>2</strong>. node: as2core2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet3/0 with resolved next-hop IP: 2.23.21.3, Routes: [ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.101.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet3/0)<br><strong>3</strong>. node: as2dist1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.34.101.4, Routes: [bgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.101.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>4</strong>. node: as2dept1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0, Routes: [connected (Network: 2.128.0.0/24, Next Hop: interface GigabitEthernet2/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>5</strong>. node: host1<br>&nbsp;&nbsp;RECEIVED(eth0)<br>&nbsp;&nbsp;PERMITTED(filter::INPUT (INGRESS_FILTER))<br>&nbsp;&nbsp;ACCEPTED(eth0)



Evaluating the first Trace


```python
result.Traces[0][0]
```




<span style="color:#019612; text-weight:bold;">ACCEPTED</span><br><strong>1</strong>. node: as2border1<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.11.2, Routes: [ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.101.4),ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.201.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>2</strong>. node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.23.11.3, Routes: [ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.101.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>3</strong>. node: as2dist1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.34.101.4, Routes: [bgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.101.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>4</strong>. node: as2dept1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0, Routes: [connected (Network: 2.128.0.0/24, Next Hop: interface GigabitEthernet2/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>5</strong>. node: host1<br>&nbsp;&nbsp;RECEIVED(eth0)<br>&nbsp;&nbsp;PERMITTED(filter::INPUT (INGRESS_FILTER))<br>&nbsp;&nbsp;ACCEPTED(eth0)



Retrieving the disposition of the first Trace


```python
result.Traces[0][0].disposition
```




    'ACCEPTED'



Retrieving the first hop of the first Trace


```python
result.Traces[0][0][0]
```




node: as2border1<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.11.2, Routes: [ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.101.4),ibgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.201.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)



Retrieving the last hop of the first Trace


```python
result.Traces[0][0][-1]
```




node: host1<br>&nbsp;&nbsp;RECEIVED(eth0)<br>&nbsp;&nbsp;PERMITTED(filter::INPUT (INGRESS_FILTER))<br>&nbsp;&nbsp;ACCEPTED(eth0)




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Bi-directional Reachability

Searches for successfully delivered flows that can successfully receive a response.

Performs two reachability analyses, first originating from specified sources, then returning back to those sources. After the first (forward) pass, sets up sessions in the network and creates returning flows for each successfully delivered forward flow. The second pass searches for return flows that can be successfully delivered in the presence of the setup sessions.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
pathConstraints | Constraint the path a flow can take (start/end/transit locations). | [PathConstraints](../datamodel.rst#pybatfish.datamodel.flow.PathConstraints) | True | 
headers | Packet header constraints. | [HeaderConstraints](../datamodel.rst#pybatfish.datamodel.flow.HeaderConstraints) | False | 
returnFlowType | Specifies the type of return flows to search. | str | True | SUCCESS

###### **Invocation**


```python
result = bf.q.bidirectionalReachability(pathConstraints=PathConstraints(startLocation = '/as2dist1/'), headers=HeaderConstraints(dstIps='host1', srcIps='0.0.0.0/0', applications='DNS'), returnFlowType='SUCCESS').answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Forward_Flow | The forward flow. | [Flow](../datamodel.rst#pybatfish.datamodel.flow.Flow)
Forward_Traces | The forward traces. | List of [Trace](../datamodel.rst#pybatfish.datamodel.flow.Trace)
New_Sessions | Sessions initialized by the forward trace. | List of str
Reverse_Flow | The reverse flow. | [Flow](../datamodel.rst#pybatfish.datamodel.flow.Flow)
Reverse_Traces | The reverse traces. | List of [Trace](../datamodel.rst#pybatfish.datamodel.flow.Trace)

Retrieving the Forward flow definition


```python
result.Forward_Flow
```




    0    start=as2dist1 [2.34.101.3:49152->2.128.0.101:53 UDP]
    Name: Forward_Flow, dtype: object



Retrieving the detailed Forward Trace information


```python
len(result.Forward_Traces)
```




    1




```python
result.Forward_Traces[0]
```




<span style="color:#019612; text-weight:bold;">ACCEPTED</span><br><strong>1</strong>. node: as2dist1<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.34.101.4, Routes: [bgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.101.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>2</strong>. node: as2dept1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0, Routes: [connected (Network: 2.128.0.0/24, Next Hop: interface GigabitEthernet2/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>3</strong>. node: host1<br>&nbsp;&nbsp;RECEIVED(eth0)<br>&nbsp;&nbsp;PERMITTED(filter::INPUT (INGRESS_FILTER))<br>&nbsp;&nbsp;ACCEPTED(eth0)



Evaluating the first Forward Trace


```python
result.Forward_Traces[0][0]
```




<span style="color:#019612; text-weight:bold;">ACCEPTED</span><br><strong>1</strong>. node: as2dist1<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.34.101.4, Routes: [bgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.101.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>2</strong>. node: as2dept1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0, Routes: [connected (Network: 2.128.0.0/24, Next Hop: interface GigabitEthernet2/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>3</strong>. node: host1<br>&nbsp;&nbsp;RECEIVED(eth0)<br>&nbsp;&nbsp;PERMITTED(filter::INPUT (INGRESS_FILTER))<br>&nbsp;&nbsp;ACCEPTED(eth0)



Retrieving the disposition of the first Forward Trace


```python
result.Forward_Traces[0][0].disposition
```




    'ACCEPTED'



Retrieving the first hop of the first Forward Trace


```python
result.Forward_Traces[0][0][0]
```




node: as2dist1<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.34.101.4, Routes: [bgp (Network: 2.128.0.0/24, Next Hop: ip 2.34.101.4)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)



Retrieving the last hop of the first Forward Trace


```python
result.Forward_Traces[0][0][-1]
```




node: host1<br>&nbsp;&nbsp;RECEIVED(eth0)<br>&nbsp;&nbsp;PERMITTED(filter::INPUT (INGRESS_FILTER))<br>&nbsp;&nbsp;ACCEPTED(eth0)



Retrieving the Return flow definition


```python
result.Reverse_Flow
```




    0    start=host1 [2.128.0.101:53->2.34.101.3:49152 UDP]
    Name: Reverse_Flow, dtype: object



Retrieving the detailed Return Trace information


```python
len(result.Reverse_Traces)
```




    1




```python
result.Reverse_Traces[0]
```




<span style="color:#019612; text-weight:bold;">ACCEPTED</span><br><strong>1</strong>. node: host1<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: eth0 with resolved next-hop IP: 2.128.0.1, Routes: [static (Network: 0.0.0.0/0, Next Hop: interface eth0 ip 2.128.0.1)])<br>&nbsp;&nbsp;PERMITTED(filter::OUTPUT (EGRESS_FILTER))<br>&nbsp;&nbsp;TRANSMITTED(eth0)<br><strong>2</strong>. node: as2dept1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;PERMITTED(RESTRICT_HOST_TRAFFIC_IN (INGRESS_FILTER))<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0, Routes: [connected (Network: 2.34.101.0/24, Next Hop: interface GigabitEthernet0/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)<br><strong>3</strong>. node: as2dist1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;ACCEPTED(GigabitEthernet2/0)



Evaluating the first Reverse Trace


```python
result.Reverse_Traces[0][0]
```




<span style="color:#019612; text-weight:bold;">ACCEPTED</span><br><strong>1</strong>. node: host1<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: eth0 with resolved next-hop IP: 2.128.0.1, Routes: [static (Network: 0.0.0.0/0, Next Hop: interface eth0 ip 2.128.0.1)])<br>&nbsp;&nbsp;PERMITTED(filter::OUTPUT (EGRESS_FILTER))<br>&nbsp;&nbsp;TRANSMITTED(eth0)<br><strong>2</strong>. node: as2dept1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;PERMITTED(RESTRICT_HOST_TRAFFIC_IN (INGRESS_FILTER))<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0, Routes: [connected (Network: 2.34.101.0/24, Next Hop: interface GigabitEthernet0/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)<br><strong>3</strong>. node: as2dist1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;ACCEPTED(GigabitEthernet2/0)



Retrieving the disposition of the first Reverse Trace


```python
result.Reverse_Traces[0][0].disposition
```




    'ACCEPTED'



Retrieving the first hop of the first Reverse Trace


```python
result.Reverse_Traces[0][0][0]
```




node: host1<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: eth0 with resolved next-hop IP: 2.128.0.1, Routes: [static (Network: 0.0.0.0/0, Next Hop: interface eth0 ip 2.128.0.1)])<br>&nbsp;&nbsp;PERMITTED(filter::OUTPUT (EGRESS_FILTER))<br>&nbsp;&nbsp;TRANSMITTED(eth0)



Retrieving the last hop of the first Reverse Trace


```python
result.Reverse_Traces[0][0][-1]
```




node: as2dist1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;ACCEPTED(GigabitEthernet2/0)




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Loop detection

Detects forwarding loops.

Searches across all possible flows in the network and returns example flows that will experience forwarding loops.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
maxTraces | Limit the number of traces returned. | int | True | 

###### **Invocation**


```python
result = bf.q.detectLoops().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Flow | The flow | [Flow](../datamodel.rst#pybatfish.datamodel.flow.Flow)
Traces | The traces for this flow | Set of [Trace](../datamodel.rst#pybatfish.datamodel.flow.Trace)
TraceCount | The total number traces for this flow | int

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
      <th>Traces</th>
      <th>TraceCount</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Multipath Consistency for host-subnets

Validates multipath consistency between all pairs of subnets.

Searches across all flows between subnets that are treated differently (i.e., dropped versus forwarded) by different paths in the network and returns example flows.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
maxTraces | Limit the number of traces returned. | int | True | 

###### **Invocation**


```python
result = bf.q.subnetMultipathConsistency().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Flow | The flow | [Flow](../datamodel.rst#pybatfish.datamodel.flow.Flow)
Traces | The traces for this flow | Set of [Trace](../datamodel.rst#pybatfish.datamodel.flow.Trace)
TraceCount | The total number traces for this flow | int

Retrieving the flow definition


```python
result.Flow
```




    0    start=as2dept1 interface=GigabitEthernet0/0 [2.34.101.1:49152->1.0.1.3:23 TCP (SYN)]
    1    start=as2dept1 interface=GigabitEthernet1/0 [2.34.201.1:49152->1.0.1.3:23 TCP (SYN)]
    2     start=as2dept1 interface=GigabitEthernet2/0 [2.128.0.2:49152->1.0.1.3:23 TCP (SYN)]
    3     start=as2dept1 interface=GigabitEthernet3/0 [2.128.1.2:49152->1.0.1.3:23 TCP (SYN)]
    4     start=as2dist1 interface=GigabitEthernet0/0 [2.23.11.1:49152->1.0.1.3:23 TCP (SYN)]
    5     start=as2dist1 interface=GigabitEthernet1/0 [2.23.21.1:49152->1.0.1.3:23 TCP (SYN)]
    6    start=as2dist1 interface=GigabitEthernet2/0 [2.34.101.1:49152->1.0.1.3:23 TCP (SYN)]
    7     start=as2dist2 interface=GigabitEthernet0/0 [2.23.22.1:49152->1.0.1.3:23 TCP (SYN)]
    8     start=as2dist2 interface=GigabitEthernet1/0 [2.23.12.1:49152->1.0.1.3:23 TCP (SYN)]
    9    start=as2dist2 interface=GigabitEthernet2/0 [2.34.201.1:49152->1.0.1.3:23 TCP (SYN)]
    Name: Flow, dtype: object



Retrieving the detailed Trace information


```python
len(result.Traces)
```




    10




```python
result.Traces[0]
```




<span style="color:#7c020e; text-weight:bold;">DENIED_IN</span><br><strong>1</strong>. node: as2dept1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0 with resolved next-hop IP: 2.34.101.3, Routes: [bgp (Network: 1.0.1.0/24, Next Hop: ip 2.34.101.3)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)<br><strong>2</strong>. node: as2dist1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0 with resolved next-hop IP: 2.23.11.2, Routes: [ibgp (Network: 1.0.1.0/24, Next Hop: ip 10.12.11.1)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)<br><strong>3</strong>. node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;DENIED(blocktelnet (INGRESS_FILTER))<br><br><span style="color:#019612; text-weight:bold;">DELIVERED_TO_SUBNET</span><br><strong>1</strong>. node: as2dept1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0 with resolved next-hop IP: 2.34.101.3, Routes: [bgp (Network: 1.0.1.0/24, Next Hop: ip 2.34.101.3)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)<br><strong>2</strong>. node: as2dist1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.23.21.2, Routes: [ibgp (Network: 1.0.1.0/24, Next Hop: ip 10.12.11.1)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>3</strong>. node: as2core2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet3/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.12.1, Routes: [ibgp (Network: 1.0.1.0/24, Next Hop: ip 10.12.11.1)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>4</strong>. node: as2border1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0 with resolved next-hop IP: 10.12.11.1, Routes: [bgp (Network: 1.0.1.0/24, Next Hop: ip 10.12.11.1)])<br>&nbsp;&nbsp;PERMITTED(INSIDE_TO_AS1 (EGRESS_FILTER))<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)<br><strong>5</strong>. node: as1border1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0, Routes: [connected (Network: 1.0.1.0/24, Next Hop: interface GigabitEthernet0/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)<br>&nbsp;&nbsp;DELIVERED_TO_SUBNET(Output Interface: GigabitEthernet0/0, Resolved Next Hop IP: 1.0.1.3)<br><br><span style="color:#019612; text-weight:bold;">DELIVERED_TO_SUBNET</span><br><strong>1</strong>. node: as2dept1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.34.201.3, Routes: [bgp (Network: 1.0.1.0/24, Next Hop: ip 2.34.201.3)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>2</strong>. node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0 with resolved next-hop IP: 2.23.22.2, Routes: [ibgp (Network: 1.0.1.0/24, Next Hop: ip 10.12.11.1)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)<br><strong>3</strong>. node: as2core2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.12.1, Routes: [ibgp (Network: 1.0.1.0/24, Next Hop: ip 10.12.11.1)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>4</strong>. node: as2border1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0 with resolved next-hop IP: 10.12.11.1, Routes: [bgp (Network: 1.0.1.0/24, Next Hop: ip 10.12.11.1)])<br>&nbsp;&nbsp;PERMITTED(INSIDE_TO_AS1 (EGRESS_FILTER))<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)<br><strong>5</strong>. node: as1border1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0, Routes: [connected (Network: 1.0.1.0/24, Next Hop: interface GigabitEthernet0/0)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)<br>&nbsp;&nbsp;DELIVERED_TO_SUBNET(Output Interface: GigabitEthernet0/0, Resolved Next Hop IP: 1.0.1.3)<br><br><span style="color:#7c020e; text-weight:bold;">DENIED_IN</span><br><strong>1</strong>. node: as2dept1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.34.201.3, Routes: [bgp (Network: 1.0.1.0/24, Next Hop: ip 2.34.201.3)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>2</strong>. node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.23.12.2, Routes: [ibgp (Network: 1.0.1.0/24, Next Hop: ip 10.12.11.1)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>3</strong>. node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet3/0)<br>&nbsp;&nbsp;DENIED(blocktelnet (INGRESS_FILTER))



Evaluating the first Trace


```python
result.Traces[0][0]
```




<span style="color:#7c020e; text-weight:bold;">DENIED_IN</span><br><strong>1</strong>. node: as2dept1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0 with resolved next-hop IP: 2.34.101.3, Routes: [bgp (Network: 1.0.1.0/24, Next Hop: ip 2.34.101.3)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)<br><strong>2</strong>. node: as2dist1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0 with resolved next-hop IP: 2.23.11.2, Routes: [ibgp (Network: 1.0.1.0/24, Next Hop: ip 10.12.11.1)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)<br><strong>3</strong>. node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;DENIED(blocktelnet (INGRESS_FILTER))



Retrieving the disposition of the first Trace


```python
result.Traces[0][0].disposition
```




    'DENIED_IN'



Retrieving the first hop of the first Trace


```python
result.Traces[0][0][0]
```




node: as2dept1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0 with resolved next-hop IP: 2.34.101.3, Routes: [bgp (Network: 1.0.1.0/24, Next Hop: ip 2.34.101.3)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)



Retrieving the last hop of the first Trace


```python
result.Traces[0][0][-1]
```




node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;DENIED(blocktelnet (INGRESS_FILTER))




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Multipath Consistency for router loopbacks

Validates multipath consistency between all pairs of loopbacks.

Finds flows between loopbacks that are treated differently (i.e., dropped versus forwarded) by different paths in the presence of multipath routing.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
maxTraces | Limit the number of traces returned. | int | True | 

###### **Invocation**


```python
result = bf.q.loopbackMultipathConsistency().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Flow | The flow | [Flow](../datamodel.rst#pybatfish.datamodel.flow.Flow)
Traces | The traces for this flow | Set of [Trace](../datamodel.rst#pybatfish.datamodel.flow.Trace)
TraceCount | The total number traces for this flow | int

Retrieving the flow definition


```python
result.Flow
```




    0    start=as2core2 [2.1.2.2:49152->2.1.2.1:23 TCP (SYN)]
    1    start=as2dist1 [2.1.3.1:49152->2.1.1.1:23 TCP (SYN)]
    2    start=as2dist2 [2.1.3.2:49152->2.1.1.1:23 TCP (SYN)]
    Name: Flow, dtype: object



Retrieving the detailed Trace information


```python
len(result.Traces)
```




    3




```python
result.Traces[0]
```




<span style="color:#019612; text-weight:bold;">ACCEPTED</span><br><strong>1</strong>. node: as2core2<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0 with resolved next-hop IP: 2.12.22.1, Routes: [ospf (Network: 2.1.2.1/32, Next Hop: interface GigabitEthernet0/0 ip 2.12.22.1)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)<br><strong>2</strong>. node: as2border2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.12.21.2, Routes: [ospf (Network: 2.1.2.1/32, Next Hop: interface GigabitEthernet2/0 ip 2.12.21.2)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>3</strong>. node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;ACCEPTED(Loopback0)<br><br><span style="color:#019612; text-weight:bold;">ACCEPTED</span><br><strong>1</strong>. node: as2core2<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.12.1, Routes: [ospf (Network: 2.1.2.1/32, Next Hop: interface GigabitEthernet1/0 ip 2.12.12.1)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>2</strong>. node: as2border1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.12.11.2, Routes: [ospf (Network: 2.1.2.1/32, Next Hop: interface GigabitEthernet1/0 ip 2.12.11.2)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>3</strong>. node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;ACCEPTED(Loopback0)<br><br><span style="color:#7c020e; text-weight:bold;">DENIED_IN</span><br><strong>1</strong>. node: as2core2<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.23.22.3, Routes: [ospf (Network: 2.1.2.1/32, Next Hop: interface GigabitEthernet2/0 ip 2.23.22.3)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>2</strong>. node: as2dist2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet0/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet1/0 with resolved next-hop IP: 2.23.12.2, Routes: [ospf (Network: 2.1.2.1/32, Next Hop: interface GigabitEthernet1/0 ip 2.23.12.2)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet1/0)<br><strong>3</strong>. node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet3/0)<br>&nbsp;&nbsp;DENIED(blocktelnet (INGRESS_FILTER))<br><br><span style="color:#7c020e; text-weight:bold;">DENIED_IN</span><br><strong>1</strong>. node: as2core2<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet3/0 with resolved next-hop IP: 2.23.21.3, Routes: [ospf (Network: 2.1.2.1/32, Next Hop: interface GigabitEthernet3/0 ip 2.23.21.3)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet3/0)<br><strong>2</strong>. node: as2dist1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0 with resolved next-hop IP: 2.23.11.2, Routes: [ospf (Network: 2.1.2.1/32, Next Hop: interface GigabitEthernet0/0 ip 2.23.11.2)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)<br><strong>3</strong>. node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet2/0)<br>&nbsp;&nbsp;DENIED(blocktelnet (INGRESS_FILTER))



Evaluating the first Trace


```python
result.Traces[0][0]
```




<span style="color:#019612; text-weight:bold;">ACCEPTED</span><br><strong>1</strong>. node: as2core2<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0 with resolved next-hop IP: 2.12.22.1, Routes: [ospf (Network: 2.1.2.1/32, Next Hop: interface GigabitEthernet0/0 ip 2.12.22.1)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)<br><strong>2</strong>. node: as2border2<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet2/0 with resolved next-hop IP: 2.12.21.2, Routes: [ospf (Network: 2.1.2.1/32, Next Hop: interface GigabitEthernet2/0 ip 2.12.21.2)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet2/0)<br><strong>3</strong>. node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;ACCEPTED(Loopback0)



Retrieving the disposition of the first Trace


```python
result.Traces[0][0].disposition
```




    'ACCEPTED'



Retrieving the first hop of the first Trace


```python
result.Traces[0][0][0]
```




node: as2core2<br>&nbsp;&nbsp;ORIGINATED(default)<br>&nbsp;&nbsp;FORWARDED(Forwarded out interface: GigabitEthernet0/0 with resolved next-hop IP: 2.12.22.1, Routes: [ospf (Network: 2.1.2.1/32, Next Hop: interface GigabitEthernet0/0 ip 2.12.22.1)])<br>&nbsp;&nbsp;TRANSMITTED(GigabitEthernet0/0)



Retrieving the last hop of the first Trace


```python
result.Traces[0][0][-1]
```




node: as2core1<br>&nbsp;&nbsp;RECEIVED(GigabitEthernet1/0)<br>&nbsp;&nbsp;ACCEPTED(Loopback0)


