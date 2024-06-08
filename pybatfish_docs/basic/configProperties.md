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

#### Configuration Properties

This category of questions enables you to retrieve and process the
contents of device configurations in a vendor-agnostic manner
(except where the question itself is vendor-specific). Batfish organizes
configuration content into several sub-categories.


* [Node Properties](#Node-Properties)
* [Interface Properties](#Interface-Properties)
* [BGP Process Configuration](#BGP-Process-Configuration)
* [BGP Peer Configuration](#BGP-Peer-Configuration)
* [HSRP Properties](#HSRP-Properties)
* [OSPF Process Configuration](#OSPF-Process-Configuration)
* [OSPF Interface Configuration](#OSPF-Interface-Configuration)
* [OSPF Area Configuration](#OSPF-Area-Configuration)
* [Multi-chassis LAG](#Multi-chassis-LAG)
* [IP Owners](#IP-Owners)
* [Named Structures](#Named-Structures)
* [Defined Structures](#Defined-Structures)
* [Referenced Structures](#Referenced-Structures)
* [Undefined References](#Undefined-References)
* [Unused Structures](#Unused-Structures)
* [VLAN Properties](#VLAN-Properties)
* [VRRP Properties](#VRRP-Properties)
* [A10 Virtual Server Configuration](#A10-Virtual-Server-Configuration)
* [F5 BIG-IP VIP Configuration](#F5-BIG-IP-VIP-Configuration)


```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Node Properties

Returns configuration settings of nodes.

Lists global settings of devices in the network. Settings that are specific to interfaces, routing protocols, etc. are available via other questions.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | 
properties | Include properties matching this regex. | [NodePropertySpec](../specifiers.md#node-property-specifier) | True | 

###### **Invocation**


```python
result = bf.q.nodeProperties().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
AS_Path_Access_Lists | Names of AS path access lists | Set of str
Authentication_Key_Chains | Names of authentication keychains | Set of str
Community_Match_Exprs | Names of expressions for matching a community | Set of str
Community_Set_Exprs | Names of expressions representing a community-set | Set of str
Community_Set_Match_Exprs | Names of expressions for matching a ommunity-set | Set of str
Community_Sets | Names of community-sets | Set of str
Configuration_Format | Configuration format of the node | str
DNS_Servers | Configured DNS servers | Set of str
DNS_Source_Interface | Source interface to use for communicating with DNS servers | str
Default_Cross_Zone_Action | Default action (PERMIT, DENY) for traffic that traverses firewall zones (null for non-firewall nodes) | str
Default_Inbound_Action | Default action (PERMIT, DENY) for traffic destined for this node | str
Domain_Name | Domain name of the node | str
Hostname | Hostname of the node | str
IKE_Phase1_Keys | Names of IKE Phase 1 keys | Set of str
IKE_Phase1_Policies | Names of IKE Phase 1 policies | Set of str
IKE_Phase1_Proposals | Names of IKE Phase 1 proposals | Set of str
IP6_Access_Lists | (Deprecated) Names of IPv6 filters (ACLs, firewall rule sets) | Set of str
IP_Access_Lists | Names of IPv4 filters (ACLs, firewall rule sets) | Set of str
IPsec_Peer_Configs | Names of IPSec peers | Set of str
IPsec_Phase2_Policies | Names of IPSec Phase 2 policies | Set of str
IPsec_Phase2_Proposals | Names of IPSec Phase 2 proposals | Set of str
Interfaces | Names of interfaces | Set of str
Logging_Servers | Configured logging servers | Set of str
Logging_Source_Interface | Source interface for communicating with logging servers | str
NTP_Servers | Configured NTP servers | Set of str
NTP_Source_Interface | Source interface for communicating with NTP servers | str
PBR_Policies | Names of policy-based routing (PBR) policies | Set of str
Route6_Filter_Lists | (Deprecated) Names of structures that filter IPv6 routes (e.g., prefix lists) | Set of str
Route_Filter_Lists | Names of structures that filter IPv4 routes (e.g., prefix lists) | Set of str
Routing_Policies | Names of policies that manipulate routes (e.g., route maps) | Set of str
SNMP_Source_Interface | Source interface to use for communicating with SNMP servers | str
SNMP_Trap_Servers | Configured SNMP trap servers | Set of str
TACACS_Servers | Configured TACACS servers | Set of str
TACACS_Source_Interface | Source interface to use for communicating with TACACS servers | str
VRFs | Names of VRFs present on the node | Set of str
Zones | Names of firewall zones on the node | Set of str

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
      <th>AS_Path_Access_Lists</th>
      <th>Authentication_Key_Chains</th>
      <th>Community_Match_Exprs</th>
      <th>Community_Set_Exprs</th>
      <th>Community_Set_Match_Exprs</th>
      <th>Community_Sets</th>
      <th>Configuration_Format</th>
      <th>DNS_Servers</th>
      <th>DNS_Source_Interface</th>
      <th>Default_Cross_Zone_Action</th>
      <th>Default_Inbound_Action</th>
      <th>Domain_Name</th>
      <th>Hostname</th>
      <th>IKE_Phase1_Keys</th>
      <th>...</th>
      <th>Interfaces</th>
      <th>Logging_Servers</th>
      <th>Logging_Source_Interface</th>
      <th>NTP_Servers</th>
      <th>NTP_Source_Interface</th>
      <th>PBR_Policies</th>
      <th>Route6_Filter_Lists</th>
      <th>Route_Filter_Lists</th>
      <th>Routing_Policies</th>
      <th>SNMP_Source_Interface</th>
      <th>SNMP_Trap_Servers</th>
      <th>TACACS_Servers</th>
      <th>TACACS_Source_Interface</th>
      <th>VRFs</th>
      <th>Zones</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as2border2</td>
      <td>[]</td>
      <td>[]</td>
      <td>['as1_community', 'as2_community', 'as3_community']</td>
      <td>[]</td>
      <td>['as1_community', 'as2_community', 'as3_community']</td>
      <td>[]</td>
      <td>CISCO_IOS</td>
      <td>[]</td>
      <td>None</td>
      <td>PERMIT</td>
      <td>PERMIT</td>
      <td>lab.local</td>
      <td>as2border2</td>
      <td>[]</td>
      <td>...</td>
      <td>['Ethernet0/0', 'GigabitEthernet0/0', 'GigabitEthernet1/0', 'GigabitEthernet2/0', 'Loopback0']</td>
      <td>[]</td>
      <td>None</td>
      <td>['18.18.18.18']</td>
      <td>None</td>
      <td>[]</td>
      <td>[]</td>
      <td>['101', '103', 'inbound_route_filter', 'outbound_routes', '~MATCH_SUPPRESSED_SUMMARY_ONLY:default~']</td>
      <td>['as1_to_as2', 'as2_to_as1', 'as2_to_as3', 'as3_to_as2', '~BGP_COMMON_EXPORT_POLICY:default~', '~BGP_PEER_EXPORT_POLICY:default:10.23.21.3~', '~BGP_PEER_EXPORT_POLICY:default:2.1.2.1~', '~BGP_PEER_EXPORT_POLICY:default:2.1.2.2~', '~BGP_REDISTRIBUTION_POLICY:default~', '~OSPF_EXPORT_POLICY:default:1~', '~RESOLUTION_POLICY~', '~suppress~rp~summary-only~']</td>
      <td>None</td>
      <td>[]</td>
      <td>[]</td>
      <td>None</td>
      <td>['default']</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as1border1</td>
      <td>[]</td>
      <td>[]</td>
      <td>['as1_community', 'as2_community', 'as3_community']</td>
      <td>[]</td>
      <td>['as1_community', 'as2_community', 'as3_community']</td>
      <td>[]</td>
      <td>CISCO_IOS</td>
      <td>[]</td>
      <td>None</td>
      <td>PERMIT</td>
      <td>PERMIT</td>
      <td>lab.local</td>
      <td>as1border1</td>
      <td>[]</td>
      <td>...</td>
      <td>['Ethernet0/0', 'GigabitEthernet0/0', 'GigabitEthernet1/0', 'Loopback0']</td>
      <td>[]</td>
      <td>None</td>
      <td>[]</td>
      <td>None</td>
      <td>[]</td>
      <td>[]</td>
      <td>['101', '102', '103', 'default_list', 'inbound_route_filter']</td>
      <td>['as1_to_as2', 'as1_to_as3', 'as2_to_as1', 'as3_to_as1', '~BGP_COMMON_EXPORT_POLICY:default~', '~BGP_PEER_EXPORT_POLICY:default:1.10.1.1~', '~BGP_PEER_EXPORT_POLICY:default:10.12.11.2~', '~BGP_PEER_EXPORT_POLICY:default:3.2.2.2~', '~BGP_PEER_EXPORT_POLICY:default:5.6.7.8~', '~BGP_REDISTRIBUTION_POLICY:default~', '~OSPF_EXPORT_POLICY:default:1~', '~RESOLUTION_POLICY~']</td>
      <td>None</td>
      <td>[]</td>
      <td>[]</td>
      <td>None</td>
      <td>['default']</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as3border2</td>
      <td>[]</td>
      <td>[]</td>
      <td>['as1_community', 'as2_community', 'as3_community']</td>
      <td>[]</td>
      <td>['as1_community', 'as2_community', 'as3_community']</td>
      <td>[]</td>
      <td>CISCO_IOS</td>
      <td>[]</td>
      <td>None</td>
      <td>PERMIT</td>
      <td>PERMIT</td>
      <td>lab.local</td>
      <td>as3border2</td>
      <td>[]</td>
      <td>...</td>
      <td>['Ethernet0/0', 'GigabitEthernet0/0', 'GigabitEthernet1/0', 'Loopback0']</td>
      <td>[]</td>
      <td>None</td>
      <td>['18.18.18.18', '23.23.23.23']</td>
      <td>None</td>
      <td>[]</td>
      <td>[]</td>
      <td>['101', '102', '103', 'inbound_route_filter']</td>
      <td>['as1_to_as3', 'as2_to_as3', 'as3_to_as1', 'as3_to_as2', '~BGP_COMMON_EXPORT_POLICY:default~', '~BGP_PEER_EXPORT_POLICY:default:10.13.22.1~', '~BGP_PEER_EXPORT_POLICY:default:3.10.1.1~', '~BGP_REDISTRIBUTION_POLICY:default~', '~OSPF_EXPORT_POLICY:default:1~', '~RESOLUTION_POLICY~']</td>
      <td>None</td>
      <td>[]</td>
      <td>[]</td>
      <td>None</td>
      <td>['default']</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as1border2</td>
      <td>[]</td>
      <td>[]</td>
      <td>['as1_community', 'as2_community', 'as3_community', 'as4_community']</td>
      <td>[]</td>
      <td>['as1_community', 'as2_community', 'as3_community', 'as4_community']</td>
      <td>[]</td>
      <td>CISCO_IOS</td>
      <td>[]</td>
      <td>None</td>
      <td>PERMIT</td>
      <td>PERMIT</td>
      <td>lab.local</td>
      <td>as1border2</td>
      <td>[]</td>
      <td>...</td>
      <td>['Ethernet0/0', 'GigabitEthernet0/0', 'GigabitEthernet1/0', 'GigabitEthernet2/0', 'Loopback0']</td>
      <td>[]</td>
      <td>None</td>
      <td>['18.18.18.18', '23.23.23.23']</td>
      <td>None</td>
      <td>[]</td>
      <td>[]</td>
      <td>['101', '102', '103', 'as4-prefixes', 'inbound_route_filter']</td>
      <td>['as1_to_as2', 'as1_to_as3', 'as1_to_as4', 'as2_to_as1', 'as3_to_as1', 'as4_to_as1', '~BGP_COMMON_EXPORT_POLICY:default~', '~BGP_PEER_EXPORT_POLICY:default:1.10.1.1~', '~BGP_PEER_EXPORT_POLICY:default:10.13.22.3~', '~BGP_PEER_EXPORT_POLICY:default:10.14.22.4~', '~BGP_REDISTRIBUTION_POLICY:default~', '~OSPF_EXPORT_POLICY:default:1~', '~RESOLUTION_POLICY~']</td>
      <td>None</td>
      <td>[]</td>
      <td>[]</td>
      <td>None</td>
      <td>['default']</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as2dept1</td>
      <td>[]</td>
      <td>[]</td>
      <td>['as2_community']</td>
      <td>[]</td>
      <td>['as2_community']</td>
      <td>[]</td>
      <td>CISCO_IOS</td>
      <td>[]</td>
      <td>None</td>
      <td>PERMIT</td>
      <td>PERMIT</td>
      <td>lab.local</td>
      <td>as2dept1</td>
      <td>[]</td>
      <td>...</td>
      <td>['Ethernet0/0', 'GigabitEthernet0/0', 'GigabitEthernet1/0', 'GigabitEthernet2/0', 'GigabitEthernet3/0', 'Loopback0']</td>
      <td>[]</td>
      <td>None</td>
      <td>[]</td>
      <td>None</td>
      <td>[]</td>
      <td>[]</td>
      <td>['102']</td>
      <td>['as2_to_dept', 'dept_to_as2', '~BGP_COMMON_EXPORT_POLICY:default~', '~BGP_PEER_EXPORT_POLICY:default:2.34.101.3~', '~BGP_PEER_EXPORT_POLICY:default:2.34.201.3~', '~BGP_REDISTRIBUTION_POLICY:default~', '~RESOLUTION_POLICY~']</td>
      <td>None</td>
      <td>[]</td>
      <td>[]</td>
      <td>None</td>
      <td>['default']</td>
      <td>[]</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 37 columns</p>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                                                                                                                                                                                                                                                                                                                                                                  as2border2
    AS_Path_Access_Lists                                                                                                                                                                                                                                                                                                                                                                          []
    Authentication_Key_Chains                                                                                                                                                                                                                                                                                                                                                                     []
    Community_Match_Exprs                                                                                                                                                                                                                                                                                                                        ['as1_community', 'as2_community', 'as3_community']
    Community_Set_Exprs                                                                                                                                                                                                                                                                                                                                                                           []
    Community_Set_Match_Exprs                                                                                                                                                                                                                                                                                                                    ['as1_community', 'as2_community', 'as3_community']
    Community_Sets                                                                                                                                                                                                                                                                                                                                                                                []
    Configuration_Format                                                                                                                                                                                                                                                                                                                                                                   CISCO_IOS
    DNS_Servers                                                                                                                                                                                                                                                                                                                                                                                   []
    DNS_Source_Interface                                                                                                                                                                                                                                                                                                                                                                        None
    Default_Cross_Zone_Action                                                                                                                                                                                                                                                                                                                                                                 PERMIT
    Default_Inbound_Action                                                                                                                                                                                                                                                                                                                                                                    PERMIT
    Domain_Name                                                                                                                                                                                                                                                                                                                                                                            lab.local
    Hostname                                                                                                                                                                                                                                                                                                                                                                              as2border2
    IKE_Phase1_Keys                                                                                                                                                                                                                                                                                                                                                                               []
    IKE_Phase1_Policies                                                                                                                                                                                                                                                                                                                                                                           []
    IKE_Phase1_Proposals                                                                                                                                                                                                                                                                                                                                                                          []
    IP6_Access_Lists                                                                                                                                                                                                                                                                                                                                                                              []
    IP_Access_Lists                                                                                                                                                                                                                                                                                                                             ['101', '103', 'INSIDE_TO_AS3', 'OUTSIDE_TO_INSIDE']
    IPsec_Peer_Configs                                                                                                                                                                                                                                                                                                                                                                            []
    IPsec_Phase2_Policies                                                                                                                                                                                                                                                                                                                                                                         []
    IPsec_Phase2_Proposals                                                                                                                                                                                                                                                                                                                                                                        []
    Interfaces                                                                                                                                                                                                                                                                                        ['Ethernet0/0', 'GigabitEthernet0/0', 'GigabitEthernet1/0', 'GigabitEthernet2/0', 'Loopback0']
    Logging_Servers                                                                                                                                                                                                                                                                                                                                                                               []
    Logging_Source_Interface                                                                                                                                                                                                                                                                                                                                                                    None
    NTP_Servers                                                                                                                                                                                                                                                                                                                                                                      ['18.18.18.18']
    NTP_Source_Interface                                                                                                                                                                                                                                                                                                                                                                        None
    PBR_Policies                                                                                                                                                                                                                                                                                                                                                                                  []
    Route6_Filter_Lists                                                                                                                                                                                                                                                                                                                                                                           []
    Route_Filter_Lists                                                                                                                                                                                                                                                                          ['101', '103', 'inbound_route_filter', 'outbound_routes', '~MATCH_SUPPRESSED_SUMMARY_ONLY:default~']
    Routing_Policies             ['as1_to_as2', 'as2_to_as1', 'as2_to_as3', 'as3_to_as2', '~BGP_COMMON_EXPORT_POLICY:default~', '~BGP_PEER_EXPORT_POLICY:default:10.23.21.3~', '~BGP_PEER_EXPORT_POLICY:default:2.1.2.1~', '~BGP_PEER_EXPORT_POLICY:default:2.1.2.2~', '~BGP_REDISTRIBUTION_POLICY:default~', '~OSPF_EXPORT_POLICY:default:1~', '~RESOLUTION_POLICY~', '~suppress~rp~summary-only~']
    SNMP_Source_Interface                                                                                                                                                                                                                                                                                                                                                                       None
    SNMP_Trap_Servers                                                                                                                                                                                                                                                                                                                                                                             []
    TACACS_Servers                                                                                                                                                                                                                                                                                                                                                                                []
    TACACS_Source_Interface                                                                                                                                                                                                                                                                                                                                                                     None
    VRFs                                                                                                                                                                                                                                                                                                                                                                                 ['default']
    Zones                                                                                                                                                                                                                                                                                                                                                                                         []
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Interface Properties

Returns configuration settings of interfaces.

Lists interface-level settings of interfaces. Settings for routing protocols, VRFs, and zones etc. that are attached to interfaces are available via other questions.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
interfaces | Include interfaces matching this specifier. | [InterfaceSpec](../specifiers.md#interface-specifier) | True | 
properties | Include properties matching this specifier. | [InterfacePropertySpec](../specifiers.md#interface-property-specifier) | True | 
excludeShutInterfaces | Exclude interfaces that are shutdown. | bool | True | 

###### **Invocation**


```python
result = bf.q.interfaceProperties().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Interface | Interface | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Access_VLAN | VLAN number when the switchport mode is access (null otherwise) | int
Active | Whether the interface is active | bool
Admin_Up | Whether the interface is administratively enabled | bool
All_Prefixes | All IPv4 addresses assigned to the interface | List of str
Allowed_VLANs | Allowed VLAN numbers when the switchport mode is trunk | str
Auto_State_VLAN | For VLAN interfaces, whether the operational status depends on member switchports | bool
Bandwidth | Nominal bandwidth in bits/sec, used for protocol cost calculations | float
Blacklisted | Whether the interface is considered down for maintenance | bool
Channel_Group | Name of the aggregated interface (e.g., a port channel) to which this interface belongs | str
Channel_Group_Members | For aggregated interfaces (e.g., a port channel), names of constituent interfaces | List of str
DHCP_Relay_Addresses | IPv4 addresses to which incoming DHCP requests are relayed | List of str
Declared_Names | Any aliases explicitly defined for this interface | List of str
Description | Configured interface description | str
Encapsulation_VLAN | Number for VLAN encapsulation | int
HSRP_Groups | HSRP group identifiers | Set of str
HSRP_Version | HSRP version that will be used | str
Inactive_Reason | Reason why interface is inactive | str
Incoming_Filter_Name | Name of the input IPv4 filter | str
MLAG_ID | MLAG identifier of the interface | int
MTU | Layer3 MTU of the interface | int
Native_VLAN | Native VLAN when switchport mode is trunk | int
Outgoing_Filter_Name | Name of the output IPv4 filter | str
PBR_Policy_Name | Name of policy-based routing (PBR) policy | str
Primary_Address | Primary IPv4 address along with the prefix length | str
Primary_Network | Primary IPv4 subnet, in canonical form | str
Proxy_ARP | Whether proxy ARP is enabled | bool
Rip_Enabled | Whether RIP is enabled | bool
Rip_Passive | Whether interface is in RIP passive mode | bool
Spanning_Tree_Portfast | Whether spanning-tree portfast feature is enabled | bool
Speed | Link speed in bits/sec | float
Switchport | Whether the interface is configured as switchport | bool
Switchport_Mode | Switchport mode (ACCESS, DOT1Q_TUNNEL, DYNAMIC_AUTO, DYNAMIC_DESIRABLE, FEX_FABRIC, MONITOR, NONE, TAP, TOOL, TRUNK) for switchport interfaces | str
Switchport_Trunk_Encapsulation | Encapsulation type (DOT1Q, ISL, NEGOTIATE) for switchport trunk interfaces | str
VRF | Name of the VRF to which the interface belongs | str
VRRP_Groups | All VRRP groups to which the interface belongs | List of int
Zone_Name | Name of the firewall zone to which the interface belongs | str

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
      <th>Access_VLAN</th>
      <th>Active</th>
      <th>Admin_Up</th>
      <th>All_Prefixes</th>
      <th>Allowed_VLANs</th>
      <th>Auto_State_VLAN</th>
      <th>Bandwidth</th>
      <th>Blacklisted</th>
      <th>Channel_Group</th>
      <th>Channel_Group_Members</th>
      <th>DHCP_Relay_Addresses</th>
      <th>Declared_Names</th>
      <th>Description</th>
      <th>Encapsulation_VLAN</th>
      <th>...</th>
      <th>Outgoing_Filter_Name</th>
      <th>PBR_Policy_Name</th>
      <th>Primary_Address</th>
      <th>Primary_Network</th>
      <th>Proxy_ARP</th>
      <th>Rip_Enabled</th>
      <th>Rip_Passive</th>
      <th>Spanning_Tree_Portfast</th>
      <th>Speed</th>
      <th>Switchport</th>
      <th>Switchport_Mode</th>
      <th>Switchport_Trunk_Encapsulation</th>
      <th>VRF</th>
      <th>VRRP_Groups</th>
      <th>Zone_Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as1border1[Ethernet0/0]</td>
      <td>None</td>
      <td>False</td>
      <td>False</td>
      <td>[]</td>
      <td></td>
      <td>True</td>
      <td>10000000.0</td>
      <td>False</td>
      <td>None</td>
      <td>[]</td>
      <td>[]</td>
      <td>['Ethernet0/0']</td>
      <td>None</td>
      <td>None</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>10000000.0</td>
      <td>False</td>
      <td>NONE</td>
      <td>DOT1Q</td>
      <td>default</td>
      <td>[]</td>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as1border1[GigabitEthernet0/0]</td>
      <td>None</td>
      <td>True</td>
      <td>True</td>
      <td>['1.0.1.1/24']</td>
      <td></td>
      <td>True</td>
      <td>1000000000.0</td>
      <td>False</td>
      <td>None</td>
      <td>[]</td>
      <td>[]</td>
      <td>['GigabitEthernet0/0']</td>
      <td>None</td>
      <td>None</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>1.0.1.1/24</td>
      <td>1.0.1.0/24</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>1000000000.0</td>
      <td>False</td>
      <td>NONE</td>
      <td>DOT1Q</td>
      <td>default</td>
      <td>[123]</td>
      <td>None</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as1border1[GigabitEthernet1/0]</td>
      <td>None</td>
      <td>True</td>
      <td>True</td>
      <td>['10.12.11.1/24']</td>
      <td></td>
      <td>True</td>
      <td>1000000000.0</td>
      <td>False</td>
      <td>None</td>
      <td>[]</td>
      <td>[]</td>
      <td>['GigabitEthernet1/0']</td>
      <td>None</td>
      <td>None</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>10.12.11.1/24</td>
      <td>10.12.11.0/24</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>1000000000.0</td>
      <td>False</td>
      <td>NONE</td>
      <td>DOT1Q</td>
      <td>default</td>
      <td>[]</td>
      <td>None</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as1border1[Loopback0]</td>
      <td>None</td>
      <td>True</td>
      <td>True</td>
      <td>['1.1.1.1/32']</td>
      <td></td>
      <td>True</td>
      <td>8000000000.0</td>
      <td>None</td>
      <td>None</td>
      <td>[]</td>
      <td>[]</td>
      <td>['Loopback0']</td>
      <td>None</td>
      <td>None</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>1.1.1.1/32</td>
      <td>1.1.1.1/32</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>None</td>
      <td>False</td>
      <td>NONE</td>
      <td>DOT1Q</td>
      <td>default</td>
      <td>[]</td>
      <td>None</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as1border2[Ethernet0/0]</td>
      <td>None</td>
      <td>False</td>
      <td>False</td>
      <td>[]</td>
      <td></td>
      <td>True</td>
      <td>10000000.0</td>
      <td>False</td>
      <td>None</td>
      <td>[]</td>
      <td>[]</td>
      <td>['Ethernet0/0']</td>
      <td>None</td>
      <td>None</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>10000000.0</td>
      <td>False</td>
      <td>NONE</td>
      <td>DOT1Q</td>
      <td>default</td>
      <td>[]</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 37 columns</p>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Interface                         as1border1[Ethernet0/0]
    Access_VLAN                                          None
    Active                                              False
    Admin_Up                                            False
    All_Prefixes                                           []
    Allowed_VLANs                                            
    Auto_State_VLAN                                      True
    Bandwidth                                      10000000.0
    Blacklisted                                         False
    Channel_Group                                        None
    Channel_Group_Members                                  []
    DHCP_Relay_Addresses                                   []
    Declared_Names                            ['Ethernet0/0']
    Description                                          None
    Encapsulation_VLAN                                   None
    HSRP_Groups                                            []
    HSRP_Version                                         None
    Inactive_Reason                     Administratively down
    Incoming_Filter_Name                                 None
    MLAG_ID                                              None
    MTU                                                  1500
    Native_VLAN                                          None
    Outgoing_Filter_Name                                 None
    PBR_Policy_Name                                      None
    Primary_Address                                      None
    Primary_Network                                      None
    Proxy_ARP                                            True
    Rip_Enabled                                         False
    Rip_Passive                                         False
    Spanning_Tree_Portfast                              False
    Speed                                          10000000.0
    Switchport                                          False
    Switchport_Mode                                      NONE
    Switchport_Trunk_Encapsulation                      DOT1Q
    VRF                                               default
    VRRP_Groups                                            []
    Zone_Name                                            None
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### BGP Process Configuration

Returns configuration settings of BGP processes.

Reports configuration settings for each BGP process on each node and VRF in the network. This question reports only process-wide settings. Peer-specific settings are reported by the bgpPeerConfiguration question.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | 
properties | Include properties matching this regex. | [BgpProcessPropertySpec](../specifiers.md#bgp-process-property-specifier) | True | 

###### **Invocation**


```python
result = bf.q.bgpProcessConfiguration().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
VRF | VRF | str
Router_ID | Router ID | str
Confederation_ID | Externally visible autonomous system number for the confederation | int
Confederation_Members | Set of autonomous system numbers visible only within this BGP confederation | str
Multipath_EBGP | Whether multipath routing is enabled for EBGP | bool
Multipath_IBGP | Whether multipath routing is enabled for IBGP | bool
Multipath_Match_Mode | Which AS paths are considered equivalent (EXACT_PATH, FIRST_AS, PATH_LENGTH) when multipath BGP is enabled | str
Neighbors | All peers configured on this process, identified by peer address (for active and dynamic peers) or peer interface (for BGP unnumbered peers) | Set of str
Route_Reflector | Whether any BGP peer in this process is configured as a route reflector client, for ipv4 unicast address family | bool
Tie_Breaker | Tie breaking mode (ARRIVAL_ORDER, CLUSTER_LIST_LENGTH, ROUTER_ID) | str

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
      <th>Router_ID</th>
      <th>Confederation_ID</th>
      <th>Confederation_Members</th>
      <th>Multipath_EBGP</th>
      <th>Multipath_IBGP</th>
      <th>Multipath_Match_Mode</th>
      <th>Neighbors</th>
      <th>Route_Reflector</th>
      <th>Tie_Breaker</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1.1.1.1</td>
      <td>None</td>
      <td>None</td>
      <td>True</td>
      <td>True</td>
      <td>EXACT_PATH</td>
      <td>['3.2.2.2', '1.10.1.1', '5.6.7.8', '10.12.11.2']</td>
      <td>False</td>
      <td>ARRIVAL_ORDER</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as1border2</td>
      <td>default</td>
      <td>1.2.2.2</td>
      <td>None</td>
      <td>None</td>
      <td>True</td>
      <td>True</td>
      <td>EXACT_PATH</td>
      <td>['10.14.22.4', '1.10.1.1', '10.13.22.3']</td>
      <td>False</td>
      <td>ARRIVAL_ORDER</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as1core1</td>
      <td>default</td>
      <td>1.10.1.1</td>
      <td>None</td>
      <td>None</td>
      <td>True</td>
      <td>True</td>
      <td>EXACT_PATH</td>
      <td>['1.1.1.1', '1.2.2.2']</td>
      <td>True</td>
      <td>ARRIVAL_ORDER</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as2border1</td>
      <td>default</td>
      <td>2.1.1.1</td>
      <td>None</td>
      <td>None</td>
      <td>True</td>
      <td>True</td>
      <td>EXACT_PATH</td>
      <td>['2.1.2.1', '2.1.2.2', '10.12.11.1']</td>
      <td>False</td>
      <td>ARRIVAL_ORDER</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as2border2</td>
      <td>default</td>
      <td>2.1.1.2</td>
      <td>None</td>
      <td>None</td>
      <td>True</td>
      <td>True</td>
      <td>EXACT_PATH</td>
      <td>['2.1.2.1', '2.1.2.2', '10.23.21.3']</td>
      <td>False</td>
      <td>ARRIVAL_ORDER</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                                           as1border1
    VRF                                                               default
    Router_ID                                                         1.1.1.1
    Confederation_ID                                                     None
    Confederation_Members                                                None
    Multipath_EBGP                                                       True
    Multipath_IBGP                                                       True
    Multipath_Match_Mode                                           EXACT_PATH
    Neighbors                ['3.2.2.2', '1.10.1.1', '5.6.7.8', '10.12.11.2']
    Route_Reflector                                                     False
    Tie_Breaker                                                 ARRIVAL_ORDER
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### BGP Peer Configuration

Returns configuration settings for BGP peerings.

Reports configuration settings for each configured BGP peering on each node in the network. This question reports peer-specific settings. Settings that are process-wide are reported by the bgpProcessConfiguration question.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | 
properties | Include properties matching this regex. | [BgpPeerPropertySpec](../specifiers.md#bgp-peer-property-specifier) | True | 

###### **Invocation**


```python
result = bf.q.bgpPeerConfiguration().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
VRF | VRF | str
Local_AS | Local AS number | int
Local_IP | Local IPv4 address (null for BGP unnumbered peers) | str
Local_Interface | Local Interface | str
Confederation | Confederation AS number | int
Remote_AS | Remote AS numbers with which this peer may establish a session | str
Remote_IP | Remote IP | str
Description | Configured peer description | str
Route_Reflector_Client | Whether this peer is a route reflector client | bool
Cluster_ID | Cluster ID of this peer (null for peers that are not route reflector clients) | str
Peer_Group | Name of the BGP peer group to which this peer belongs | str
Import_Policy | Names of import policies to be applied to routes received by this peer | Set of str
Export_Policy | Names of export policies to be applied to routes exported by this peer | Set of str
Send_Community | Whether this peer propagates communities | bool
Is_Passive | Whether this peer is passive | bool

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
      <th>Local_IP</th>
      <th>Local_Interface</th>
      <th>Confederation</th>
      <th>Remote_AS</th>
      <th>Remote_IP</th>
      <th>Description</th>
      <th>Route_Reflector_Client</th>
      <th>Cluster_ID</th>
      <th>Peer_Group</th>
      <th>Import_Policy</th>
      <th>Export_Policy</th>
      <th>Send_Community</th>
      <th>Is_Passive</th>
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
      <td>None</td>
      <td>666</td>
      <td>3.2.2.2</td>
      <td>None</td>
      <td>False</td>
      <td>None</td>
      <td>bad-ebgp</td>
      <td>[]</td>
      <td>[]</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1</td>
      <td>1.1.1.1</td>
      <td>None</td>
      <td>None</td>
      <td>1</td>
      <td>1.10.1.1</td>
      <td>None</td>
      <td>False</td>
      <td>None</td>
      <td>as1</td>
      <td>[]</td>
      <td>[]</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>555</td>
      <td>5.6.7.8</td>
      <td>None</td>
      <td>False</td>
      <td>None</td>
      <td>xanadu</td>
      <td>[]</td>
      <td>[]</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as1border1</td>
      <td>default</td>
      <td>1</td>
      <td>10.12.11.1</td>
      <td>None</td>
      <td>None</td>
      <td>2</td>
      <td>10.12.11.2</td>
      <td>None</td>
      <td>False</td>
      <td>None</td>
      <td>as2</td>
      <td>['as2_to_as1']</td>
      <td>['as1_to_as2']</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as1border2</td>
      <td>default</td>
      <td>1</td>
      <td>10.14.22.1</td>
      <td>None</td>
      <td>None</td>
      <td>4</td>
      <td>10.14.22.4</td>
      <td>None</td>
      <td>False</td>
      <td>None</td>
      <td>as4</td>
      <td>['as4_to_as1']</td>
      <td>['as1_to_as4']</td>
      <td>False</td>
      <td>False</td>
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
    Local_IP                        None
    Local_Interface                 None
    Confederation                   None
    Remote_AS                        666
    Remote_IP                    3.2.2.2
    Description                     None
    Route_Reflector_Client         False
    Cluster_ID                      None
    Peer_Group                  bad-ebgp
    Import_Policy                     []
    Export_Policy                     []
    Send_Community                 False
    Is_Passive                     False
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('ios_basic_hsrp')
```




    'ios_basic_hsrp'



##### HSRP Properties

Returns configuration settings of HSRP groups.

Lists information about HSRP groups on interfaces.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
interfaces | Include interfaces matching this specifier. | [InterfaceSpec](../specifiers.md#interface-specifier) | True | 
virtualAddresses | Include only groups with at least one virtual address matching this specifier. | [IpSpec](../specifiers.md#ip-specifier) | True | 
excludeShutInterfaces | Exclude interfaces that are shutdown. | bool | True | 

###### **Invocation**


```python
result = bf.q.hsrpProperties().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Interface | Interface | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Group_Id | HSRP Group ID | int
Virtual_Addresses | Virtual Addresses | Set of str
Source_Address | Source Address used for HSRP messages | str
Priority | HSRP router priority | int
Preempt | Whether preemption is allowed | bool
Active | Whether the interface is active | bool

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
      <th>Group_Id</th>
      <th>Virtual_Addresses</th>
      <th>Source_Address</th>
      <th>Priority</th>
      <th>Preempt</th>
      <th>Active</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>br2[GigabitEthernet0/2]</td>
      <td>12</td>
      <td>['192.168.1.254']</td>
      <td>192.168.1.2/24</td>
      <td>100</td>
      <td>False</td>
      <td>True</td>
    </tr>
    <tr>
      <th>1</th>
      <td>br1[GigabitEthernet0/2]</td>
      <td>12</td>
      <td>['192.168.1.254']</td>
      <td>192.168.1.1/24</td>
      <td>110</td>
      <td>False</td>
      <td>True</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Interface            br2[GigabitEthernet0/2]
    Group_Id                                  12
    Virtual_Addresses          ['192.168.1.254']
    Source_Address                192.168.1.2/24
    Priority                                 100
    Preempt                                False
    Active                                  True
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### OSPF Process Configuration

Returns configuration parameters for OSPF routing processes.

Returns the values of important properties for all OSPF processes running across the network.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | 
properties | Include properties matching this specifier. | [OspfProcessPropertySpec](../specifiers.md#ospf-process-property-specifier) | True | 

###### **Invocation**


```python
result = bf.q.ospfProcessConfiguration().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
VRF | VRF name | str
Process_ID | Process ID | str
Areas | All OSPF areas for this process | Set of str
Reference_Bandwidth | Reference bandwidth in bits/sec used to calculate interface OSPF cost | float
Router_ID | Router ID of the process | str
Export_Policy_Sources | Names of policies that determine which routes are exported into OSPF | Set of str
Area_Border_Router | Whether this process is at the area border (with at least one interface in Area 0 and one in another area) | bool

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
      <th>Process_ID</th>
      <th>Areas</th>
      <th>Reference_Bandwidth</th>
      <th>Router_ID</th>
      <th>Export_Policy_Sources</th>
      <th>Area_Border_Router</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as2border1</td>
      <td>default</td>
      <td>1</td>
      <td>['1']</td>
      <td>100000000.0</td>
      <td>2.1.1.1</td>
      <td>[]</td>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as2core1</td>
      <td>default</td>
      <td>1</td>
      <td>['1']</td>
      <td>100000000.0</td>
      <td>2.1.2.1</td>
      <td>[]</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as2dist1</td>
      <td>default</td>
      <td>1</td>
      <td>['1']</td>
      <td>100000000.0</td>
      <td>2.1.3.1</td>
      <td>[]</td>
      <td>False</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as2dist2</td>
      <td>default</td>
      <td>1</td>
      <td>['1']</td>
      <td>100000000.0</td>
      <td>2.1.3.2</td>
      <td>[]</td>
      <td>False</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as1border2</td>
      <td>default</td>
      <td>1</td>
      <td>['1']</td>
      <td>100000000.0</td>
      <td>1.2.2.2</td>
      <td>[]</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                      as2border1
    VRF                          default
    Process_ID                         1
    Areas                          ['1']
    Reference_Bandwidth      100000000.0
    Router_ID                    2.1.1.1
    Export_Policy_Sources             []
    Area_Border_Router             False
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### OSPF Interface Configuration

Returns OSPF configuration of interfaces.

Returns the interface level OSPF configuration details for the interfaces in the network which run OSPF.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
properties | Include properties matching this specifier. | [OspfInterfacePropertySpec](../specifiers.md#ospf-interface-property-specifier) | True | 

###### **Invocation**


```python
result = bf.q.ospfInterfaceConfiguration().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Interface | Interface | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
VRF | VRF name | str
Process_ID | Process ID | str
OSPF_Area_Name | OSPF area to which the interface belongs | int
OSPF_Enabled | Whether OSPF is enabled | bool
OSPF_Passive | Whether interface is in OSPF passive mode | bool
OSPF_Cost | OSPF cost if explicitly configured | int
OSPF_Network_Type | Type of OSPF network associated with the interface | str
OSPF_Hello_Interval | Interval in seconds between sending OSPF hello messages | int
OSPF_Dead_Interval | Interval in seconds before a silent OSPF neighbor is declared dead | int

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
      <th>Process_ID</th>
      <th>OSPF_Area_Name</th>
      <th>OSPF_Enabled</th>
      <th>OSPF_Passive</th>
      <th>OSPF_Cost</th>
      <th>OSPF_Network_Type</th>
      <th>OSPF_Hello_Interval</th>
      <th>OSPF_Dead_Interval</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as1core1[GigabitEthernet1/0]</td>
      <td>default</td>
      <td>1</td>
      <td>1</td>
      <td>True</td>
      <td>False</td>
      <td>1</td>
      <td>BROADCAST</td>
      <td>10</td>
      <td>40</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as1core1[GigabitEthernet0/0]</td>
      <td>default</td>
      <td>1</td>
      <td>1</td>
      <td>True</td>
      <td>False</td>
      <td>1</td>
      <td>BROADCAST</td>
      <td>10</td>
      <td>40</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as2dist1[Loopback0]</td>
      <td>default</td>
      <td>1</td>
      <td>1</td>
      <td>True</td>
      <td>False</td>
      <td>1</td>
      <td>BROADCAST</td>
      <td>10</td>
      <td>40</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as3core1[GigabitEthernet0/0]</td>
      <td>default</td>
      <td>1</td>
      <td>1</td>
      <td>True</td>
      <td>False</td>
      <td>1</td>
      <td>BROADCAST</td>
      <td>10</td>
      <td>40</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as3core1[GigabitEthernet1/0]</td>
      <td>default</td>
      <td>1</td>
      <td>1</td>
      <td>True</td>
      <td>False</td>
      <td>1</td>
      <td>BROADCAST</td>
      <td>10</td>
      <td>40</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Interface              as1core1[GigabitEthernet1/0]
    VRF                                         default
    Process_ID                                        1
    OSPF_Area_Name                                    1
    OSPF_Enabled                                   True
    OSPF_Passive                                  False
    OSPF_Cost                                         1
    OSPF_Network_Type                         BROADCAST
    OSPF_Hello_Interval                              10
    OSPF_Dead_Interval                               40
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### OSPF Area Configuration

Returns configuration parameters of OSPF areas.

Returns information about all OSPF areas defined across the network.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | 

###### **Invocation**


```python
result = bf.q.ospfAreaConfiguration().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
VRF | VRF | str
Process_ID | Process ID | str
Area | Area number | str
Area_Type | Area type | str
Active_Interfaces | Names of active interfaces | Set of str
Passive_Interfaces | Names of passive interfaces | Set of str

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
      <th>Process_ID</th>
      <th>Area</th>
      <th>Area_Type</th>
      <th>Active_Interfaces</th>
      <th>Passive_Interfaces</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as2dist2</td>
      <td>default</td>
      <td>1</td>
      <td>1</td>
      <td>NONE</td>
      <td>['GigabitEthernet0/0', 'GigabitEthernet1/0', 'Loopback0']</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as2border2</td>
      <td>default</td>
      <td>1</td>
      <td>1</td>
      <td>NONE</td>
      <td>['GigabitEthernet1/0', 'GigabitEthernet2/0', 'Loopback0']</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as3core1</td>
      <td>default</td>
      <td>1</td>
      <td>1</td>
      <td>NONE</td>
      <td>['GigabitEthernet0/0', 'GigabitEthernet1/0', 'Loopback0']</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as2core1</td>
      <td>default</td>
      <td>1</td>
      <td>1</td>
      <td>NONE</td>
      <td>['GigabitEthernet0/0', 'GigabitEthernet1/0', 'GigabitEthernet2/0', 'GigabitEthernet3/0', 'Loopback0']</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as1border2</td>
      <td>default</td>
      <td>1</td>
      <td>1</td>
      <td>NONE</td>
      <td>['GigabitEthernet1/0', 'Loopback0']</td>
      <td>[]</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                                                   as2dist2
    VRF                                                                     default
    Process_ID                                                                    1
    Area                                                                          1
    Area_Type                                                                  NONE
    Active_Interfaces     ['GigabitEthernet0/0', 'GigabitEthernet1/0', 'Loopback0']
    Passive_Interfaces                                                           []
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('aristaevpn')
```




    'aristaevpn'



##### Multi-chassis LAG

Returns MLAG configuration.

Lists the configuration settings for each MLAG domain in the network.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
mlagIds | Include MLAG IDs matching this specifier. | [MlagIdSpec](../specifiers.md#mlag-id-specifier) | True | 

###### **Invocation**


```python
result = bf.q.mlagProperties().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node name | str
MLAG_ID | MLAG domain ID | str
Peer_Address | Peer's IP address | str
Local_Interface | Local interface used for MLAG peering | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Source_Interface | Local interface used as source-interface for MLAG peering | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)

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
      <th>MLAG_ID</th>
      <th>Peer_Address</th>
      <th>Local_Interface</th>
      <th>Source_Interface</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>dc1-bl1a</td>
      <td>DC1_BL1</td>
      <td>10.255.252.11</td>
      <td>dc1-bl1a[Port-Channel3]</td>
      <td>dc1-bl1a[Vlan4094]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>dc1-bl1b</td>
      <td>DC1_BL1</td>
      <td>10.255.252.10</td>
      <td>dc1-bl1b[Port-Channel3]</td>
      <td>dc1-bl1b[Vlan4094]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>dc1-l2leaf5a</td>
      <td>DC1_L2LEAF5</td>
      <td>10.255.252.19</td>
      <td>dc1-l2leaf5a[Port-Channel3]</td>
      <td>dc1-l2leaf5a[Vlan4094]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>dc1-l2leaf5b</td>
      <td>DC1_L2LEAF5</td>
      <td>10.255.252.18</td>
      <td>dc1-l2leaf5b[Port-Channel3]</td>
      <td>dc1-l2leaf5b[Vlan4094]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>dc1-l2leaf6a</td>
      <td>DC1_L2LEAF6</td>
      <td>10.255.252.23</td>
      <td>dc1-l2leaf6a[Port-Channel3]</td>
      <td>dc1-l2leaf6a[Vlan4094]</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                               dc1-bl1a
    MLAG_ID                             DC1_BL1
    Peer_Address                  10.255.252.11
    Local_Interface     dc1-bl1a[Port-Channel3]
    Source_Interface         dc1-bl1a[Vlan4094]
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### IP Owners

Returns where IP addresses are attached in the network.

For each device, lists the mapping from IPs to corresponding interface(s) and VRF(s).

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
ips | Restrict output to only specified IP addresses. | [IpSpec](../specifiers.md#ip-specifier) | True | 
duplicatesOnly | Restrict output to only IP addresses that are duplicated (configured on a different node or VRF) in the snapshot. | bool | False | False

###### **Invocation**


```python
result = bf.q.ipOwners().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node hostname | str
VRF | VRF name | str
Interface | Interface name | str
IP | IP address | str
Mask | Network mask length | int
Active | Whether the interface is active | bool

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
      <th>Interface</th>
      <th>IP</th>
      <th>Mask</th>
      <th>Active</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as2dist2</td>
      <td>default</td>
      <td>Loopback0</td>
      <td>2.1.3.2</td>
      <td>32</td>
      <td>True</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as2dist1</td>
      <td>default</td>
      <td>Loopback0</td>
      <td>2.1.3.1</td>
      <td>32</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as2dept1</td>
      <td>default</td>
      <td>GigabitEthernet1/0</td>
      <td>2.34.201.4</td>
      <td>24</td>
      <td>True</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as2dept1</td>
      <td>default</td>
      <td>Loopback0</td>
      <td>2.1.1.2</td>
      <td>32</td>
      <td>True</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as3border2</td>
      <td>default</td>
      <td>GigabitEthernet1/0</td>
      <td>3.0.2.1</td>
      <td>24</td>
      <td>True</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node          as2dist2
    VRF            default
    Interface    Loopback0
    IP             2.1.3.2
    Mask                32
    Active            True
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Named Structures

Returns named structure definitions.

Return structures defined in the configurations, represented in a vendor-independent JSON format.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
structureTypes | Include structures of this type. | [NamedStructureSpec](../specifiers.md#named-structure-specifier) | True | 
structureNames | Include structures matching this name or regex. | str | True | 
ignoreGenerated | Whether to ignore auto-generated structures. | bool | True | True
indicatePresence | Output if the structure is present or absent. | bool | True | 

###### **Invocation**


```python
result = bf.q.namedStructures().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
Structure_Type | Structure type | str
Structure_Name | Structure name | str
Structure_Definition | Structure definition | dict

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
      <th>Structure_Type</th>
      <th>Structure_Name</th>
      <th>Structure_Definition</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>as1border1</td>
      <td>Community_Set_Match_Expr</td>
      <td>as1_community</td>
      <td>{'expr': {'class': 'org.batfish.datamodel.routing_policy.communities.CommunityMatchRegex', 'communityRendering': {'class': 'org.batfish.datamodel.routing_policy.communities.ColonSeparatedRendering'}, 'regex': '(,|\{|\}|^|$| )1:'}}</td>
    </tr>
    <tr>
      <th>1</th>
      <td>as1border2</td>
      <td>Community_Set_Match_Expr</td>
      <td>as1_community</td>
      <td>{'expr': {'class': 'org.batfish.datamodel.routing_policy.communities.CommunityMatchRegex', 'communityRendering': {'class': 'org.batfish.datamodel.routing_policy.communities.ColonSeparatedRendering'}, 'regex': '(,|\{|\}|^|$| )1:'}}</td>
    </tr>
    <tr>
      <th>2</th>
      <td>as2border1</td>
      <td>Community_Set_Match_Expr</td>
      <td>as1_community</td>
      <td>{'expr': {'class': 'org.batfish.datamodel.routing_policy.communities.CommunityMatchRegex', 'communityRendering': {'class': 'org.batfish.datamodel.routing_policy.communities.ColonSeparatedRendering'}, 'regex': '(,|\{|\}|^|$| )1:'}}</td>
    </tr>
    <tr>
      <th>3</th>
      <td>as2border2</td>
      <td>Community_Set_Match_Expr</td>
      <td>as1_community</td>
      <td>{'expr': {'class': 'org.batfish.datamodel.routing_policy.communities.CommunityMatchRegex', 'communityRendering': {'class': 'org.batfish.datamodel.routing_policy.communities.ColonSeparatedRendering'}, 'regex': '(,|\{|\}|^|$| )1:'}}</td>
    </tr>
    <tr>
      <th>4</th>
      <td>as3border1</td>
      <td>Community_Set_Match_Expr</td>
      <td>as1_community</td>
      <td>{'expr': {'class': 'org.batfish.datamodel.routing_policy.communities.CommunityMatchRegex', 'communityRendering': {'class': 'org.batfish.datamodel.routing_policy.communities.ColonSeparatedRendering'}, 'regex': '(,|\{|\}|^|$| )1:'}}</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                                                                                                                                                                                                                                as1border1
    Structure_Type                                                                                                                                                                                                                        Community_Set_Match_Expr
    Structure_Name                                                                                                                                                                                                                                   as1_community
    Structure_Definition    {'expr': {'class': 'org.batfish.datamodel.routing_policy.communities.CommunityMatchRegex', 'communityRendering': {'class': 'org.batfish.datamodel.routing_policy.communities.ColonSeparatedRendering'}, 'regex': '(,|\{|\}|^|$| )1:'}}
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Defined Structures

Lists the structures defined in the network.

Lists the structures defined in the network, along with the files and line numbers in which they are defined.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
filename | Include structures defined in the given file. | str | True | 
nodes | Include files used to generate nodes whose name matches this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | .*
names | Include structures whose name matches this string or regex. | str | True | .*
types | Include structures whose vendor-specific type matches this string or regex. | str | True | .*

###### **Invocation**


```python
result = bf.q.definedStructures().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Structure_Type | Vendor-specific type of the structure | str
Structure_Name | Name of the structure | str
Source_Lines | File and line numbers where the structure is defined | [FileLines](../datamodel.rst#pybatfish.datamodel.primitives.FileLines)

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
      <th>Structure_Type</th>
      <th>Structure_Name</th>
      <th>Source_Lines</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>extended ipv4 access-list line</td>
      <td>OUTSIDE_TO_INSIDE: permit ip any any</td>
      <td>configs/as2border1.cfg:[137]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>extended ipv4 access-list line</td>
      <td>blocktelnet: deny   tcp any any eq telnet</td>
      <td>configs/as2core1.cfg:[122]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>interface</td>
      <td>GigabitEthernet1/0</td>
      <td>configs/as1core1.cfg:[69, 70, 71]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>route-map-clause</td>
      <td>as3_to_as2 1</td>
      <td>configs/as3border1.cfg:[146, 147, 148, 149]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>extended ipv4 access-list</td>
      <td>101</td>
      <td>configs/as2border2.cfg:[140, 141]</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Structure_Type          extended ipv4 access-list line
    Structure_Name    OUTSIDE_TO_INSIDE: permit ip any any
    Source_Lines              configs/as2border1.cfg:[137]
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Referenced Structures

Lists the references in configuration files to vendor-specific structures.

Lists the references in configuration files to vendor-specific structures, along with the line number, the name and the type of the structure referenced, and configuration context in which each reference occurs.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include files used to generate nodes whose name matches this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
names | Include structures whose name matches this string or regex. | str | True | 
types | Include structures whose vendor-specific type matches this string or regex. | str | True | 

###### **Invocation**


```python
result = bf.q.referencedStructures().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Structure_Type | Type of structure referenced | str
Structure_Name | The referenced structure | str
Context | Configuration context in which the reference appears | str
Source_Lines | Lines where reference appears | [FileLines](../datamodel.rst#pybatfish.datamodel.primitives.FileLines)

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
      <th>Structure_Type</th>
      <th>Structure_Name</th>
      <th>Context</th>
      <th>Source_Lines</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>bgp neighbor</td>
      <td>1.10.1.1 (VRF default)</td>
      <td>bgp neighbor self ref</td>
      <td>configs/as1border1.cfg:[92, 111]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>bgp neighbor</td>
      <td>10.12.11.2 (VRF default)</td>
      <td>bgp neighbor self ref</td>
      <td>configs/as1border1.cfg:[114]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>bgp neighbor</td>
      <td>3.2.2.2 (VRF default)</td>
      <td>bgp neighbor self ref</td>
      <td>configs/as1border1.cfg:[112]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>bgp neighbor</td>
      <td>5.6.7.8 (VRF default)</td>
      <td>bgp neighbor self ref</td>
      <td>configs/as1border1.cfg:[113]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>bgp peer-group</td>
      <td>as1</td>
      <td>bgp neighbor peer-group</td>
      <td>configs/as1border1.cfg:[91]</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Structure_Type                        bgp neighbor
    Structure_Name              1.10.1.1 (VRF default)
    Context                      bgp neighbor self ref
    Source_Lines      configs/as1border1.cfg:[92, 111]
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Undefined References

Identifies undefined references in configuration.

Finds configurations that have references to named structures (e.g., ACLs) that are not defined. Such occurrences indicate errors and can have serious consequences in some cases.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Look for undefined references on nodes matching this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | .*

###### **Invocation**


```python
result = bf.q.undefinedReferences().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
File_Name | File containing reference | str
Struct_Type | Type of struct reference is supposed to be | str
Ref_Name | The undefined reference | str
Context | Context of undefined reference | str
Lines | Lines where reference appears | [FileLines](../datamodel.rst#pybatfish.datamodel.primitives.FileLines)

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
      <th>File_Name</th>
      <th>Struct_Type</th>
      <th>Ref_Name</th>
      <th>Context</th>
      <th>Lines</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>configs/as2core2.cfg</td>
      <td>route-map</td>
      <td>filter-bogons</td>
      <td>bgp inbound route-map</td>
      <td>configs/as2core2.cfg:[110]</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    File_Name            configs/as2core2.cfg
    Struct_Type                     route-map
    Ref_Name                    filter-bogons
    Context             bgp inbound route-map
    Lines          configs/as2core2.cfg:[110]
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('generate_questions')
```




    'generate_questions'



##### Unused Structures

Returns nodes with structures such as ACLs, routemaps, etc. that are defined but not used.

Return nodes with structures such as ACLs, routes, etc. that are defined but not used. This may represent a bug in the configuration, which may have occurred because a final step in a template or MOP was not completed. Or it could be harmless extra configuration generated from a master template that is not meant to be used on those nodes.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Look for unused structures on nodes matching this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | .*

###### **Invocation**


```python
result = bf.q.unusedStructures().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Structure_Type | Vendor-specific type of the structure | str
Structure_Name | Name of the structure | str
Source_Lines | File and line numbers where the structure is defined | [FileLines](../datamodel.rst#pybatfish.datamodel.primitives.FileLines)

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
      <th>Structure_Type</th>
      <th>Structure_Name</th>
      <th>Source_Lines</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>bgp peer-group</td>
      <td>as3</td>
      <td>configs/as1border1.cfg:[85]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>expanded community-list</td>
      <td>as1_community</td>
      <td>configs/as1border1.cfg:[121]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ipv4 prefix-list</td>
      <td>inbound_route_filter</td>
      <td>configs/as1border1.cfg:[131, 132]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>bgp peer-group</td>
      <td>as2</td>
      <td>configs/as1border2.cfg:[87]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>expanded community-list</td>
      <td>as1_community</td>
      <td>configs/as1border2.cfg:[123]</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Structure_Type                 bgp peer-group
    Structure_Name                            as3
    Source_Lines      configs/as1border1.cfg:[85]
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('aristaevpn')
```




    'aristaevpn'



##### VLAN Properties

Returns configuration settings of switched VLANs.

Lists information about implicitly and explicitly configured switched VLANs.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
interfaces | Include interfaces matching this specifier. | [InterfaceSpec](../specifiers.md#interface-specifier) | True | 
vlans | Include VLANs in this space. | str | True | 
excludeShutInterfaces | Exclude interfaces that are shutdown. | bool | True | 

###### **Invocation**


```python
result = bf.q.switchedVlanProperties().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
VLAN_ID | VLAN_ID | int
Interfaces | Switched interfaces carrying traffic for this VLAN | Set of [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
VXLAN_VNI | VXLAN VNI with which this VLAN is associated | int

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
      <th>VLAN_ID</th>
      <th>Interfaces</th>
      <th>VXLAN_VNI</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>dc1-bl1b</td>
      <td>250</td>
      <td>[dc1-bl1b[Port-Channel3], dc1-bl1b[Vlan250]]</td>
      <td>20250</td>
    </tr>
    <tr>
      <th>1</th>
      <td>dc1-leaf1a</td>
      <td>210</td>
      <td>[dc1-leaf1a[Vlan210]]</td>
      <td>20210</td>
    </tr>
    <tr>
      <th>2</th>
      <td>dc1-leaf1a</td>
      <td>211</td>
      <td>[dc1-leaf1a[Vlan211]]</td>
      <td>20211</td>
    </tr>
    <tr>
      <th>3</th>
      <td>dc1-leaf2a</td>
      <td>3764</td>
      <td>[dc1-leaf2a[Port-Channel3]]</td>
      <td>None</td>
    </tr>
    <tr>
      <th>4</th>
      <td>dc1-leaf2b</td>
      <td>3789</td>
      <td>[dc1-leaf2b[Port-Channel3]]</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                              dc1-bl1b
    VLAN_ID                                                250
    Interfaces    [dc1-bl1b[Port-Channel3], dc1-bl1b[Vlan250]]
    VXLAN_VNI                                            20250
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('ios_basic_vrrp')
```




    'ios_basic_vrrp'



##### VRRP Properties

Returns configuration settings of VRRP groups.

Lists information about VRRP groups on interfaces.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this specifier. | [NodeSpec](../specifiers.md#node-specifier) | True | 
interfaces | Include interfaces matching this specifier. | [InterfaceSpec](../specifiers.md#interface-specifier) | True | 
virtualAddresses | Include only groups with at least one virtual address matching this specifier. | [IpSpec](../specifiers.md#ip-specifier) | True | 
excludeShutInterfaces | Exclude interfaces that are shutdown. | bool | True | 

###### **Invocation**


```python
result = bf.q.vrrpProperties().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Interface | Interface | [Interface](../datamodel.rst#pybatfish.datamodel.primitives.Interface)
Group_Id | VRRP Group ID | int
Virtual_Addresses | Virtual Addresses | Set of str
Source_Address | Source Address used for VRRP messages | str
Priority | VRRP router priority | int
Preempt | Whether preemption is allowed | bool
Active | Whether the interface is active | bool

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
      <th>Group_Id</th>
      <th>Virtual_Addresses</th>
      <th>Source_Address</th>
      <th>Priority</th>
      <th>Preempt</th>
      <th>Active</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>br1[GigabitEthernet0/2]</td>
      <td>12</td>
      <td>['192.168.1.254']</td>
      <td>192.168.1.1/24</td>
      <td>110</td>
      <td>True</td>
      <td>True</td>
    </tr>
    <tr>
      <th>1</th>
      <td>br2[GigabitEthernet0/2]</td>
      <td>12</td>
      <td>['192.168.1.254']</td>
      <td>192.168.1.2/24</td>
      <td>100</td>
      <td>True</td>
      <td>True</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Interface            br1[GigabitEthernet0/2]
    Group_Id                                  12
    Virtual_Addresses          ['192.168.1.254']
    Source_Address                192.168.1.1/24
    Priority                                 110
    Preempt                                 True
    Active                                  True
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('a10')
```




    'a10'



##### A10 Virtual Server Configuration

Returns Virtual Server configuration of A10 devices.

Lists all the virtual-server to service-group to server mappings in A10 configurations.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | 
virtualServerIps | Include virtual servers whose IP match this specifier. | [IpSpec](../specifiers.md#ip-specifier) | True | 

###### **Invocation**


```python
result = bf.q.a10VirtualServerConfiguration().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
Virtual_Server_Name | Virtual Server Name | str
Virtual_Server_Enabled | Virtual Server Enabled | bool
Virtual_Server_IP | Virtual Server IP | str
Virtual_Server_Port | Virtual Server Port | int
Virtual_Server_Port_Enabled | Virtual Server Port Enabled | bool
Virtual_Server_Type | Virtual Server Type | str
Virtual_Server_Port_Type_Name | Virtual Server Port Type Name | str
Service_Group_Name | Service Group Name | str
Service_Group_Type | Service Group Type | str
Servers | List of Servers. Each item is a 4-tuple: Server Name, Port, IP Address, and Active Status. | Set of List of str
Source_NAT_Pool_Name | Source NAT Pool Name | str

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
      <th>Virtual_Server_Name</th>
      <th>Virtual_Server_Enabled</th>
      <th>Virtual_Server_IP</th>
      <th>Virtual_Server_Port</th>
      <th>Virtual_Server_Port_Enabled</th>
      <th>Virtual_Server_Type</th>
      <th>Virtual_Server_Port_Type_Name</th>
      <th>Service_Group_Name</th>
      <th>Service_Group_Type</th>
      <th>Servers</th>
      <th>Source_NAT_Pool_Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>lb42</td>
      <td>VS_TCP_80</td>
      <td>True</td>
      <td>10.0.0.1</td>
      <td>80</td>
      <td>True</td>
      <td>TCP</td>
      <td>None</td>
      <td>SG_TCP_80</td>
      <td>TCP</td>
      <td>[['SERVER1', '80', '10.1.10.11', 'active'], ['SERVER2', '80', '10.1.10.12', 'inactive']]</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                                                                                                                 lb42
    Virtual_Server_Name                                                                                             VS_TCP_80
    Virtual_Server_Enabled                                                                                               True
    Virtual_Server_IP                                                                                                10.0.0.1
    Virtual_Server_Port                                                                                                    80
    Virtual_Server_Port_Enabled                                                                                          True
    Virtual_Server_Type                                                                                                   TCP
    Virtual_Server_Port_Type_Name                                                                                        None
    Service_Group_Name                                                                                              SG_TCP_80
    Service_Group_Type                                                                                                    TCP
    Servers                          [['SERVER1', '80', '10.1.10.11', 'active'], ['SERVER2', '80', '10.1.10.12', 'inactive']]
    Source_NAT_Pool_Name                                                                                                 None
    Name: 0, dtype: object




```python
bf.set_network('generate_questions')
```




    'generate_questions'




```python
bf.set_snapshot('f5')
```




    'f5'



##### F5 BIG-IP VIP Configuration

Returns VIP configuration of F5 BIG-IP devices.

Lists all the VIP to server IP mappings contained in F5 BIP-IP configurations.

###### **Inputs**

Name | Description | Type | Optional | Default Value
--- | --- | --- | --- | --- 
nodes | Include nodes matching this name or regex. | [NodeSpec](../specifiers.md#node-specifier) | True | 

###### **Invocation**


```python
result = bf.q.f5BigipVipConfiguration().answer().frame()
```

###### **Return Value**

Name | Description | Type
--- | --- | ---
Node | Node | str
VIP_Name | Virtual Service Name | str
VIP_Endpoint | Virtual Service Endpoint | str
Servers | Servers | Set of str
Description | Description | str

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
      <th>VIP_Name</th>
      <th>VIP_Endpoint</th>
      <th>Servers</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>f5bigip</td>
      <td>/Common/virtual1</td>
      <td>192.0.2.1:80 TCP</td>
      <td>['10.0.0.1:80']</td>
      <td>virtual1 is cool</td>
    </tr>
    <tr>
      <th>1</th>
      <td>f5bigip</td>
      <td>/Common/virtual2</td>
      <td>192.0.2.2:80 TCP</td>
      <td>['10.0.0.2:80']</td>
      <td>pool2 is lame</td>
    </tr>
    <tr>
      <th>2</th>
      <td>f5bigip</td>
      <td>/Common/virtual3</td>
      <td>192.0.2.3:80 TCP</td>
      <td>['10.0.0.4:80', '10.0.0.3:80']</td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>



Print the first row of the returned Dataframe


```python
result.iloc[0]
```




    Node                     f5bigip
    VIP_Name        /Common/virtual1
    VIP_Endpoint    192.0.2.1:80 TCP
    Servers          ['10.0.0.1:80']
    Description     virtual1 is cool
    Name: 0, dtype: object


