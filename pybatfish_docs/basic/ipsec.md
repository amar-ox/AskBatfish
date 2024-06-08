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

#### IPSec Tunnels

This category of questions allows you to query IPSec sessions and tunnels.


* [IPSec Session Status](#IPSec-Session-Status)
* [IPSec Edges](#IPSec-Edges)


```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('hybridcloud')
```




    'hybridcloud'



##### IPSec Session Status

Returns the status of configured IPSec sessions.

Shows configuration settings and status for each configured IPSec tunnel in the network. The status is IPSEC_SESSION_ESTABLISHED for tunnels that are expected to be established; it is IKE_PHASE1_FAILED if IKE parameters negotiation failed; it is IKE_PHASE1_KEY_MISMATCH if IKE negotiation was successful but IKE keys do not match; it is IPSEC_PHASE2_FAILED if negotiation of IPsec parameters failed; and it is MISSING_END_POINT if the remote endpoint for a configured IPsec tunnel could not be found in the network.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include sessions whose first node matches this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
remoteNodes | Include sessions whose second node matches this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
status | Only include IPSec sessions for which status matches this specifier. | [IpsecSessionStatusSpec](../specifiers.md#ipsec-session-status-specifier) | True | 

###### **Invocation**


```python
result = bf.q.ipsecSessionStatus().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | IPSec initiator | str
Node_Interface | Initiator Interface | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Node_IP | Initiator IP | str
Remote_Node | IPSec responder | str
Remote_Node_Interface | Responder Interface | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Remote_Node_IP | Responder IP | str
Tunnel_Interfaces | Tunnel interfaces pair used in peering session | str
Status | IPSec session status | str

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
      <th>Node_Interface</th>
      <th>Node_IP</th>
      <th>Remote_Node</th>
      <th>Remote_Node_Interface</th>
      <th>Remote_Node_IP</th>
      <th>Tunnel_Interfaces</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>exitgw</td>
      <td>exitgw[GigabitEthernet3]</td>
      <td>147.75.69.27</td>
      <td>tgw-06b348adabd13452d</td>
      <td>tgw-06b348adabd13452d[external-vpn-01c45673532d3e33e-1]</td>
      <td>3.19.24.131</td>
      <td>Tunnel1 -&gt; vpn-vpn-01c45673532d3e33e-1</td>
      <td>IPSEC_SESSION_ESTABLISHED</td>
    </tr>
    <tr>
      <th>1</th>
      <td>exitgw</td>
      <td>exitgw[GigabitEthernet3]</td>
      <td>147.75.69.27</td>
      <td>tgw-06b348adabd13452d</td>
      <td>tgw-06b348adabd13452d[external-vpn-01c45673532d3e33e-2]</td>
      <td>52.14.53.162</td>
      <td>Tunnel2 -&gt; vpn-vpn-01c45673532d3e33e-2</td>
      <td>IPSEC_SESSION_ESTABLISHED</td>
    </tr>
    <tr>
      <th>2</th>
      <td>exitgw</td>
      <td>exitgw[GigabitEthernet3]</td>
      <td>147.75.69.27</td>
      <td>tgw-0888a76c8a371246d</td>
      <td>tgw-0888a76c8a371246d[external-vpn-0dc7abdb974ff8a69-1]</td>
      <td>34.209.88.227</td>
      <td>Tunnel3 -&gt; vpn-vpn-0dc7abdb974ff8a69-1</td>
      <td>IPSEC_SESSION_ESTABLISHED</td>
    </tr>
    <tr>
      <th>3</th>
      <td>exitgw</td>
      <td>exitgw[GigabitEthernet3]</td>
      <td>147.75.69.27</td>
      <td>tgw-0888a76c8a371246d</td>
      <td>tgw-0888a76c8a371246d[external-vpn-0dc7abdb974ff8a69-2]</td>
      <td>44.227.244.7</td>
      <td>Tunnel4 -&gt; vpn-vpn-0dc7abdb974ff8a69-2</td>
      <td>IPSEC_SESSION_ESTABLISHED</td>
    </tr>
    <tr>
      <th>4</th>
      <td>tgw-06b348adabd13452d</td>
      <td>tgw-06b348adabd13452d[external-vpn-01c45673532d3e33e-1]</td>
      <td>3.19.24.131</td>
      <td>exitgw</td>
      <td>exitgw[GigabitEthernet3]</td>
      <td>147.75.69.27</td>
      <td>vpn-vpn-01c45673532d3e33e-1 -&gt; Tunnel1</td>
      <td>IPSEC_SESSION_ESTABLISHED</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                                                      exitgw
    Node_Interface                                          exitgw[GigabitEthernet3]
    Node_IP                                                             147.75.69.27
    Remote_Node                                                tgw-06b348adabd13452d
    Remote_Node_Interface    tgw-06b348adabd13452d[external-vpn-01c45673532d3e33e-1]
    Remote_Node_IP                                                       3.19.24.131
    Tunnel_Interfaces                         Tunnel1 -> vpn-vpn-01c45673532d3e33e-1
    Status                                                 IPSEC_SESSION_ESTABLISHED
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('hybridcloud')
```




    'hybridcloud'



##### IPSec Edges

Returns IPSec tunnels.

Lists all IPSec tunnels in the network.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include tunnels whose first node matches this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | .*
remoteNodes | Include tunnels whose second node matches this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | .*

###### **Invocation**


```python
result = bf.q.ipsecEdges().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Source_Interface | Source interface used in the IPsec session | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Tunnel_Interface | Tunnel interface (if any) used in the IPsec session | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Remote_Source_Interface | Remote source interface used in the IPsec session | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Remote_Tunnel_Interface | Remote tunnel interface (if any) used in the IPsec session | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)

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
      <th>Source_Interface</th>
      <th>Tunnel_Interface</th>
      <th>Remote_Source_Interface</th>
      <th>Remote_Tunnel_Interface</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>tgw-06b348adabd13452d[external-vpn-01c45673532d3e33e-1]</td>
      <td>tgw-06b348adabd13452d[vpn-vpn-01c45673532d3e33e-1]</td>
      <td>exitgw[GigabitEthernet3]</td>
      <td>exitgw[Tunnel1]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>tgw-0888a76c8a371246d[external-vpn-0dc7abdb974ff8a69-1]</td>
      <td>tgw-0888a76c8a371246d[vpn-vpn-0dc7abdb974ff8a69-1]</td>
      <td>exitgw[GigabitEthernet3]</td>
      <td>exitgw[Tunnel3]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>tgw-06b348adabd13452d[external-vpn-01c45673532d3e33e-2]</td>
      <td>tgw-06b348adabd13452d[vpn-vpn-01c45673532d3e33e-2]</td>
      <td>exitgw[GigabitEthernet3]</td>
      <td>exitgw[Tunnel2]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>exitgw[GigabitEthernet3]</td>
      <td>exitgw[Tunnel4]</td>
      <td>tgw-0888a76c8a371246d[external-vpn-0dc7abdb974ff8a69-2]</td>
      <td>tgw-0888a76c8a371246d[vpn-vpn-0dc7abdb974ff8a69-2]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>tgw-0888a76c8a371246d[external-vpn-0dc7abdb974ff8a69-2]</td>
      <td>tgw-0888a76c8a371246d[vpn-vpn-0dc7abdb974ff8a69-2]</td>
      <td>exitgw[GigabitEthernet3]</td>
      <td>exitgw[Tunnel4]</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Source_Interface           tgw-06b348adabd13452d[external-vpn-01c45673532d3e33e-1]
    Tunnel_Interface                tgw-06b348adabd13452d[vpn-vpn-01c45673532d3e33e-1]
    Remote_Source_Interface                                   exitgw[GigabitEthernet3]
    Remote_Tunnel_Interface                                            exitgw[Tunnel1]
    Name: 0, dtype: object


