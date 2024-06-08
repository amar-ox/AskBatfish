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

#### Topology

This caterogy of questions is intended to retrieve the network topology
used by Batfish. This topology is a combination of information in the
snapshot and inference logic (e.g., which interfaces are layer3 neighbors).
Currently, Layer 3 topology can be retrieved.


* [User Provided Layer 1 Topology](#User-Provided-Layer-1-Topology)
* [Layer 3 Topology](#Layer-3-Topology)


```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('aristaevpn')
```




    'aristaevpn'



##### User Provided Layer 1 Topology

Returns normalized Layer 1 edges that were input to Batfish.

Lists Layer 1 edges after potentially normalizing node and interface names. All node names are lower-cased, and for nodes that appear in the snapshot, interface names are canonicalized based on the vendor. All input edges are in the output, including nodes and interfaces that do not appear in the snapshot.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include edges whose first node matches this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | .*
remoteNodes | Include edges whose second node matches this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | .*

###### **Invocation**


```python
result = bf.q.userProvidedLayer1Edges().answer().frame()
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
      <td>dc1-leaf2a[Ethernet1]</td>
      <td>dc1-spine1[Ethernet2]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>dc1-leaf2b[Ethernet1]</td>
      <td>dc1-spine1[Ethernet3]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>dc1-leaf2b[Ethernet2]</td>
      <td>dc1-spine2[Ethernet3]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>dc1-svc3b[Ethernet6]</td>
      <td>dc1-l2leaf5b[Ethernet2]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>dc1-leaf2a[Ethernet4]</td>
      <td>dc1-leaf2b[Ethernet4]</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Interface           dc1-leaf2a[Ethernet1]
    Remote_Interface    dc1-spine1[Ethernet2]
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Layer 3 Topology

Returns Layer 3 links.

Lists all Layer 3 edges in the network.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include edges whose first node matches this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | .*
remoteNodes | Include edges whose second node matches this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | .*

###### **Invocation**


```python
result = bf.q.layer3Edges().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Interface | Interface from which the edge originates | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
IPs | IPs | Set of str
Remote_Interface | Interface at which the edge terminates | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Remote_IPs | Remote IPs | Set of str

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
      <th>IPs</th>
      <th>Remote_Interface</th>
      <th>Remote_IPs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as1border1[GigabitEthernet0/0]</td>
      <td>['1.0.1.1']</td>
      <td>as1core1[GigabitEthernet1/0]</td>
      <td>['1.0.1.2']</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as1border1[GigabitEthernet1/0]</td>
      <td>['10.12.11.1']</td>
      <td>as2border1[GigabitEthernet0/0]</td>
      <td>['10.12.11.2']</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as1border2[GigabitEthernet0/0]</td>
      <td>['10.13.22.1']</td>
      <td>as3border2[GigabitEthernet0/0]</td>
      <td>['10.13.22.3']</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as1border2[GigabitEthernet1/0]</td>
      <td>['1.0.2.1']</td>
      <td>as1core1[GigabitEthernet0/0]</td>
      <td>['1.0.2.2']</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as1core1[GigabitEthernet0/0]</td>
      <td>['1.0.2.2']</td>
      <td>as1border2[GigabitEthernet1/0]</td>
      <td>['1.0.2.1']</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Interface           as1border1[GigabitEthernet0/0]
    IPs                                    ['1.0.1.1']
    Remote_Interface      as1core1[GigabitEthernet1/0]
    Remote_IPs                             ['1.0.1.2']
    Name: 0, dtype: object


