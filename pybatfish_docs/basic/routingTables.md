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

#### Routing and Forwarding Tables

This category of questions allows you to query the RIBs and FIBs computed
by Batfish.


* [Routes](#Routes)
* [BGP RIB](#BGP-RIB)
* [EVPN RIB](#EVPN-RIB)
* [Longest Prefix Match](#Longest-Prefix-Match)


```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Routes

Returns routing tables.

Shows routes for specified RIB, VRF, and node(s).

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Return routes on nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
network | Return routes for networks matching this prefix. | str | True | 
prefixMatchType | Use this prefix matching criterion: EXACT, LONGEST_PREFIX_MATCH, LONGER_PREFIXES, SHORTER_PREFIXES. | str | True | EXACT
protocols | Return routes for protocols matching this specifier. | [RoutingProtocolSpec](../specifiers.md#routing-protocol-specifier) | True | 
vrfs | Return routes on VRFs matching this name or regex. | str | True | 
rib | Only return routes from a given protocol RIB. | str | True | 

###### **Invocation**


```python
result = bf.q.routes().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
VRF | VRF name | str
Network | Network for this route | str
Next_Hop | Route's Next Hop | [NextHop](../datamodel.rst#pybatfish.datamodel.route.NextHop)
Next_Hop_IP | Route's Next Hop IP | str
Next_Hop_Interface | Route's Next Hop Interface | str
Protocol | Route's Protocol | str
Metric | Route's Metric | int
Admin_Distance | Route's Admin distance | int
Tag | Tag for this route | int

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
      <th>Network</th>
      <th>Next_Hop</th>
      <th>Next_Hop_IP</th>
      <th>Next_Hop_Interface</th>
      <th>Protocol</th>
      <th>Metric</th>
      <th>Admin_Distance</th>
      <th>Tag</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1.0.1.0/24</td>
      <td>interface GigabitEthernet0/0</td>
      <td>AUTO/NONE(-1l)</td>
      <td>GigabitEthernet0/0</td>
      <td>connected</td>
      <td>0</td>
      <td>0</td>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1.0.1.1/32</td>
      <td>interface GigabitEthernet0/0</td>
      <td>AUTO/NONE(-1l)</td>
      <td>GigabitEthernet0/0</td>
      <td>local</td>
      <td>0</td>
      <td>0</td>
      <td>None</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1.0.2.0/24</td>
      <td>interface GigabitEthernet0/0 ip 1.0.1.2</td>
      <td>1.0.1.2</td>
      <td>GigabitEthernet0/0</td>
      <td>ospf</td>
      <td>2</td>
      <td>110</td>
      <td>None</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1.1.1.1/32</td>
      <td>interface Loopback0</td>
      <td>AUTO/NONE(-1l)</td>
      <td>Loopback0</td>
      <td>connected</td>
      <td>0</td>
      <td>0</td>
      <td>None</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1.2.2.2/32</td>
      <td>interface GigabitEthernet0/0 ip 1.0.1.2</td>
      <td>1.0.1.2</td>
      <td>GigabitEthernet0/0</td>
      <td>ospf</td>
      <td>3</td>
      <td>110</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                    as1border1
    VRF                                        default
    Network                                 1.0.1.0/24
    Next_Hop              interface GigabitEthernet0/0
    Next_Hop_IP                         AUTO/NONE(-1l)
    Next_Hop_Interface              GigabitEthernet0/0
    Protocol                                 connected
    Metric                                           0
    Admin_Distance                                   0
    Tag                                           None
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### BGP RIB

Returns routes in the BGP RIB.

Shows BGP routes for specified VRF and node(s). This question is not available in Batfish containers on dockerhub prior to March 29, 2021.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Examine routes on nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
network | Examine routes for networks matching this prefix. | str | True | 
prefixMatchType | Use this prefix matching criterion: EXACT, LONGEST_PREFIX_MATCH, LONGER_PREFIXES, SHORTER_PREFIXES. | str | True | EXACT
vrfs | Examine routes on VRFs matching this name or regex. | str | True | 
status | Examine routes whose status matches this specifier. | [BgpRouteStatusSpec](../specifiers.md#bgp-route-status-specifier) | True | 

###### **Invocation**


```python
result = bf.q.bgpRib().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
VRF | VRF name | str
Network | Network for this route | str
Status | Route's statuses | List of str
Next_Hop | Route's Next Hop | [NextHop](../datamodel.rst#pybatfish.datamodel.route.NextHop)
Next_Hop_IP | Route's Next Hop IP | str
Next_Hop_Interface | Route's Next Hop Interface | str
Protocol | Route's Protocol | str
AS_Path | Route's AS path | str
Metric | Route's Metric | int
Local_Pref | Route's Local Preference | int
Communities | Route's List of communities | List of str
Origin_Protocol | Route's Origin protocol | str
Origin_Type | Route's Origin type | str
Originator_Id | Route's Originator ID | str
Received_From_IP | IP of the neighbor who sent this route | str
Received_Path_Id | Route's Received Path ID | int
Cluster_List | Route's Cluster List | Set of int
Tunnel_Encapsulation_Attribute | Route's BGP Tunnel Encapsulation Attribute | str
Weight | Route's BGP Weight | int
Tag | Tag for this route | int

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
      <th>Network</th>
      <th>Status</th>
      <th>Next_Hop</th>
      <th>Next_Hop_IP</th>
      <th>Next_Hop_Interface</th>
      <th>Protocol</th>
      <th>AS_Path</th>
      <th>Metric</th>
      <th>Local_Pref</th>
      <th>Communities</th>
      <th>Origin_Protocol</th>
      <th>Origin_Type</th>
      <th>Originator_Id</th>
      <th>Received_From_IP</th>
      <th>Received_Path_Id</th>
      <th>Cluster_List</th>
      <th>Tunnel_Encapsulation_Attribute</th>
      <th>Weight</th>
      <th>Tag</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1.0.1.0/24</td>
      <td>['BEST']</td>
      <td>discard</td>
      <td>AUTO/NONE(-1l)</td>
      <td>null_interface</td>
      <td>bgp</td>
      <td></td>
      <td>0</td>
      <td>100</td>
      <td>[]</td>
      <td>connected</td>
      <td>igp</td>
      <td>1.1.1.1</td>
      <td>0.0.0.0</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>32768</td>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1.0.2.0/24</td>
      <td>['BEST']</td>
      <td>ip 1.0.1.2</td>
      <td>1.0.1.2</td>
      <td>dynamic</td>
      <td>bgp</td>
      <td></td>
      <td>2</td>
      <td>100</td>
      <td>[]</td>
      <td>ospf</td>
      <td>igp</td>
      <td>1.1.1.1</td>
      <td>0.0.0.0</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>32768</td>
      <td>None</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as1border1</td>
      <td>default</td>
      <td>2.128.0.0/16</td>
      <td>['BEST']</td>
      <td>ip 10.12.11.2</td>
      <td>10.12.11.2</td>
      <td>dynamic</td>
      <td>bgp</td>
      <td>2</td>
      <td>50</td>
      <td>350</td>
      <td>['2:1']</td>
      <td>bgp</td>
      <td>igp</td>
      <td>2.1.1.1</td>
      <td>10.12.11.2</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0</td>
      <td>None</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as1border1</td>
      <td>default</td>
      <td>3.0.1.0/24</td>
      <td>['BEST']</td>
      <td>ip 10.13.22.3</td>
      <td>10.13.22.3</td>
      <td>dynamic</td>
      <td>ibgp</td>
      <td>3</td>
      <td>50</td>
      <td>350</td>
      <td>['3:1']</td>
      <td>ibgp</td>
      <td>igp</td>
      <td>1.2.2.2</td>
      <td>1.10.1.1</td>
      <td>1</td>
      <td>[17432833]</td>
      <td>None</td>
      <td>0</td>
      <td>None</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as1border1</td>
      <td>default</td>
      <td>3.0.2.0/24</td>
      <td>['BEST']</td>
      <td>ip 10.13.22.3</td>
      <td>10.13.22.3</td>
      <td>dynamic</td>
      <td>ibgp</td>
      <td>3</td>
      <td>50</td>
      <td>350</td>
      <td>['3:1']</td>
      <td>ibgp</td>
      <td>igp</td>
      <td>1.2.2.2</td>
      <td>1.10.1.1</td>
      <td>1</td>
      <td>[17432833]</td>
      <td>None</td>
      <td>0</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                  as1border1
    VRF                                      default
    Network                               1.0.1.0/24
    Status                                  ['BEST']
    Next_Hop                                 discard
    Next_Hop_IP                       AUTO/NONE(-1l)
    Next_Hop_Interface                null_interface
    Protocol                                     bgp
    AS_Path                                         
    Metric                                         0
    Local_Pref                                   100
    Communities                                   []
    Origin_Protocol                        connected
    Origin_Type                                  igp
    Originator_Id                            1.1.1.1
    Received_From_IP                         0.0.0.0
    Received_Path_Id                            None
    Cluster_List                                None
    Tunnel_Encapsulation_Attribute              None
    Weight                                     32768
    Tag                                         None
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('aristaevpn')
```




    'aristaevpn'



##### EVPN RIB

Returns routes in the EVPN RIB.

Shows EVPN routes for specified VRF and node(s). This question is not available in Batfish containers on dockerhub prior to March 29, 2021.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Examine routes on nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
network | Examine routes for networks matching this prefix. | str | True | 
prefixMatchType | Use this prefix matching criterion: EXACT, LONGEST_PREFIX_MATCH, LONGER_PREFIXES, SHORTER_PREFIXES. | str | True | EXACT
vrfs | Examine routes on VRFs matching this name or regex. | str | True | 

###### **Invocation**


```python
result = bf.q.evpnRib().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
VRF | VRF name | str
Network | Network for this route | str
Status | Route's statuses | List of str
Route_Distinguisher | Route distinguisher | str
Next_Hop | Route's Next Hop | [NextHop](../datamodel.rst#pybatfish.datamodel.route.NextHop)
Next_Hop_IP | Route's Next Hop IP | str
Next_Hop_Interface | Route's Next Hop Interface | str
Protocol | Route's Protocol | str
AS_Path | Route's AS path | str
Metric | Route's Metric | int
Local_Pref | Route's Local Preference | int
Communities | Route's List of communities | List of str
Origin_Protocol | Route's Origin protocol | str
Origin_Type | Route's Origin type | str
Originator_Id | Route's Originator ID | str
Received_Path_Id | Route's Received Path ID | int
Cluster_List | Route's Cluster List | Set of int
Tunnel_Encapsulation_Attribute | Route's BGP Tunnel Encapsulation Attribute | str
Weight | Route's BGP Weight | int
Tag | Tag for this route | int

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
      <th>Network</th>
      <th>Status</th>
      <th>Route_Distinguisher</th>
      <th>Next_Hop</th>
      <th>Next_Hop_IP</th>
      <th>Next_Hop_Interface</th>
      <th>Protocol</th>
      <th>AS_Path</th>
      <th>Metric</th>
      <th>Local_Pref</th>
      <th>Communities</th>
      <th>Origin_Protocol</th>
      <th>Origin_Type</th>
      <th>Originator_Id</th>
      <th>Received_Path_Id</th>
      <th>Cluster_List</th>
      <th>Tunnel_Encapsulation_Attribute</th>
      <th>Weight</th>
      <th>Tag</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>dc1-bl1a</td>
      <td>default</td>
      <td>10.1.10.0/24</td>
      <td>['BEST']</td>
      <td>192.168.255.3:15001</td>
      <td>vni 15001 vtep 192.168.254.3</td>
      <td>AUTO/NONE(-1l)</td>
      <td>dynamic</td>
      <td>bgp</td>
      <td>65001 65101</td>
      <td>0</td>
      <td>100</td>
      <td>['2:15001:15001']</td>
      <td>bgp</td>
      <td>igp</td>
      <td>192.168.255.1</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0</td>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>dc1-bl1a</td>
      <td>default</td>
      <td>10.1.10.0/24</td>
      <td>['BEST']</td>
      <td>192.168.255.5:15001</td>
      <td>vni 15001 vtep 192.168.254.4</td>
      <td>AUTO/NONE(-1l)</td>
      <td>dynamic</td>
      <td>bgp</td>
      <td>65001 65102</td>
      <td>0</td>
      <td>100</td>
      <td>['2:15001:15001']</td>
      <td>bgp</td>
      <td>igp</td>
      <td>192.168.255.1</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0</td>
      <td>None</td>
    </tr>
    <tr>
      <th>2</th>
      <td>dc1-bl1a</td>
      <td>default</td>
      <td>10.1.10.0/24</td>
      <td>['BEST']</td>
      <td>192.168.255.4:15001</td>
      <td>vni 15001 vtep 192.168.254.4</td>
      <td>AUTO/NONE(-1l)</td>
      <td>dynamic</td>
      <td>bgp</td>
      <td>65001 65102</td>
      <td>0</td>
      <td>100</td>
      <td>['2:15001:15001']</td>
      <td>bgp</td>
      <td>igp</td>
      <td>192.168.255.1</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0</td>
      <td>None</td>
    </tr>
    <tr>
      <th>3</th>
      <td>dc1-bl1a</td>
      <td>default</td>
      <td>10.1.11.0/24</td>
      <td>['BEST']</td>
      <td>192.168.255.4:15001</td>
      <td>vni 15001 vtep 192.168.254.4</td>
      <td>AUTO/NONE(-1l)</td>
      <td>dynamic</td>
      <td>bgp</td>
      <td>65001 65102</td>
      <td>0</td>
      <td>100</td>
      <td>['2:15001:15001']</td>
      <td>bgp</td>
      <td>igp</td>
      <td>192.168.255.1</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0</td>
      <td>None</td>
    </tr>
    <tr>
      <th>4</th>
      <td>dc1-bl1a</td>
      <td>default</td>
      <td>10.1.11.0/24</td>
      <td>['BEST']</td>
      <td>192.168.255.5:15001</td>
      <td>vni 15001 vtep 192.168.254.4</td>
      <td>AUTO/NONE(-1l)</td>
      <td>dynamic</td>
      <td>bgp</td>
      <td>65001 65102</td>
      <td>0</td>
      <td>100</td>
      <td>['2:15001:15001']</td>
      <td>bgp</td>
      <td>igp</td>
      <td>192.168.255.1</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                                  dc1-bl1a
    VRF                                                    default
    Network                                           10.1.10.0/24
    Status                                                ['BEST']
    Route_Distinguisher                        192.168.255.3:15001
    Next_Hop                          vni 15001 vtep 192.168.254.3
    Next_Hop_IP                                     AUTO/NONE(-1l)
    Next_Hop_Interface                                     dynamic
    Protocol                                                   bgp
    AS_Path                                            65001 65101
    Metric                                                       0
    Local_Pref                                                 100
    Communities                                  ['2:15001:15001']
    Origin_Protocol                                            bgp
    Origin_Type                                                igp
    Originator_Id                                    192.168.255.1
    Received_Path_Id                                          None
    Cluster_List                                              None
    Tunnel_Encapsulation_Attribute                            None
    Weight                                                       0
    Tag                                                       None
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Longest Prefix Match

Returns routes that are longest prefix match for a given IP address.

Return longest prefix match routes for a given IP in the RIBs of specified nodes and VRFs.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
ip | IP address to run LPM on. | str | False | 
nodes | Examine routes on nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | .*
vrfs | Examine routes on VRFs matching this name or regex. | str | True | .*

###### **Invocation**


```python
result = bf.q.lpmRoutes(ip='2.34.201.10').answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node where the route is present | str
VRF | VRF where the route is present | str
Ip | IP that was being matched on | str
Network | The longest-prefix network that matched | str
Num_Routes | Number of routes that matched (in case of ECMP) | int

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
      <th>Ip</th>
      <th>Network</th>
      <th>Num_Routes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as2border1</td>
      <td>default</td>
      <td>2.34.201.10</td>
      <td>2.34.201.0/24</td>
      <td>2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as2border2</td>
      <td>default</td>
      <td>2.34.201.10</td>
      <td>2.34.201.0/24</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as2core1</td>
      <td>default</td>
      <td>2.34.201.10</td>
      <td>2.34.201.0/24</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as2core2</td>
      <td>default</td>
      <td>2.34.201.10</td>
      <td>2.34.201.0/24</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as2dept1</td>
      <td>default</td>
      <td>2.34.201.10</td>
      <td>2.34.201.0/24</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node             as2border1
    VRF                 default
    Ip              2.34.201.10
    Network       2.34.201.0/24
    Num_Routes                2
    Name: 0, dtype: object


