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

#### VXLAN and EVPN

This category of questions allows you to query aspects of VXLAN and EVPN
configuration and behavior.


* [VXLAN VNI Properties](#VXLAN-VNI-Properties)
* [VXLAN Edges](#VXLAN-Edges)
* [L3 EVPN VNIs](#L3-EVPN-VNIs)


```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('aristaevpn')
```




    'aristaevpn'



##### VXLAN VNI Properties

Returns configuration settings of VXLANs.

Lists VNI-level network segment settings configured for VXLANs.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
properties | Include properties matching this specifier. | [VxlanVniPropertySpec](../specifiers.md#vxlan-vni-property-specifier) | True | 

###### **Invocation**


```python
result = bf.q.vxlanVniProperties().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
VRF | VRF | str
VNI | VXLAN Segment ID | int
Local_VTEP_IP | IPv4 address of the local VTEP | str
Multicast_Group | IPv4 address of the multicast group | str
VLAN | VLAN number for the VNI | int
VTEP_Flood_List | All IPv4 addresses in the VTEP flood list | List of str
VXLAN_Port | Destination port number for the VXLAN tunnel | int

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
      <th>VNI</th>
      <th>Local_VTEP_IP</th>
      <th>Multicast_Group</th>
      <th>VLAN</th>
      <th>VTEP_Flood_List</th>
      <th>VXLAN_Port</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>dc1-svc3a</td>
      <td>default</td>
      <td>10140</td>
      <td>192.168.254.6</td>
      <td>None</td>
      <td>140</td>
      <td>['192.168.254.3', '192.168.254.4', '192.168.254.8']</td>
      <td>4789</td>
    </tr>
    <tr>
      <th>1</th>
      <td>dc1-svc3b</td>
      <td>default</td>
      <td>10140</td>
      <td>192.168.254.6</td>
      <td>None</td>
      <td>140</td>
      <td>['192.168.254.3', '192.168.254.4', '192.168.254.8']</td>
      <td>4789</td>
    </tr>
    <tr>
      <th>2</th>
      <td>dc1-leaf2a</td>
      <td>default</td>
      <td>10130</td>
      <td>192.168.254.4</td>
      <td>None</td>
      <td>130</td>
      <td>['192.168.254.3', '192.168.254.6', '192.168.254.8']</td>
      <td>4789</td>
    </tr>
    <tr>
      <th>3</th>
      <td>dc1-leaf2a</td>
      <td>default</td>
      <td>10160</td>
      <td>192.168.254.4</td>
      <td>None</td>
      <td>160</td>
      <td>['192.168.254.3', '192.168.254.6', '192.168.254.8']</td>
      <td>4789</td>
    </tr>
    <tr>
      <th>4</th>
      <td>dc1-leaf2b</td>
      <td>default</td>
      <td>10130</td>
      <td>192.168.254.4</td>
      <td>None</td>
      <td>130</td>
      <td>['192.168.254.3', '192.168.254.6', '192.168.254.8']</td>
      <td>4789</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                                         dc1-svc3a
    VRF                                                            default
    VNI                                                              10140
    Local_VTEP_IP                                            192.168.254.6
    Multicast_Group                                                   None
    VLAN                                                               140
    VTEP_Flood_List    ['192.168.254.3', '192.168.254.4', '192.168.254.8']
    VXLAN_Port                                                        4789
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('aristaevpn')
```




    'aristaevpn'



##### VXLAN Edges

Returns VXLAN edges.

Lists all VXLAN edges in the network.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include edges whose first node matches this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | .*
remoteNodes | Include edges whose second node matches this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | .*

###### **Invocation**


```python
result = bf.q.vxlanEdges().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
VNI | VNI of the VXLAN tunnel edge | int
Node | Node from which the edge originates | str
Remote_Node | Node at which the edge terminates | str
VTEP_Address | VTEP IP of node from which the edge originates | str
Remote_VTEP_Address | VTEP IP of node at which the edge terminates | str
VLAN | VLAN associated with VNI on node from which the edge originates | int
Remote_VLAN | VLAN associated with VNI on node at which the edge terminates | int
UDP_Port | UDP port of the VXLAN tunnel transport | int
Multicast_Group | Multicast group of the VXLAN tunnel transport | str

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
      <th>VNI</th>
      <th>Node</th>
      <th>Remote_Node</th>
      <th>VTEP_Address</th>
      <th>Remote_VTEP_Address</th>
      <th>VLAN</th>
      <th>Remote_VLAN</th>
      <th>UDP_Port</th>
      <th>Multicast_Group</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10130</td>
      <td>dc1-leaf2b</td>
      <td>dc1-svc3a</td>
      <td>192.168.254.4</td>
      <td>192.168.254.6</td>
      <td>130</td>
      <td>130</td>
      <td>4789</td>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10140</td>
      <td>dc1-leaf2a</td>
      <td>dc1-svc3a</td>
      <td>192.168.254.4</td>
      <td>192.168.254.6</td>
      <td>140</td>
      <td>140</td>
      <td>4789</td>
      <td>None</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10130</td>
      <td>dc1-svc3a</td>
      <td>dc1-leaf2a</td>
      <td>192.168.254.6</td>
      <td>192.168.254.4</td>
      <td>130</td>
      <td>130</td>
      <td>4789</td>
      <td>None</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10111</td>
      <td>dc1-leaf1a</td>
      <td>dc1-leaf2b</td>
      <td>192.168.254.3</td>
      <td>192.168.254.4</td>
      <td>111</td>
      <td>111</td>
      <td>4789</td>
      <td>None</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10130</td>
      <td>dc1-svc3b</td>
      <td>dc1-leaf2b</td>
      <td>192.168.254.6</td>
      <td>192.168.254.4</td>
      <td>130</td>
      <td>130</td>
      <td>4789</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    VNI                            10130
    Node                      dc1-leaf2b
    Remote_Node                dc1-svc3a
    VTEP_Address           192.168.254.4
    Remote_VTEP_Address    192.168.254.6
    VLAN                             130
    Remote_VLAN                      130
    UDP_Port                        4789
    Multicast_Group                 None
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('aristaevpn')
```




    'aristaevpn'



##### L3 EVPN VNIs

Returns configuration settings of VXLANs.

Lists VNI-level network segment settings configured for VXLANs.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 

###### **Invocation**


```python
result = bf.q.evpnL3VniProperties().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
VRF | VRF | str
VNI | VXLAN Segment ID | int
Route_Distinguisher | Route distinguisher | str
Import_Route_Target | Import route target | str
Export_Route_Target | Export route target | str

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
      <th>VNI</th>
      <th>Route_Distinguisher</th>
      <th>Import_Route_Target</th>
      <th>Export_Route_Target</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>dc1-bl1a</td>
      <td>Tenant_A_WAN_Zone</td>
      <td>15005</td>
      <td>192.168.255.8:15005</td>
      <td>15005:15005</td>
      <td>15005:15005</td>
    </tr>
    <tr>
      <th>1</th>
      <td>dc1-bl1a</td>
      <td>Tenant_B_WAN_Zone</td>
      <td>25021</td>
      <td>192.168.255.8:25021</td>
      <td>25021:25021</td>
      <td>25021:25021</td>
    </tr>
    <tr>
      <th>2</th>
      <td>dc1-bl1a</td>
      <td>Tenant_C_WAN_Zone</td>
      <td>35031</td>
      <td>192.168.255.8:35031</td>
      <td>35031:35031</td>
      <td>35031:35031</td>
    </tr>
    <tr>
      <th>3</th>
      <td>dc1-bl1b</td>
      <td>Tenant_A_WAN_Zone</td>
      <td>15005</td>
      <td>192.168.255.9:15005</td>
      <td>15005:15005</td>
      <td>15005:15005</td>
    </tr>
    <tr>
      <th>4</th>
      <td>dc1-bl1b</td>
      <td>Tenant_B_WAN_Zone</td>
      <td>25021</td>
      <td>192.168.255.9:25021</td>
      <td>25021:25021</td>
      <td>25021:25021</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                              dc1-bl1a
    VRF                      Tenant_A_WAN_Zone
    VNI                                  15005
    Route_Distinguisher    192.168.255.8:15005
    Import_Route_Target            15005:15005
    Export_Route_Target            15005:15005
    Name: 0, dtype: object


