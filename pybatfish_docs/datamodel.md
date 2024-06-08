Datamodel classes
===============================================================

Here we describe classes used in answers and their attributes, which may help you filter your answers as desired.

Base Types
-------------------------------------------------

_class_ pybatfish.datamodel.primitives.Edge(_node1: str_, _node1interface_, _node2: str_, _node2interface_)

A network edge (i.e., a link between two node/interface pairs).

Variables:

*   **node1** – First node name
    
*   **node1interface** – First node’s interface name
    
*   **node2** – Second node name
    
*   **node2interface** – Second node’s interface name
    

_class_ pybatfish.datamodel.primitives.Interface(_hostname: str_, _interface: str_)

A network interface — a combination of node and interface names.

Variables:

*   **hostname** – Node hostname to which this interface belongs
    
*   **interface** – Interface name
    

ACL Traces
---------------------------------------------------------------------

_class_ pybatfish.datamodel.acl.AclTrace(_events: List\[[AclTraceEvent](#pybatfish.datamodel.acl.AclTraceEvent "pybatfish.datamodel.acl.AclTraceEvent")\] \= NOTHING_)

The trace of a packet’s life through an ACL.

Variables:

**events** – A list of [`AclTraceEvent`](#pybatfish.datamodel.acl.AclTraceEvent "pybatfish.datamodel.acl.AclTraceEvent")

_class_ pybatfish.datamodel.acl.AclTraceEvent(_description: str | None \= None_)

One event corresponding to a packet’s life through an ACL.

Variables:

**description** – The description of the event

_class_ pybatfish.datamodel.acl.Fragment

An element in `TraceElement.fragments`, can be one of [`TextFragment`](#pybatfish.datamodel.acl.TextFragment "pybatfish.datamodel.acl.TextFragment") or [`LinkFragment`](#pybatfish.datamodel.acl.LinkFragment "pybatfish.datamodel.acl.LinkFragment").

_class_ pybatfish.datamodel.acl.LinkFragment(_text: str_, _vendorStructureId: [VendorStructureId](#pybatfish.datamodel.acl.VendorStructureId "pybatfish.datamodel.acl.VendorStructureId")_)

Represents a [`Fragment`](#pybatfish.datamodel.acl.Fragment "pybatfish.datamodel.acl.Fragment") that links to a vendor structure.

Variables:

*   **text** – Text content of the fragment
    
*   **vendorStructureId** – Link of the fragment
    

_class_ pybatfish.datamodel.acl.TextFragment(_text: str_)

Represents a plain-text [`Fragment`](#pybatfish.datamodel.acl.Fragment "pybatfish.datamodel.acl.Fragment").

Variables:

**text** – Text content of the fragment

_class_ pybatfish.datamodel.acl.TraceElement(_fragments: List\[[Fragment](#pybatfish.datamodel.acl.Fragment "pybatfish.datamodel.acl.Fragment")\]_)

Metadata used to create human-readable traces.

Variables:

**fragments** – A list of [`Fragment`](#pybatfish.datamodel.acl.Fragment "pybatfish.datamodel.acl.Fragment") which describes an element of a trace

_class_ pybatfish.datamodel.acl.TraceTree(_traceElement: [TraceElement](#pybatfish.datamodel.acl.TraceElement "pybatfish.datamodel.acl.TraceElement")_, _children: List\[[TraceTree](#pybatfish.datamodel.acl.TraceTree "pybatfish.datamodel.acl.TraceTree")\]_)

Represents a filter trace tree.

Variables:

*   **traceElement** – Metadata and description of the node
    
*   **children** – A list of sub-traces, i.e. children of the node
    

_class_ pybatfish.datamodel.acl.VendorStructureId(_filename: str_, _structureType: str_, _structureName: str_)

Identifies a vendor structure in a configuration file.

Variables:

*   **filename** – Filename of the configuration file
    
*   **structureType** – Type of the vendor structure
    
*   **structureName** – Name of the vendor structure
    

Flows and Packets
-----------------------------------------------------------------------------

_class_ pybatfish.datamodel.flow.ArpErrorStepDetail(_outputInterface: str | None_, _resolvedNexthopIp: str | None_)

Details of a step representing the arp error of a flow when sending out of a Hop.

Variables:

*   **outputInterface** – Interface of the Hop from which the flow exits
    
*   **resolvedNexthopIp** – Resolve next hop Ip address
    

_class_ pybatfish.datamodel.flow.DelegatedToNextVrf(_nextVrf: str_, _type: str \= 'DelegatedToNextVrf'_)

A flow being delegated to a different VRF for further processing.

_class_ pybatfish.datamodel.flow.DeliveredStepDetail(_outputInterface: str | None_, _resolvedNexthopIp: str | None_)

Details of a step representing the flow is delivered or exiting the network.

Variables:

*   **outputInterface** – Interface of the Hop from which the flow exits
    
*   **resolvedNexthopIp** – Resolve next hop Ip address
    

_class_ pybatfish.datamodel.flow.Discarded(_type: str \= 'Discarded'_)

A flow being discarded.

_class_ pybatfish.datamodel.flow.EnterInputIfaceStepDetail(_inputInterface: str_, _inputVrf: str | None_)

Details of a step representing the entering of a flow into a Hop.

Variables:

*   **inputInterface** – Interface of the Hop on which this flow enters
    
*   **inputVrf** – VRF associated with the input interface
    

_class_ pybatfish.datamodel.flow.ExitOutputIfaceStepDetail(_outputInterface: str_, _transformedFlow: str | None_)

Details of a step representing the exiting of a flow out of a Hop.

Variables:

*   **outputInterface** – Interface of the Hop from which the flow exits
    
*   **transformedFlow** – Transformed Flow if a source NAT was applied on the Flow
    

_class_ pybatfish.datamodel.flow.FilterStepDetail(_filter: str_, _filterType: str_, _inputInterface: str_, _flow: [Flow](#pybatfish.datamodel.flow.Flow "pybatfish.datamodel.flow.Flow") | None_)

Details of a step representing a filter step.

Variables:

*   **filter** – filter name
    
*   **type** – filter type
    
*   **inputInterface** – input interface of the flow
    
*   **flow** – current flow
    

_class_ pybatfish.datamodel.flow.Flow(_dscp_, _dstIp_, _dstPort_, _ecn_, _fragmentOffset_, _icmpCode_, _icmpVar_, _ingressInterface: str | None_, _ingressNode: str | None_, _ingressVrf: str | None_, _ipProtocol: str_, _packetLength: str_, _srcIp_, _srcPort_, _tcpFlagsAck_, _tcpFlagsCwr_, _tcpFlagsEce_, _tcpFlagsFin_, _tcpFlagsPsh_, _tcpFlagsRst_, _tcpFlagsSyn_, _tcpFlagsUrg_)

A concrete IPv4 flow.

Noteworthy attributes for flow inspection/filtering:

Variables:

*   **srcIP** – Source IP of the flow
    
*   **dstIP** – Destination IP of the flow
    
*   **srcPort** – Source port of the flow
    
*   **dstPort** – Destination port of the flow
    
*   **ipProtocol** – the IP protocol of the flow either as its name (e.g., TCP) for well-known protocols or a string like UNNAMED\_168
    
*   **ingressNode** – the node where the flow started (or entered the network)
    
*   **ingressInterface** – the interface name where the flow started (or entered the network)
    
*   **ingressVrf** – the VRF name where the flow started (or entered the network)
    

get\_flag\_str() → str

Returns a print friendly version of all set TCP flags.

get\_ip\_protocol\_str() → str

Returns a print-friendly version of IP protocol and any protocol-specific information (e.g., flags for TCP, type/code for ICMP.

_class_ pybatfish.datamodel.flow.ForwardedIntoVxlanTunnel(_vni: int_, _vtep: str_, _type: str \= 'ForwardedIntoVxlanTunnel'_)

A flow being forwarded into a VXLAN tunnel.

_class_ pybatfish.datamodel.flow.ForwardedOutInterface(_outputInterface: str_, _resolvedNextHopIp: str | None \= None_, _type: str \= 'ForwardedOutInterface'_)

A flow being forwarded out an interface.

If there is no resolved next-hop IP and this is the final step on this node, the destination IP of the flow will be used as the next gateway IP.

_class_ pybatfish.datamodel.flow.HeaderConstraints(_srcIps: str | None \= None_, _dstIps: str | None \= None_, _srcPorts\=None_, _dstPorts\=None_, _ipProtocols\=None_, _applications\=None_, _icmpCodes\=None_, _icmpTypes\=None_, _ecns\=None_, _dscps\=None_, _packetLengths\=None_, _fragmentOffsets\=None_, _tcpFlags\=None_)

Constraints on an IPv4 packet header space.

Specify constraints on packet headers by specifying lists of allowed values in each field of IP packet.

Variables:

*   **srcIps** (_str_) – Source location/IP
    
*   **dstIps** (_str_) – Destination location/IP
    
*   **srcPorts** – Source ports as list of ranges (e.g., `"22,53-99"`)
    
*   **dstPorts** – Destination ports as list of ranges, (e.g., `"22,53-99"`)
    
*   **applications** – Shorthands for application protocols (e.g., `SSH`, `DNS`, `SNMP`)
    
*   **ipProtocols** – List of well-known IP protocols (e.g., `TCP`, `UDP`, `ICMP`)
    
*   **icmpCodes** – List of integer ICMP codes
    
*   **icmpTypes** – List of integer ICMP types
    
*   **dscps** – List of allowed DSCP value ranges
    
*   **ecns** – List of allowed ECN values ranges
    
*   **packetLengths** – List of allowed packet length value ranges
    
*   **fragmentOffsets** – List of allowed fragmentOffset value ranges
    
*   **tcpFlags** – List of [`MatchTcpFlags`](#pybatfish.datamodel.flow.MatchTcpFlags "pybatfish.datamodel.flow.MatchTcpFlags") – conditions on which TCP flags to match
    

Lists of values in each fields are subject to a logical “OR”:

\>>> HeaderConstraints(ipProtocols\=\["TCP", "UDP"\])
HeaderConstraints(srcIps=None, dstIps=None, srcPorts=None, dstPorts=None, ipProtocols=\['TCP', 'UDP'\], applications=None,
icmpCodes=None, icmpTypes=None, ecns=None, dscps=None, packetLengths=None, fragmentOffsets=None, tcpFlags=None)

means allow TCP OR UDP.

Different fields are ANDed together:

\>>> HeaderConstraints(srcIps\="1.1.1.1", dstIps\="2.2.2.2", applications\=\["SSH"\])
HeaderConstraints(srcIps='1.1.1.1', dstIps='2.2.2.2', srcPorts=None, dstPorts=None, ipProtocols=None, applications=\['SSH'\],
icmpCodes=None, icmpTypes=None, ecns=None, dscps=None, packetLengths=None, fragmentOffsets=None, tcpFlags=None)

means an SSH connection originating at `1.1.1.1` and going to `2.2.2.2`

Any `None` values will be treated as unconstrained.

_classmethod_ of(_flow: [Flow](#pybatfish.datamodel.flow.Flow "pybatfish.datamodel.flow.Flow")_) → [HeaderConstraints](#pybatfish.datamodel.flow.HeaderConstraints "pybatfish.datamodel.flow.HeaderConstraints")

Create header constraints from an existing flow.

_class_ pybatfish.datamodel.flow.Hop(_node: str_, _steps: List\[Step\]_)

A single hop in a flow trace.

Variables:

*   **node** – Name of node considered as the Hop
    
*   **steps** – List of steps taken at this Hop
    

_class_ pybatfish.datamodel.flow.InboundStepDetail(_interface: str_)

Details of a step representing the receiving (acceptance) of a flow into a Hop.

Variables:

**interface** – interface that owns the destination IP

_class_ pybatfish.datamodel.flow.MatchSessionStepDetail(_sessionScope: SessionScope_, _sessionAction: SessionAction_, _matchCriteria: SessionMatchExpr_, _transformation: List\[FlowDiff\] | None \= NOTHING_)

Details of a step for when a flow matches a firewall session.

Variables:

*   **sessionScope** – Scope of flows session can match (incoming interfaces or originating VRF)
    
*   **sessionAction** – A SessionAction that the firewall takes for a matching session
    
*   **matchCriteria** – A SessionMatchExpr that describes the match criteria of the session
    
*   **transformation** – List of FlowDiffs that will be applied after session match
    

_class_ pybatfish.datamodel.flow.MatchTcpFlags(_tcpFlags: [TcpFlags](#pybatfish.datamodel.flow.TcpFlags "pybatfish.datamodel.flow.TcpFlags")_, _useAck: bool \= True_, _useCwr: bool \= True_, _useEce: bool \= True_, _useFin: bool \= True_, _usePsh: bool \= True_, _useRst: bool \= True_, _useSyn: bool \= True_, _useUrg: bool \= True_)

Match given [`TcpFlags`](#pybatfish.datamodel.flow.TcpFlags "pybatfish.datamodel.flow.TcpFlags").

For each bit in the TCP flags, a useX must be set to true, otherwise the bit is treated as “don’t care”.

Variables:

*   **tcpFlags** – tcp flags to match
    
*   **useAck**
    
*   **useCwr**
    
*   **useEce**
    
*   **useFin**
    
*   **usePsh**
    
*   **useRst**
    
*   **useSyn**
    
*   **useUrg**
    

_static_ match\_ack() → [MatchTcpFlags](#pybatfish.datamodel.flow.MatchTcpFlags "pybatfish.datamodel.flow.MatchTcpFlags")

Return match conditions checking that ACK bit is set.

Other bits may take any value.

_static_ match\_established() → List\[[MatchTcpFlags](#pybatfish.datamodel.flow.MatchTcpFlags "pybatfish.datamodel.flow.MatchTcpFlags")\]

Return a list of match conditions matching an established flow (ACK or RST bit set).

Other bits may take any value.

_static_ match\_not\_established() → List\[[MatchTcpFlags](#pybatfish.datamodel.flow.MatchTcpFlags "pybatfish.datamodel.flow.MatchTcpFlags")\]

Return a list of match conditions matching a non-established flow.

Meaning both ACK and RST bits are unset. Other bits may take any value.

_static_ match\_rst() → [MatchTcpFlags](#pybatfish.datamodel.flow.MatchTcpFlags "pybatfish.datamodel.flow.MatchTcpFlags")

Return match conditions checking that RST bit is set.

Other bits may take any value.

_static_ match\_syn() → [MatchTcpFlags](#pybatfish.datamodel.flow.MatchTcpFlags "pybatfish.datamodel.flow.MatchTcpFlags")

Return match conditions checking that the SYN bit is set.

Other bits may take any value.

_static_ match\_synack() → [MatchTcpFlags](#pybatfish.datamodel.flow.MatchTcpFlags "pybatfish.datamodel.flow.MatchTcpFlags")

Return match conditions checking that both the SYN and ACK bits are set.

Other bits may take any value.

_class_ pybatfish.datamodel.flow.OriginateStepDetail(_originatingVrf: str_)

Details of a step representing the originating of a flow in a Hop.

Variables:

**originatingVrf** – VRF from which the Flow originates

_class_ pybatfish.datamodel.flow.PathConstraints(_startLocation: str | None \= None_, _endLocation: str | None \= None_, _transitLocations: str | None \= None_, _forbiddenLocations: str | None \= None_)

Constraints on the path of a flow.

Variables:

*   **startLocation** – Location specification for where a flow is allowed to start
    
*   **endLocation** – Node specification for where a flow is allowed to terminate
    
*   **transitLocations** – Node specification for where a flow must transit
    
*   **forbiddenLocations** – Node specification for where a flow is _not_ allowed to transit
    

_class_ pybatfish.datamodel.flow.RoutingStepDetail(_routes: List\[RouteInfo\]_, _forwardingDetail: ForwardingDetail | None_, _arpIp: str | None_, _outputInterface: str | None_)

Details of a step representing the routing from input interface to output interface.

Variables:

**routes** – List of routes which were considered to select the forwarding action

_class_ pybatfish.datamodel.flow.SetupSessionStepDetail(_sessionScope: SessionScope_, _sessionAction: SessionAction_, _matchCriteria: SessionMatchExpr_, _transformation: List\[FlowDiff\] | None \= NOTHING_)

Details of a step for when a firewall session is created.

Variables:

*   **sessionScope** – Scope of flows session can match (incoming interfaces or originating VRF)
    
*   **sessionAction** – A SessionAction that the firewall takes for a return traffic matching the session
    
*   **matchCriteria** – A SessionMatchExpr that describes the match criteria of the session
    
*   **transformation** – List of FlowDiffs that will be applied on the return traffic matching the session
    

_class_ pybatfish.datamodel.flow.TcpFlags(_ack: bool \= False_, _cwr: bool \= False_, _ece: bool \= False_, _fin: bool \= False_, _psh: bool \= False_, _rst: bool \= False_, _syn: bool \= False_, _urg: bool \= False_)

Represents a set of TCP flags in a packet.

Variables:

*   **ack**
    
*   **cwr**
    
*   **ece**
    
*   **fin**
    
*   **psh**
    
*   **rst**
    
*   **syn**
    
*   **urg**
    

_class_ pybatfish.datamodel.flow.Trace(_disposition: str_, _hops: List\[[Hop](#pybatfish.datamodel.flow.Hop "pybatfish.datamodel.flow.Hop")\]_)

A trace of a flow through the network.

A Trace is a combination of hops and flow fate (i.e., disposition).

Variables:

*   **disposition** – Flow disposition
    
*   **hops** – A list of hops ([`Hop`](#pybatfish.datamodel.flow.Hop "pybatfish.datamodel.flow.Hop")) the flow took
    

_class_ pybatfish.datamodel.flow.TransformationStepDetail(_transformationType: str_, _flowDiffs: List\[FlowDiff\]_)

Details of a step representation a packet transformation.

Variables:

*   **transformationType** – The type of the transformation
    
*   **flowDiffs** – Set of changed flow fields
    

Reference Library
-----------------------------------------------------------------------------------------

_class_ pybatfish.datamodel.referencelibrary.AddressGroup(_name: str_, _addresses\=NOTHING_, _childGroupNames\=NOTHING_)

Information about an address group.

Variables:

*   **name** – The name of the group
    
*   **addresses** – a list of ‘addresses’ where each element is a string that represents an IP address (e.g., “1.1.1.1”), prefix (e.g., 1.1.1.0/24), or an address:mask (e.g., “1.1.1.1:0.0.0.8”).
    
*   **childGroupNames** – a list of names of child groups in this address group. The child groups must exist in the same reference book. Circular descendant relationships between address groups are allowed. The address group is considered to contain all addresses that are directly in it or in any of its descendants.
    

_class_ pybatfish.datamodel.referencelibrary.InterfaceGroup(_name: str_, _interfaces\=NOTHING_)

Information about an interface group.

Variables:

*   **name** – The name of the group
    
*   **interfaces** – a list of interfaces, of type `Interface`.
    

_class_ pybatfish.datamodel.referencelibrary.NodeRole(_\*args_, _\*\*kwargs_)

Information about a node role.

Variables:

*   **name** – Name of the node role.
    
*   **regex** – A regular expression over node names to describe nodes that belong to this role. The regular expression must be a valid **Java** regex.
    

_class_ pybatfish.datamodel.referencelibrary.NodeRoleDimension(_\*args_, _\*\*kwargs_)

Information about a node role dimension.

Variables:

*   **name** – Name of the node role dimension.
    
*   **roles** – The list of [`NodeRole`](#pybatfish.datamodel.referencelibrary.NodeRole "pybatfish.datamodel.referencelibrary.NodeRole") objects in this dimension (deprecated).
    
*   **roleDimensionMappings** – The list of [`RoleDimensionMapping`](#pybatfish.datamodel.referencelibrary.RoleDimensionMapping "pybatfish.datamodel.referencelibrary.RoleDimensionMapping") objects in this dimension.
    

_class_ pybatfish.datamodel.referencelibrary.NodeRolesData(_defaultDimension: str | None \= None_, _roleDimensionOrder\=NOTHING_, _roleMappings\=NOTHING_)

Information about a node roles data.

:ivar defaultDimension :ivar roleDimensionOrder: The precedence order of role dimensions. :ivar roleMappings: A list of [`RoleMapping`](#pybatfish.datamodel.referencelibrary.RoleMapping "pybatfish.datamodel.referencelibrary.RoleMapping") objects

_class_ pybatfish.datamodel.referencelibrary.ReferenceBook(_name: str_, _addressGroups\=NOTHING_, _interfaceGroups\=NOTHING_)

Information about a reference book.

Variables:

*   **name** – Name of the reference book.
    
*   **addressGroups** – A list of groups, of type [`AddressGroup`](#pybatfish.datamodel.referencelibrary.AddressGroup "pybatfish.datamodel.referencelibrary.AddressGroup").
    
*   **interfaceGroups** – A list of groups, of type [`InterfaceGroup`](#pybatfish.datamodel.referencelibrary.InterfaceGroup "pybatfish.datamodel.referencelibrary.InterfaceGroup").
    

_class_ pybatfish.datamodel.referencelibrary.ReferenceLibrary(_books\=NOTHING_)

Information about a reference library.

Variables:

**books** – A list of books of type [`ReferenceBook`](#pybatfish.datamodel.referencelibrary.ReferenceBook "pybatfish.datamodel.referencelibrary.ReferenceBook").

_class_ pybatfish.datamodel.referencelibrary.RoleDimensionMapping(_\*args_, _\*\*kwargs_)

Information about a role dimension mapping.

Variables:

*   **regex** – A regular expression over node names to describe nodes that belong to this role. The regular expression must be a valid **Java** regex.
    
*   **groups** – A list of group numbers (integers) that identify the role name for a given node name (default value is \[1\]).
    
*   **canonicalRoleNames** – A map from Java regexes over role names determined from the groups to a canonical set of role names for this dimension (default value is {}).
    

_class_ pybatfish.datamodel.referencelibrary.RoleMapping(_name: str_, _regex: str_, _roleDimensionGroups: Dict\[str, int\]_, _canonicalRoleNames: Dict\[str, Dict\[str, str\]\] \= NOTHING_)

A mapping from node name to role dimensions.

Variables:

*   **name** – (Optional) the name of the role mapping
    
*   **regex** – A java regex over hostnames, with groups to extract role data
    
*   **roleDimensionGroups** – a map from each role dimension name to the list of regex groups that signify the role name for that dimension.
    
*   **canonicalRoleNames** – for each role dimension, a map from the default role name that was obtained from the node name to a canonical role name
    

Routes
-------------------------------------------------------------------

_class_ pybatfish.datamodel.route.BgpRoute(_network: str_, _originatorIp: str_, _originType: str_, _protocol: str_, _asPath: list \= \[\]_, _communities: list \= \[\]_, _localPreference: int \= 0_, _metric: int \= 0_, _nextHopIp: str | None \= None_, _sourceProtocol: str | None \= None_, _tag: int \= 0_, _weight: int \= 0_)

A BGP routing advertisement.

Variables:

*   **network** – The network prefix advertised by the route.
    
*   **asPath** – The AS path of the route.
    
*   **communities** – The communities of the route.
    
*   **localPreference** – The local preference of the route.
    
*   **metric** – The metric of the route.
    
*   **nextHopIp** – The next hop IP of the route.
    
*   **protocol** – The protocol of the route.
    
*   **originatorIp** – The IP address of the originator of the route.
    
*   **originType** – The origin type of the route.
    
*   **sourceProtocol** – The source protocol of the route.
    
*   **tag** – The tag of the route.
    
*   **weight** – The weight of the route.
    

_class_ pybatfish.datamodel.route.BgpRouteConstraints(_prefix\=None_, _complementPrefix: bool | None \= None_, _localPreference\=None_, _med\=None_, _communities\=None_, _asPath\=None_)

Constraints on a BGP route announcement.

Specify constraints on route announcements by specifying allowed values in each field of the announcement.

Variables:

*   **prefix** – Allowed prefixes as a list of prefix ranges (e.g., “0.0.0.0/0:0-32”)
    
*   **complementPrefix** – A flag indicating that all prefixes except the ones in prefix are allowed
    
*   **localPreference** – List of allowed local preference integer ranges, as a string
    
*   **med** – List of allowed MED integer ranges, as a string
    
*   **communities** – List of allowed and disallowed community regexes
    
*   **asPath** – List of allowed and disallowed AS-path regexes
    

_class_ pybatfish.datamodel.route.BgpRouteDiff(_fieldName: str_, _oldValue: str_, _newValue: str_)

A difference between two BGP routes.

Variables:

*   **fieldName** – A Flow field name that has changed.
    
*   **oldValue** – The old value of the field.
    
*   **newValue** – The new value of the field.
    

_class_ pybatfish.datamodel.route.BgpRouteDiffs(_diffs: List\[[BgpRouteDiff](#pybatfish.datamodel.route.BgpRouteDiff "pybatfish.datamodel.route.BgpRouteDiff")\]_)

A set of differences between two BGP routes.

Variables:

**diffs** – The set of BgpRouteDiff objects.

_class_ pybatfish.datamodel.route.BgpSessionProperties(_localAs_, _remoteAs_, _localIp: str_, _remoteIp: str_)

Properties of a BGP session.

Properties that may be needed in order to simulate a route map that is used in a particular BGP session.

Variables:

*   **localAs** – The AS number of the session’s local peer
    
*   **remoteAs** – The AS number of the session’s remote peer
    
*   **localIp** – The IP address of the session’s local peer
    
*   **remoteIp** – The IP address of the session’s remote peer
    

_class_ pybatfish.datamodel.route.NextHop

A next-hop of a route

_class_ pybatfish.datamodel.route.NextHopDiscard(_type: str \= 'discard'_)

Indicates the packet should be dropped

_class_ pybatfish.datamodel.route.NextHopInterface(_interface: str_, _ip: str | None \= None_, _type: str \= 'interface'_)

A next-hop of a route with a fixed output interface and optional next gateway IP.

If there is no IP, the destination IP of the packet will be used as the next gateway IP.

_class_ pybatfish.datamodel.route.NextHopIp(_ip: str_, _type: str \= 'ip'_)

A next-hop of a route including the next gateway IP

_class_ pybatfish.datamodel.route.NextHopVrf(_vrf: str_, _type: str \= 'vrf'_)

A next-hop of a route indicating the destination IP should be resolved in another VRF

_class_ pybatfish.datamodel.route.NextHopVtep(_vni: int_, _vtep: str_, _type: str \= 'vtep'_)

A next-hop of a route indicating the packet should be routed through a VXLAN tunnel

Misc question outputs
-----------------------------------------------------------------------

_class_ pybatfish.datamodel.primitives.FileLines(_filename: str_, _lines: List\[int\] \= NOTHING_)

A class that represents a set of lines in a file.

Variables:

*   **filename** – The filename referenced
    
*   **lines** – A list of lines referenced