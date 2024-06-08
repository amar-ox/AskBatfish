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

#### Access-lists and firewall rules

This category of questions allows you to analyze the behavior of access
control lists and firewall rules. It also allows you to comprehensively
validate (aka verification) that some traffic is or is not allowed.


* [Filter Line Reachability](#Filter-Line-Reachability)
* [Search Filters](#Search-Filters)
* [Test Filters](#Test-Filters)
* [Find Matching Filter Lines](#Find-Matching-Filter-Lines)
* [Check SNMP Community Clients](#Check-SNMP-Community-Clients)


```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Filter Line Reachability

Returns unreachable lines in filters (ACLs and firewall rules).

Finds all lines in the specified filters that will not match any packet, either because of being shadowed by prior lines or because of its match condition being empty.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Examine filters on nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
filters | Specifier for filters to test. | [FilterSpec](../specifiers.md#filter-specifier) | True | 
ignoreComposites | Whether to ignore filters that are composed of multiple filters defined in the configs. | bool | True | False

###### **Invocation**


```python
result = bf.q.filterLineReachability().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Sources | Filter sources | List of str
Unreachable_Line | Filter line that cannot be matched (i.e., unreachable) | str
Unreachable_Line_Action | Action performed by the unreachable line (e.g., PERMIT or DENY) | str
Blocking_Lines | Lines that, when combined, cover the unreachable line | List of str
Different_Action | Whether unreachable line has an action different from the blocking line(s) | bool
Reason | The reason a line is unreachable | str
Additional_Info | Additional information | str

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
      <th>Sources</th>
      <th>Unreachable_Line</th>
      <th>Unreachable_Line_Action</th>
      <th>Blocking_Lines</th>
      <th>Different_Action</th>
      <th>Reason</th>
      <th>Additional_Info</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>['as2dept1: RESTRICT_HOST_TRAFFIC_OUT']</td>
      <td>deny   ip 1.128.0.0 0.0.255.255 2.128.0.0 0.0.255.255</td>
      <td>DENY</td>
      <td>['permit ip any 2.128.0.0 0.0.255.255']</td>
      <td>True</td>
      <td>BLOCKING_LINES</td>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>['as2dept1: RESTRICT_HOST_TRAFFIC_IN']</td>
      <td>permit icmp any any</td>
      <td>PERMIT</td>
      <td>['deny   ip any any']</td>
      <td>True</td>
      <td>BLOCKING_LINES</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Sources                                  ['as2dept1: RESTRICT_HOST_TRAFFIC_OUT']
    Unreachable_Line           deny   ip 1.128.0.0 0.0.255.255 2.128.0.0 0.0.255.255
    Unreachable_Line_Action                                                     DENY
    Blocking_Lines                           ['permit ip any 2.128.0.0 0.0.255.255']
    Different_Action                                                            True
    Reason                                                            BLOCKING_LINES
    Additional_Info                                                             None
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('filters')
```




    'filters'



##### Search Filters

Finds flows for which a filter takes a particular behavior.

This question searches for flows for which a filter (access control list) has a particular behavior. The behaviors can be: that the filter permits the flow (`permit`), that it denies the flow (`deny`), or that the flow is matched by a particular line (`matchLine <lineNumber>`). Filters are selected using node and filter specifiers, which might match multiple filters. In this case, a (possibly different) flow will be found for each filter.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Only evaluate filters present on nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
filters | Only evaluate filters that match this specifier. | [FilterSpec](../specifiers.md#filter-specifier) | True | 
headers | Packet header constraints on the flows being searched. | [HeaderConstraints](../datamodel.rst#pybatfish.datamodel.flow.HeaderConstraints) | True | 
action | The behavior that you want evaluated. Specify exactly one of `permit`, `deny`, or `matchLine <line number>`. | str | True | 
startLocation | Only consider specified locations as possible sources. | [LocationSpec](../specifiers.md#location-specifier) | True | 
invertSearch | Search for packet headers outside the specified headerspace, rather than inside the space. | bool | True | 

###### **Invocation**


```python
result = bf.q.searchFilters(headers=HeaderConstraints(srcIps='10.10.10.0/24', dstIps='218.8.104.58', applications = ['dns']), action='deny', filters='acl_in').answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
Filter_Name | Filter name | str
Flow | Evaluated flow | [Flow](../datamodel.rst#pybatfish.datamodel.flow.Flow)
Action | Outcome | str
Line_Content | Line content | str
Trace | ACL trace | List of [TraceTree](../datamodel.rst#pybatfish.datamodel.acl.TraceTree)

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
      <th>Flow</th>
      <th>Action</th>
      <th>Line_Content</th>
      <th>Trace</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>rtr-with-acl</td>
      <td>acl_in</td>
      <td>start=rtr-with-acl [10.10.10.42:49152-&gt;218.8.104.58:53 UDP]</td>
      <td>DENY</td>
      <td>460 deny udp 10.10.10.42/32 218.8.104.58/32 eq domain</td>
      <td>- Matched line 460 deny udp 10.10.10.42/32 218.8.104.58/32 eq domain</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                                                    rtr-with-acl
    Filter_Name                                                                   acl_in
    Flow                     start=rtr-with-acl [10.10.10.42:49152->218.8.104.58:53 UDP]
    Action                                                                          DENY
    Line_Content                   460 deny udp 10.10.10.42/32 218.8.104.58/32 eq domain
    Trace           - Matched line 460 deny udp 10.10.10.42/32 218.8.104.58/32 eq domain
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('filters')
```




    'filters'



##### Test Filters

Returns how a flow is processed by a filter (ACLs, firewall rules).

Shows how the specified flow is processed through the specified filters, returning its permit/deny status as well as the line(s) it matched.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Only examine filters on nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
filters | Only consider filters that match this specifier. | [FilterSpec](../specifiers.md#filter-specifier) | True | 
headers | Packet header constraints. | [HeaderConstraints](../datamodel.rst#pybatfish.datamodel.flow.HeaderConstraints) | False | 
startLocation | Location to start tracing from. | [LocationSpec](../specifiers.md#location-specifier) | True | 

###### **Invocation**


```python
result = bf.q.testFilters(headers=HeaderConstraints(srcIps='10.10.10.1', dstIps='218.8.104.58', applications = ['dns']), nodes='rtr-with-acl', filters='acl_in').answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
Filter_Name | Filter name | str
Flow | Evaluated flow | [Flow](../datamodel.rst#pybatfish.datamodel.flow.Flow)
Action | Outcome | str
Line_Content | Line content | str
Trace | ACL trace | List of [TraceTree](../datamodel.rst#pybatfish.datamodel.acl.TraceTree)

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
      <th>Flow</th>
      <th>Action</th>
      <th>Line_Content</th>
      <th>Trace</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>rtr-with-acl</td>
      <td>acl_in</td>
      <td>start=rtr-with-acl [10.10.10.1:49152-&gt;218.8.104.58:53 UDP]</td>
      <td>PERMIT</td>
      <td>660 permit udp 10.10.10.0/24 218.8.104.58/32 eq domain</td>
      <td>- Matched line 660 permit udp 10.10.10.0/24 218.8.104.58/32 eq domain</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                                                     rtr-with-acl
    Filter_Name                                                                    acl_in
    Flow                       start=rtr-with-acl [10.10.10.1:49152->218.8.104.58:53 UDP]
    Action                                                                         PERMIT
    Line_Content                   660 permit udp 10.10.10.0/24 218.8.104.58/32 eq domain
    Trace           - Matched line 660 permit udp 10.10.10.0/24 218.8.104.58/32 eq domain
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Find Matching Filter Lines

Returns lines in filters (ACLs and firewall rules) that match any packet within the specified header constraints.

Finds all lines in the specified filters that match any packet within the specified header constraints.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Examine filters on nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
filters | Specifier for filters to check. | [FilterSpec](../specifiers.md#filter-specifier) | True | 
headers | Packet header constraints for which to find matching filter lines. | [HeaderConstraints](../datamodel.rst#pybatfish.datamodel.flow.HeaderConstraints) | True | 
action | Show filter lines with this action. By default returns lines with either action. | str | True | 
ignoreComposites | Whether to ignore filters that are composed of multiple filters defined in the configs. | bool | True | False

###### **Invocation**


```python
result = bf.q.findMatchingFilterLines(headers=HeaderConstraints(applications='DNS')).answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
Filter | Filter name | str
Line | Line text | str
Line_Index | Index of line | int
Action | Action performed by the line (e.g., PERMIT or DENY) | str

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
      <th>Filter</th>
      <th>Line</th>
      <th>Line_Index</th>
      <th>Action</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as1border1</td>
      <td>101</td>
      <td>permit ip host 1.0.1.0 host 255.255.255.0</td>
      <td>0</td>
      <td>PERMIT</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as1border1</td>
      <td>101</td>
      <td>permit ip host 1.0.2.0 host 255.255.255.0</td>
      <td>1</td>
      <td>PERMIT</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as1border1</td>
      <td>102</td>
      <td>permit ip host 2.0.0.0 host 255.0.0.0</td>
      <td>0</td>
      <td>PERMIT</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as1border1</td>
      <td>102</td>
      <td>permit ip host 2.128.0.0 host 255.255.0.0</td>
      <td>1</td>
      <td>PERMIT</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as1border1</td>
      <td>103</td>
      <td>permit ip host 3.0.1.0 host 255.255.255.0</td>
      <td>0</td>
      <td>PERMIT</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                         as1border1
    Filter                                              101
    Line          permit ip host 1.0.1.0 host 255.255.255.0
    Line_Index                                            0
    Action                                           PERMIT
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('snmp')
```




    'snmp'



##### Check SNMP Community Clients

Checks if an SNMP community permits specified client IPs.

This question checks if the specified SNMP community permits the specified client IPs on specified devices. It reports if any device does not have the community or the set of permitted client IPs by the community does not match those specified in the question. If the community exists and permits exactly the specified client IPs, the device is not included in the output. The question currently only supports Arista, Cisco-NXOS, and Juniper devices. For all others, it will report an UNSUPPORTED_DEVICE status in the output.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
community | The SNMP community to consider. | str | False | 
clients | Client IPs expected to be permitted. | [IpSpec](../specifiers.md#ip-specifier) | True | 
nodes | Only evaluate nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 

###### **Invocation**


```python
result = bf.q.snmpCommunityClients(community='COMM', clients='1.2.3.4/32').answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Hostname. | str
Community | The community name. | str
Reason | Result of the test. | str

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
      <th>Community</th>
      <th>Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>arista</td>
      <td>COMM</td>
      <td>UNEXPECTED_CLIENTS</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ios</td>
      <td>COMM</td>
      <td>UNSUPPORTED_DEVICE</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                     arista
    Community                  COMM
    Reason       UNEXPECTED_CLIENTS
    Name: 0, dtype: object


