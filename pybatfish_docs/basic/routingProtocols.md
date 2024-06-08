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

#### Routing Protocol Sessions and Policies

This category of questions reveals information regarding which routing
protocol sessions  are compatibly configured and which ones are
established. It also allows to you analyze BGP routing policies.


* [BGP Session Compatibility](#BGP-Session-Compatibility)
* [BGP Session Status](#BGP-Session-Status)
* [BGP Edges](#BGP-Edges)
* [OSPF Session Compatibility](#OSPF-Session-Compatibility)
* [OSPF Edges](#OSPF-Edges)
* [Test Route Policies](#Test-Route-Policies)
* [Search Route Policies](#Search-Route-Policies)


```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### BGP Session Compatibility

Returns the compatibility of configured BGP sessions.

Checks the settings of each configured BGP peering and reports any issue with those settings locally or incompatiblity with its remote counterparts. Each row represents one configured BGP peering on a node and contains information about the session it is meant to establish. For dynamic peers, there is one row per compatible remote peer. Statuses that indicate an independently misconfigured peerings include NO_LOCAL_AS, NO_REMOTE_AS, NO_LOCAL_IP (for eBGP single-hop peerings), LOCAL_IP_UNKNOWN_STATICALLY (for iBGP or eBGP multi-hop peerings), NO_REMOTE_IP (for point-to-point peerings), and NO_REMOTE_PREFIX (for dynamic peerings). INVALID_LOCAL_IP indicates that the peering's configured local IP does not belong to any active interface on the node; UNKNOWN_REMOTE indicates that the configured remote IP is not present in the network. A locally valid point-to-point peering is deemed HALF_OPEN if it has no compatible remote peers, UNIQUE_MATCH if it has exactly one compatible remote peer, or MULTIPLE_REMOTES if it has multiple compatible remote peers. A locally valid dynamic peering is deemed NO_MATCH_FOUND if it has no compatible remote peers, or DYNAMIC_MATCH if it has at least one compatible remote peer.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include sessions whose first node matches this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
remoteNodes | Include sessions whose second node matches this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
status | Only include sessions for which compatibility status matches this specifier. | [BgpSessionCompatStatusSpec](../specifiers.md#bgp-session-compat-status-specifier) | True | 
type | Only include sessions that match this specifier. | [BgpSessionTypeSpec](../specifiers.md#bgp-session-type-specifier) | True | 

###### **Invocation**


```python
result = bf.q.bgpSessionCompatibility().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | The node where this session is configured | str
VRF | The VRF in which this session is configured | str
Local_AS | The local AS of the session | int
Local_Interface | Local interface of the session | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Local_IP | The local IP of the session | str
Remote_AS | The remote AS or list of ASes of the session | str
Remote_Node | Remote node for this session | str
Remote_Interface | Remote interface for this session | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Remote_IP | Remote IP or prefix for this session | str
Address_Families | Address Families participating in this session | Set of str
Session_Type | The type of this session | str
Configured_Status | Configured status | str

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
      <th>VRF</th>
      <th>Local_AS</th>
      <th>Local_Interface</th>
      <th>Local_IP</th>
      <th>Remote_AS</th>
      <th>Remote_Node</th>
      <th>Remote_Interface</th>
      <th>Remote_IP</th>
      <th>Address_Families</th>
      <th>Session_Type</th>
      <th>Configured_Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1</td>
      <td>None</td>
      <td>None</td>
      <td>666</td>
      <td>None</td>
      <td>None</td>
      <td>3.2.2.2</td>
      <td>[]</td>
      <td>EBGP_SINGLEHOP</td>
      <td>NO_LOCAL_IP</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1</td>
      <td>None</td>
      <td>1.1.1.1</td>
      <td>1</td>
      <td>as1core1</td>
      <td>None</td>
      <td>1.10.1.1</td>
      <td>['IPV4_UNICAST']</td>
      <td>IBGP</td>
      <td>UNIQUE_MATCH</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1</td>
      <td>None</td>
      <td>None</td>
      <td>555</td>
      <td>None</td>
      <td>None</td>
      <td>5.6.7.8</td>
      <td>[]</td>
      <td>EBGP_SINGLEHOP</td>
      <td>NO_LOCAL_IP</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1</td>
      <td>None</td>
      <td>10.12.11.1</td>
      <td>2</td>
      <td>as2border1</td>
      <td>None</td>
      <td>10.12.11.2</td>
      <td>['IPV4_UNICAST']</td>
      <td>EBGP_SINGLEHOP</td>
      <td>UNIQUE_MATCH</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as1border2</td>
      <td>default</td>
      <td>1</td>
      <td>None</td>
      <td>10.14.22.1</td>
      <td>4</td>
      <td>None</td>
      <td>None</td>
      <td>10.14.22.4</td>
      <td>[]</td>
      <td>EBGP_SINGLEHOP</td>
      <td>UNKNOWN_REMOTE</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                     as1border1
    VRF                         default
    Local_AS                          1
    Local_Interface                None
    Local_IP                       None
    Remote_AS                       666
    Remote_Node                    None
    Remote_Interface               None
    Remote_IP                   3.2.2.2
    Address_Families                 []
    Session_Type         EBGP_SINGLEHOP
    Configured_Status       NO_LOCAL_IP
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### BGP Session Status

Returns the dynamic status of configured BGP sessions.

Checks whether configured BGP peerings can be established. Each row represents one configured BGP peering and contains information about the session it is configured to establish. For dynamic peerings, one row is shown per compatible remote peer. Possible statuses for each session are NOT_COMPATIBLE, ESTABLISHED, and NOT_ESTABLISHED. NOT_COMPATIBLE sessions are those where one or both peers are misconfigured; the BgpSessionCompatibility question provides further insight into the nature of the configuration error. NOT_ESTABLISHED sessions are those that are configured compatibly but will not come up because peers cannot reach each other (e.g., due to being blocked by an ACL). ESTABLISHED sessions are those that are compatible and are expected to come up.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include sessions whose first node matches this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
remoteNodes | Include sessions whose second node matches this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
status | Only include sessions for which status matches this specifier. | [BgpSessionStatusSpec](../specifiers.md#bgp-session-status-specifier) | True | 
type | Only include sessions that match this specifier. | [BgpSessionTypeSpec](../specifiers.md#bgp-session-type-specifier) | True | 

###### **Invocation**


```python
result = bf.q.bgpSessionStatus().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | The node where this session is configured | str
VRF | The VRF in which this session is configured | str
Local_AS | The local AS of the session | int
Local_Interface | Local interface of the session | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Local_IP | The local IP of the session | str
Remote_AS | The remote AS or list of ASes of the session | str
Remote_Node | Remote node for this session | str
Remote_Interface | Remote interface for this session | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Remote_IP | Remote IP or prefix for this session | str
Address_Families | Address Families participating in this session | Set of str
Session_Type | The type of this session | str
Established_Status | Established status | str

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
      <th>VRF</th>
      <th>Local_AS</th>
      <th>Local_Interface</th>
      <th>Local_IP</th>
      <th>Remote_AS</th>
      <th>Remote_Node</th>
      <th>Remote_Interface</th>
      <th>Remote_IP</th>
      <th>Address_Families</th>
      <th>Session_Type</th>
      <th>Established_Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1</td>
      <td>None</td>
      <td>None</td>
      <td>666</td>
      <td>None</td>
      <td>None</td>
      <td>3.2.2.2</td>
      <td>[]</td>
      <td>EBGP_SINGLEHOP</td>
      <td>NOT_COMPATIBLE</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1</td>
      <td>None</td>
      <td>1.1.1.1</td>
      <td>1</td>
      <td>as1core1</td>
      <td>None</td>
      <td>1.10.1.1</td>
      <td>['IPV4_UNICAST']</td>
      <td>IBGP</td>
      <td>ESTABLISHED</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1</td>
      <td>None</td>
      <td>None</td>
      <td>555</td>
      <td>None</td>
      <td>None</td>
      <td>5.6.7.8</td>
      <td>[]</td>
      <td>EBGP_SINGLEHOP</td>
      <td>NOT_COMPATIBLE</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1</td>
      <td>None</td>
      <td>10.12.11.1</td>
      <td>2</td>
      <td>as2border1</td>
      <td>None</td>
      <td>10.12.11.2</td>
      <td>['IPV4_UNICAST']</td>
      <td>EBGP_SINGLEHOP</td>
      <td>ESTABLISHED</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as1border2</td>
      <td>default</td>
      <td>1</td>
      <td>None</td>
      <td>10.14.22.1</td>
      <td>4</td>
      <td>None</td>
      <td>None</td>
      <td>10.14.22.4</td>
      <td>[]</td>
      <td>EBGP_SINGLEHOP</td>
      <td>NOT_COMPATIBLE</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                      as1border1
    VRF                          default
    Local_AS                           1
    Local_Interface                 None
    Local_IP                        None
    Remote_AS                        666
    Remote_Node                     None
    Remote_Interface                None
    Remote_IP                    3.2.2.2
    Address_Families                  []
    Session_Type          EBGP_SINGLEHOP
    Established_Status    NOT_COMPATIBLE
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### BGP Edges

Returns BGP adjacencies.

Lists all BGP adjacencies in the network.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include adjacencies whose first node matches this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | .*
remoteNodes | Include adjacencies whose second node matches this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | .*

###### **Invocation**


```python
result = bf.q.bgpEdges().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node from which the edge originates | str
IP | IP at the side of originator | str
Interface | Interface at which the edge originates | str
AS_Number | AS Number at the side of originator | str
Remote_Node | Node at which the edge terminates | str
Remote_IP | IP at the side of the responder | str
Remote_Interface | Interface at which the edge terminates | str
Remote_AS_Number | AS Number at the side of responder | str

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
      <th>IP</th>
      <th>Interface</th>
      <th>AS_Number</th>
      <th>Remote_Node</th>
      <th>Remote_IP</th>
      <th>Remote_Interface</th>
      <th>Remote_AS_Number</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as1border2</td>
      <td>1.2.2.2</td>
      <td>None</td>
      <td>1</td>
      <td>as1core1</td>
      <td>1.10.1.1</td>
      <td>None</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as1core1</td>
      <td>1.10.1.1</td>
      <td>None</td>
      <td>1</td>
      <td>as1border1</td>
      <td>1.1.1.1</td>
      <td>None</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as2dist2</td>
      <td>2.1.3.2</td>
      <td>None</td>
      <td>2</td>
      <td>as2core2</td>
      <td>2.1.2.2</td>
      <td>None</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as3border2</td>
      <td>3.2.2.2</td>
      <td>None</td>
      <td>3</td>
      <td>as3core1</td>
      <td>3.10.1.1</td>
      <td>None</td>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as3border1</td>
      <td>10.23.21.3</td>
      <td>None</td>
      <td>3</td>
      <td>as2border2</td>
      <td>10.23.21.2</td>
      <td>None</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                as1border2
    IP                     1.2.2.2
    Interface                 None
    AS_Number                    1
    Remote_Node           as1core1
    Remote_IP             1.10.1.1
    Remote_Interface          None
    Remote_AS_Number             1
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### OSPF Session Compatibility

Returns compatible OSPF sessions.

Returns compatible OSPF sessions in the network. A session is compatible if the interfaces involved are not shutdown and do run OSPF, are not OSPF passive and are associated with the same OSPF area.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | 
remoteNodes | Include remote nodes matching this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | 
statuses | Only include sessions matching this status specifier. | [OspfSessionStatusSpec](../specifiers.md#ospf-session-status-specifier) | True | 

###### **Invocation**


```python
result = bf.q.ospfSessionCompatibility().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Interface | Interface | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
VRF | VRF | str
IP | Ip | str
Area | Area | int
Remote_Interface | Remote Interface | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Remote_VRF | Remote VRF | str
Remote_IP | Remote IP | str
Remote_Area | Remote Area | int
Session_Status | Status of the OSPF session | str

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
      <th>Interface</th>
      <th>VRF</th>
      <th>IP</th>
      <th>Area</th>
      <th>Remote_Interface</th>
      <th>Remote_VRF</th>
      <th>Remote_IP</th>
      <th>Remote_Area</th>
      <th>Session_Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as2core2[GigabitEthernet0/0]</td>
      <td>default</td>
      <td>2.12.22.2</td>
      <td>1</td>
      <td>as2border2[GigabitEthernet1/0]</td>
      <td>default</td>
      <td>2.12.22.1</td>
      <td>1</td>
      <td>ESTABLISHED</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as2core2[GigabitEthernet1/0]</td>
      <td>default</td>
      <td>2.12.12.2</td>
      <td>1</td>
      <td>as2border1[GigabitEthernet2/0]</td>
      <td>default</td>
      <td>2.12.12.1</td>
      <td>1</td>
      <td>ESTABLISHED</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as2border1[GigabitEthernet1/0]</td>
      <td>default</td>
      <td>2.12.11.1</td>
      <td>1</td>
      <td>as2core1[GigabitEthernet0/0]</td>
      <td>default</td>
      <td>2.12.11.2</td>
      <td>1</td>
      <td>ESTABLISHED</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as2border1[GigabitEthernet2/0]</td>
      <td>default</td>
      <td>2.12.12.1</td>
      <td>1</td>
      <td>as2core2[GigabitEthernet1/0]</td>
      <td>default</td>
      <td>2.12.12.2</td>
      <td>1</td>
      <td>ESTABLISHED</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as2core2[GigabitEthernet3/0]</td>
      <td>default</td>
      <td>2.23.21.2</td>
      <td>1</td>
      <td>as2dist1[GigabitEthernet1/0]</td>
      <td>default</td>
      <td>2.23.21.3</td>
      <td>1</td>
      <td>ESTABLISHED</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Interface             as2core2[GigabitEthernet0/0]
    VRF                                        default
    IP                                       2.12.22.2
    Area                                             1
    Remote_Interface    as2border2[GigabitEthernet1/0]
    Remote_VRF                                 default
    Remote_IP                                2.12.22.1
    Remote_Area                                      1
    Session_Status                         ESTABLISHED
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### OSPF Edges

Returns OSPF adjacencies.

Lists all OSPF adjacencies in the network.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include adjacencies whose first node matches this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | .*
remoteNodes | Include edges whose second node matches this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | .*

###### **Invocation**


```python
result = bf.q.ospfEdges().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Interface | Interface from which the edge originates | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Remote_Interface | Interface at which the edge terminates | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)

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
      <th>Interface</th>
      <th>Remote_Interface</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as1border1[GigabitEthernet0/0]</td>
      <td>as1core1[GigabitEthernet1/0]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as1core1[GigabitEthernet1/0]</td>
      <td>as1border1[GigabitEthernet0/0]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as1border2[GigabitEthernet1/0]</td>
      <td>as1core1[GigabitEthernet0/0]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as1core1[GigabitEthernet0/0]</td>
      <td>as1border2[GigabitEthernet1/0]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as2border1[GigabitEthernet1/0]</td>
      <td>as2core1[GigabitEthernet0/0]</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Interface           as1border1[GigabitEthernet0/0]
    Remote_Interface      as1core1[GigabitEthernet1/0]
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Test Route Policies

Evaluates the processing of a route by a given policy.

Find how the specified route is processed through the specified routing policies.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Only examine filters on nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
policies | Only consider policies that match this specifier. | [RoutingPolicySpec](../specifiers.md#routing-policy-specifier) | True | 
inputRoutes | The BGP route announcements to test the policy on. | List of [BgpRoute](../datamodel.rst#pybatfish.datamodel.route.BgpRoute) | False | 
direction | The direction of the route, with respect to the device (IN/OUT). | str | False | 
bgpSessionProperties | The BGP session properties to use when testing routes. | [BgpSessionProperties](../datamodel.rst#pybatfish.datamodel.route.BgpSessionProperties) | True | 

###### **Invocation**


```python
result = bf.q.testRoutePolicies(policies='/as1_to_/', direction='in', inputRoutes=list([BgpRoute(network='10.0.0.0/24', originatorIp='4.4.4.4', originType='egp', protocol='bgp', asPath=[[64512, 64513], [64514]], communities=['64512:42', '64513:21'])])).answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | The node that has the policy | str
Policy_Name | The name of this policy | str
Input_Route | The input route | [BgpRoute](../datamodel.rst#pybatfish.datamodel.route.BgpRoute)
Action | The action of the policy on the input route | str
Output_Route | The output route, if any | [BgpRoute](../datamodel.rst#pybatfish.datamodel.route.BgpRoute)
Difference | The difference between the input and output routes, if any | [BgpRouteDiffs](../datamodel.rst#pybatfish.datamodel.route.BgpRouteDiffs)
Trace | Route policy trace that shows which clauses/terms matched the input route. If the trace is empty, either nothing matched or tracing is not yet been implemented for this policy type. This is an experimental feature whose content and format is subject to change. | List of [TraceTree](../datamodel.rst#pybatfish.datamodel.acl.TraceTree)

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
      <th>Policy_Name</th>
      <th>Input_Route</th>
      <th>Action</th>
      <th>Output_Route</th>
      <th>Difference</th>
      <th>Trace</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as1border1</td>
      <td>as1_to_as2</td>
      <td>BgpRoute(network='10.0.0.0/24', originatorIp='4.4.4.4', originType='egp', protocol='bgp', asPath=[{'asns': [64512, 64513], 'confederation': False}, {'asns': [64514], 'confederation': False}], communities=['64512:42', '64513:21'], localPreference=0, metric=0, nextHopIp=None, sourceProtocol=None, tag=0, weight=0)</td>
      <td>DENY</td>
      <td>None</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>1</th>
      <td>as1border1</td>
      <td>as1_to_as3</td>
      <td>BgpRoute(network='10.0.0.0/24', originatorIp='4.4.4.4', originType='egp', protocol='bgp', asPath=[{'asns': [64512, 64513], 'confederation': False}, {'asns': [64514], 'confederation': False}], communities=['64512:42', '64513:21'], localPreference=0, metric=0, nextHopIp=None, sourceProtocol=None, tag=0, weight=0)</td>
      <td>DENY</td>
      <td>None</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>as1border2</td>
      <td>as1_to_as2</td>
      <td>BgpRoute(network='10.0.0.0/24', originatorIp='4.4.4.4', originType='egp', protocol='bgp', asPath=[{'asns': [64512, 64513], 'confederation': False}, {'asns': [64514], 'confederation': False}], communities=['64512:42', '64513:21'], localPreference=0, metric=0, nextHopIp=None, sourceProtocol=None, tag=0, weight=0)</td>
      <td>DENY</td>
      <td>None</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>as1border2</td>
      <td>as1_to_as3</td>
      <td>BgpRoute(network='10.0.0.0/24', originatorIp='4.4.4.4', originType='egp', protocol='bgp', asPath=[{'asns': [64512, 64513], 'confederation': False}, {'asns': [64514], 'confederation': False}], communities=['64512:42', '64513:21'], localPreference=0, metric=0, nextHopIp=None, sourceProtocol=None, tag=0, weight=0)</td>
      <td>DENY</td>
      <td>None</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>as1border2</td>
      <td>as1_to_as4</td>
      <td>BgpRoute(network='10.0.0.0/24', originatorIp='4.4.4.4', originType='egp', protocol='bgp', asPath=[{'asns': [64512, 64513], 'confederation': False}, {'asns': [64514], 'confederation': False}], communities=['64512:42', '64513:21'], localPreference=0, metric=0, nextHopIp=None, sourceProtocol=None, tag=0, weight=0)</td>
      <td>PERMIT</td>
      <td>BgpRoute(network='10.0.0.0/24', originatorIp='4.4.4.4', originType='egp', protocol='bgp', asPath=[{'asns': [64512, 64513], 'confederation': False}, {'asns': [64514], 'confederation': False}], communities=['1:4', '64512:42', '64513:21'], localPreference=0, metric=50, nextHopIp=None, sourceProtocol=None, tag=0, weight=0)</td>
      <td>BgpRouteDiffs(diffs=[BgpRouteDiff(fieldName='communities', oldValue='[64512:42, 64513:21]', newValue='[1:4, 64512:42, 64513:21]'), BgpRouteDiff(fieldName='metric', oldValue='0', newValue='50')])</td>
      <td>- Matched route-map as1_to_as4 clause 2</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                                                                                                                                                                                                                                                                                                          as1border1
    Policy_Name                                                                                                                                                                                                                                                                                                                   as1_to_as2
    Input_Route     BgpRoute(network='10.0.0.0/24', originatorIp='4.4.4.4', originType='egp', protocol='bgp', asPath=[{'asns': [64512, 64513], 'confederation': False}, {'asns': [64514], 'confederation': False}], communities=['64512:42', '64513:21'], localPreference=0, metric=0, nextHopIp=None, sourceProtocol=None, tag=0, weight=0)
    Action                                                                                                                                                                                                                                                                                                                              DENY
    Output_Route                                                                                                                                                                                                                                                                                                                        None
    Difference                                                                                                                                                                                                                                                                                                                          None
    Trace                                                                                                                                                                                                                                                                                                                                   
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Search Route Policies

Finds route announcements for which a route policy has a particular behavior.

This question finds route announcements for which a route policy has a particular behavior. The behaviors can be: that the policy permits the route (`permit`) or that it denies the route (`deny`). Constraints can be imposed on the input route announcements of interest and, in the case of a `permit` action, also on the output route announcements of interest. Route policies are selected using node and policy specifiers, which might match multiple policies. In this case, a (possibly different) answer will be found for each policy. _Note:_ This question currently does not support all of the route policy features that Batfish supports. The question only supports common forms of matching on prefixes, communities, and AS-paths, as well as common forms of setting communities, the local preference, and the metric. The question logs all unsupported features that it encounters as warnings. Due to unsupported features, it is possible for the question to return no answers even for route policies that can in fact exhibit the specified behavior.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Only examine policies on nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
policies | Only consider policies that match this specifier. | [RoutingPolicySpec](../specifiers.md#routing-policy-specifier) | True | 
inputConstraints | Constraints on the set of input BGP route announcements to consider. | [BgpRouteConstraints](../datamodel.rst#pybatfish.datamodel.route.BgpRouteConstraints) | True | 
action | The behavior to be evaluated. Specify exactly one of `permit` or `deny`. | str | True | 
outputConstraints | Constraints on the set of output BGP route announcements to consider. | [BgpRouteConstraints](../datamodel.rst#pybatfish.datamodel.route.BgpRouteConstraints) | True | 
perPath | (deprecated) Run the analysis separately for each execution path of a route map. This option is deprecated in favor of 'pathOption'. | bool | True | 
pathOption | If set to 'per_path' run the analysis separately for each execution path. If set to `non_overlap` run the analysis separately for each execution path but greedily attempt to produce a different prefix for each advertisement to cover each path. This analysis may not produce results for all paths. If set to `single` (or null) the analysis will produce a single advertisement that meets the input and output constraints along one path through the route map. | str | True | 

###### **Invocation**


```python
result = bf.q.searchRoutePolicies(nodes='/^as1/', policies='/as1_to_/', inputConstraints=BgpRouteConstraints(prefix=["10.0.0.0/8:8-32", "172.16.0.0/28:28-32", "192.168.0.0/16:16-32"]), action='permit').answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | The node that has the policy | str
Policy_Name | The name of this policy | str
Input_Route | The input route | [BgpRoute](../datamodel.rst#pybatfish.datamodel.route.BgpRoute)
Action | The action of the policy on the input route | str
Output_Route | The output route, if any | [BgpRoute](../datamodel.rst#pybatfish.datamodel.route.BgpRoute)
Difference | The difference between the input and output routes, if any | [BgpRouteDiffs](../datamodel.rst#pybatfish.datamodel.route.BgpRouteDiffs)
Trace | Route policy trace that shows which clauses/terms matched the input route. If the trace is empty, either nothing matched or tracing is not yet been implemented for this policy type. This is an experimental feature whose content and format is subject to change. | List of [TraceTree](../datamodel.rst#pybatfish.datamodel.acl.TraceTree)

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
      <th>Policy_Name</th>
      <th>Input_Route</th>
      <th>Action</th>
      <th>Output_Route</th>
      <th>Difference</th>
      <th>Trace</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as1border2</td>
      <td>as1_to_as4</td>
      <td>BgpRoute(network='10.0.0.0/8', originatorIp='0.0.0.0', originType='egp', protocol='bgp', asPath=[], communities=[], localPreference=100, metric=0, nextHopIp='0.0.0.1', sourceProtocol=None, tag=0, weight=0)</td>
      <td>PERMIT</td>
      <td>BgpRoute(network='10.0.0.0/8', originatorIp='0.0.0.0', originType='egp', protocol='bgp', asPath=[], communities=['1:4'], localPreference=100, metric=50, nextHopIp='0.0.0.1', sourceProtocol=None, tag=0, weight=0)</td>
      <td>BgpRouteDiffs(diffs=[BgpRouteDiff(fieldName='communities', oldValue='[]', newValue='[1:4]'), BgpRouteDiff(fieldName='metric', oldValue='0', newValue='50')])</td>
      <td>- Matched route-map as1_to_as4 clause 2</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                                                                                                                                                                                                     as1border2
    Policy_Name                                                                                                                                                                                                              as1_to_as4
    Input_Route           BgpRoute(network='10.0.0.0/8', originatorIp='0.0.0.0', originType='egp', protocol='bgp', asPath=[], communities=[], localPreference=100, metric=0, nextHopIp='0.0.0.1', sourceProtocol=None, tag=0, weight=0)
    Action                                                                                                                                                                                                                       PERMIT
    Output_Route    BgpRoute(network='10.0.0.0/8', originatorIp='0.0.0.0', originType='egp', protocol='bgp', asPath=[], communities=['1:4'], localPreference=100, metric=50, nextHopIp='0.0.0.1', sourceProtocol=None, tag=0, weight=0)
    Difference                                                             BgpRouteDiffs(diffs=[BgpRouteDiff(fieldName='communities', oldValue='[]', newValue='[1:4]'), BgpRouteDiff(fieldName='metric', oldValue='0', newValue='50')])
    Trace                                                                                                                                                                                       - Matched route-map as1_to_as4 clause 2
    Name: 0, dtype: object


