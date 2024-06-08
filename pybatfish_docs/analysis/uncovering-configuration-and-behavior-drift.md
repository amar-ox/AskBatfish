## Uncovering Configuration and Behavior Drift

When debugging network issues, it is important to understand how the network is different today compared to yesterday or to the desired golden state. A text diff of device configs is one way to do this, but it tends to be too noisy. It will show differences that you may not care about (e.g., changes in whitespace or timestamps), and it is hard to control what is reported. More importantly, text diffs also do not tell you about the impact of change on network behavior, such as if new traffic will be permitted or if some BGP edges will go down.

Batfish parses and builds a vendor-neutral model of device configs and behavior. This model enables you to learn how two snapshots of the network differ exactly along the aspects you care about. The behavior modeling of Batfish also lets you understand the full impact of these changes. This notebook illustrates this capability. 

We focus on the following differences across three categories. 

 1. Configuration settings
    1. Node-level properties
    1. Interface-level properties
    1. Properties of BGP peers 
 1. Structures and references
    1. Structures defined in device configs 
    1. Undefined references
 1. Network behavior
    1. BGP adjacencies
    1. ACL lines with treat flows differently 


These are examples of different types of changes that you can analyze using Batfish. You may be interested in a different aspects of your network, and you should be able to adapt the code below to suit your needs.

Text diff will help with the configuration settings category at best. The other two categories require understanding the structure of the config and the network behavior it induces. To illustrate this point, the text diff of example configs that we use in this notebook is below. 


```python
# Use recursive diff, followed by some pretty printing hacks
!diff -ur networks/drift/reference networks/drift/snapshot | sed -e 's;diff.*snapshot/\(configs.*cfg\);^-----------\1---------;g' | tr '^' '\n' | grep -v networks/drift
```


As we can see, it is difficult to grasp the nature and impact of the change from this output, not to mention that it is impossible to build automation on top of it (e.g., to alert on certain types of differences). We show next how Batfish offers a meaningful view of these differences and their impact on network behavior. 


```python
# Import packages, helpers, and load questions
%run startup.py
from drift_helper import diff_frames, diff_properties
bf = Session(host="localhost")

# Initialize both the snapshot and the reference that we want to use
NETWORK_NAME = "my_network"
SNAPSHOT_PATH = "networks/drift/snapshot"
REFERENCE_PATH = "networks/drift/reference"

bf.set_network(NETWORK_NAME)
bf.init_snapshot(SNAPSHOT_PATH, name="snapshot", overwrite=True)
bf.init_snapshot(REFERENCE_PATH, name="reference", overwrite=True)
```




    'reference'



### 1. Configuration settings

Let first uncover differences in configuration settings, starting with node-level properties.

#### 1A. Node-level properties

We focus on three example properties: 1) NTP servers, 2) Domain name, and 3) VRFs that exist on the device. The complete list of node properties extracted by Batfish is [here](https://batfish.readthedocs.io/en/latest/notebooks/configProperties.html#Node-Properties).

We will compute the property differences between across snapshots using Batfish questions. Batfish makes its models available via a [set of questions](https://batfish.readthedocs.io/en/latest/questions.html). When questions are run in [differential mode](https://pybatfish.readthedocs.io/en/latest/notebooks/differentialQuestions.html), it outputs how the answer differ across two snapshots. 


```python
# Properties of interest
NODE_PROPERTIES = ["NTP_Servers" , "Domain_Name", "VRFs"]

# Compute the difference across two snapshots and return a Pandas DataFrame
node_diff = bf.q.nodeProperties(
                properties=",".join(NODE_PROPERTIES)
            ).answer(
                snapshot="snapshot", 
                reference_snapshot="reference"
            ).frame()

# Print the DataFrame
show(node_diff.head())
```



The output above shows all property differences for all nodes. There is a row per node. We see that on `as1border1` the domain name has changed, and on `as1border2` the set of NTP servers has changes. There is no other difference for any other node for the chosen properties.

This structured output can be transformed and fed into any type of automation, e.g., to alert you when an important property has changed. We can also generate readable drift reports using the helper function we defined above.


```python
# Print readable messages on the differences
diff_properties(node_diff, "Node", ["Node"], NODE_PROPERTIES)
```

    
    Differences for Node=as1border1
        Domain_Name: lab.local -> lab.localp
    
    Differences for Node=as1border2
        NTP_Servers: ['23.23.23.23', '18.18.18.18'] -> ['18.18.18.19', '18.18.18.18']


#### 1B. Interface-level properties

We next check if any interface-level properties have changed. We again focus on three example settings: 1) whether the interface is active, 2) description, and 3) primary IP address. The complete list of interface settings extracted by Batfish are [here](https://batfish.readthedocs.io/en/latest/notebooks/configProperties.html#Interface-Properties).


```python
# Properties of interest
INTERFACE_PROPERTIES = ['Active', 'Description', 'Primary_Address']

# Compute the difference across two snapshots and return a Pandas DataFrame
interface_diff = bf.q.interfaceProperties(
                    properties=",".join(INTERFACE_PROPERTIES)
                ).answer(
                    snapshot="snapshot", 
                    reference_snapshot="reference"
                ).frame()

# Print a readable version of the differences
diff_properties(interface_diff, "Interface", ["Interface"], INTERFACE_PROPERTIES)
```

    
    Differences for Interface=as2border2[GigabitEthernet0/0]
        Active: True -> False
        Primary_Address: 10.23.21.2/24 -> None
    
    Differences for Interface=as2core1[GigabitEthernet0/0]
        Description: None -> "To as2border1 GigabitEthernet1/0"
    
    Differences for Interface=as2core1[GigabitEthernet1/0]
        Description: None -> "To as2border2 GigabitEthernet2/0"


We see that the interface `GigabitEthernet0/0` on `as2border2` has been shutdown and its address assignment has been eliminated. We also see that the description has been added for two interfaces on `as2core1`.

#### 1C. BGP peer properties

We next check properties of BGP peers, focusing on four example properties: 1) description, 2) peer group, 3) Import policies applied to the peer, and 4) Export policies applied to the peer. The complete list of BGP peers properties is [here](https://batfish.readthedocs.io/en/latest/notebooks/configProperties.html#BGP-Peer-Configuration).


```python
# Properties of interest
BGP_PEER_PROPERTIES = ['Remote_AS', 'Description', 'Peer_Group', 'Import_Policy', 'Export_Policy']

# Compute the difference across two snapshots and return a Pandas DataFrame
bgp_peer_diff = bf.q.bgpPeerConfiguration(
                    properties=",".join(BGP_PEER_PROPERTIES)
                ).answer(
                    snapshot="snapshot", 
                    reference_snapshot="reference"
                ).frame()

#Print readable messages on the differences
diff_properties(bgp_peer_diff, "BgpPeer", ["Node", "VRF", "Local_Interface", "Remote_IP"], BGP_PEER_PROPERTIES)
```

    
    BgpPeers only in snapshot
        Node=as2dept1, VRF=default, Local_Interface=None, Remote_IP=2.34.209.3
    
    Differences for Node=as2dist1, VRF=default, Local_Interface=None, Remote_IP=2.34.101.4
        Peer_Group: dept -> dept2
        Import_Policy: ['dept_to_as2dist'] -> []
        Export_Policy: ['as2dist_to_dept'] -> []


The output shows that a new peer has been defined on `as2dept1` with remote IP address `2.34.209.3`; and the peer group has changed for an an existing peer on `as2dist1`, which then also led to its import and export policies changing. This correlated change in import/export policies are invisible in the text diff.

### 2. Structures and references

Batfish models include all structures defined in device configs (e.g., ACLs, prefix-lists) and how they are referenced in other parts of the config. You can use these models to learn if structures have been defined or deleted, which represents a major change in the configuration. 

#### 2A. Structures defined in configs

The `definedStructures` question is the basis for learning about structures defined in the config.


```python
# Extract defined structures from both snapshots as a Pandas DataFrame
snapshot_structures = bf.q.definedStructures().answer(snapshot="snapshot").frame()
reference_structures = bf.q.definedStructures().answer(snapshot="reference").frame()

# Show me what the information looks like by printing the first few rows
show(snapshot_structures.head())
```



The output snippet shows how Batfish captures the exact lines in each file where each structure is defined. We can process this information from the two snapshots to produce a report on all differences.


```python
# Remove the line numbers but keep the filename. We don't care about where in the file structure are defined.
snapshot_structures_without_lines = snapshot_structures[['Structure_Type', 'Structure_Name']].assign(
    File_Name=snapshot_structures["Source_Lines"].map(lambda x: x.filename))
reference_structures_without_lines = reference_structures[['Structure_Type', 'Structure_Name']].assign(
    File_Name=reference_structures["Source_Lines"].map(lambda x: x.filename))

# Print a readable message on the differences
diff_frames(snapshot_structures_without_lines, 
            reference_structures_without_lines, 
            "DefinedStructure")
```

    
    DefinedStructures only in snapshot
         File_Name=configs/as3border1.cfg, Structure_Name=bogons, Structure_Type=ipv4 prefix-list
         File_Name=configs/as2dist1.cfg, Structure_Name=dept2, Structure_Type=bgp peer-group
         File_Name=configs/as2dist1.cfg, Structure_Name=dept_to_as2dist 200, Structure_Type=route-map-clause
         File_Name=configs/as2dist2.cfg, Structure_Name=105: permit ip host 3.0.3.0 host 255.255.255.0, Structure_Type=extended ipv4 access-list line
         File_Name=configs/as2dist1.cfg, Structure_Name=102: permit tcp host 2.128.0.0 host 255.255.0.0, Structure_Type=extended ipv4 access-list line
    
    DefinedStructures only in reference
         File_Name=configs/as2dist1.cfg, Structure_Name=dept, Structure_Type=bgp peer-group


We can easily see in this output that a BGP peer group named `dept2` was newly defined on `as2dist1` and a prefix-list named `bogons` was defined on as2border1. We also see that the peer group named `dept` was removed from `as2dist1`. The peer group change is related to what we saw earlier with a peer property changing. This view shows that the entire structure has been removed and defined.

#### 2B. Undefined structure references

References to undefined structures are symptoms of configuration errors. Using the `undefinedReferences` question, Batfish can help you understand if new undefined references have been introduced or old ones have been cleared. 


```python
# Extract undefined references from both snapshots as a Pandas DataFrame
snapshot_undefined_references=bf.q.undefinedReferences().answer(snapshot="snapshot").frame()
reference_undefined_references= bf.q.undefinedReferences().answer(snapshot="reference").frame()

# Show me all undefined references in the snapshot
show(snapshot_undefined_references)
```



The output shows that there are three undefined references in the snapshot. Let us find out which ones were newly introduced relative to the reference.


```python
# Remove Lines since we don't care about where it was referenced
snapshot_undefined_references_without_lines = snapshot_undefined_references.drop(columns=['Lines'])
reference_undefined_references_without_lines = reference_undefined_references.drop(columns=['Lines'])

# Print a readable message on the differences
diff_frames(snapshot_undefined_references_without_lines, 
            reference_undefined_references_without_lines, 
            "UndefinedRefeference")
```

    
    UndefinedRefeferences only in snapshot
         Ref_Name=dept_community_new, File_Name=configs/as2dist1.cfg, Struct_Type=community-list, Context=route-map match community-list
         Ref_Name=dept, File_Name=configs/as2dist1.cfg, Struct_Type=undeclared bgp peer-group, Context=bgp peer-group referenced before defined


We thus see that, of the three undefined references that we saw earlier, two were newly introduced and one exists in both snapshots. 

### 3. Network behavior

We now turn our attention to behavioral differences between network snapshots, starting with changes in BGP adjacencies.

#### 3A. BGP adjacencies

The `bgpEdges` question of Batfish enables you to learn about all BGP adjacencines in the network, as follows.


```python
# Get the edges from both snapshots as Pandas DataFrames
snapshot_bgp_edges = bf.q.bgpEdges().answer(snapshot="snapshot").frame()
reference_bgp_edges = bf.q.bgpEdges().answer(snapshot="reference").frame()

# Show me the schema by printing the first few rows
show(snapshot_bgp_edges.head())
```


We see that Batfish knows which BGP edges in the snapshot come up and shows key information about them. We can use the answer to this question to learn which edges exist only in the snapshot or only in the refrence.


```python
# Retain only columns we care about for this analysis
snapshot_bgp_edges_nodes = snapshot_bgp_edges[['Node', 'Remote_Node']]
reference_bgp_edges_nodes = reference_bgp_edges[['Node', 'Remote_Node']]

# DataFrames contain one edge per direction; keep only one direction
snapshot_bgp_bidir_edges_nodes = snapshot_bgp_edges_nodes[
                                    snapshot_bgp_edges_nodes['Node'] < snapshot_bgp_edges_nodes['Remote_Node']
                                  ]
reference_bgp_bidir_edges_nodes = reference_bgp_edges_nodes[
                                    reference_bgp_edges_nodes['Node'] < reference_bgp_edges_nodes['Remote_Node']
                                  ]

# Print a readable message on the differences
diff_frames(snapshot_bgp_bidir_edges_nodes, 
            reference_bgp_bidir_edges_nodes, 
            "BgpEdge")
```

    
    BgpEdges only in reference
         Node=as2border2, Remote_Node=as3border1


One BGP edge exists only in the reference, that is, it disappeared in the snapshot. We can find more about this edge, like so:


```python
# Find the matching edge in the reference edges answer from before
missing_snapshot_edge = reference_bgp_edges[
                           (reference_bgp_edges['Node']=="as2border2") 
                           & (reference_bgp_edges['Remote_Node']=="as3border1")
                         ]

# Print the edge information
show(missing_snapshot_edge)
```



Do you recall the interface on as2border2 that was shut earlier? This BGP edge was removed because of that interface shutdown (which you confirm using IP of the interface---`10.23.21.2/24`).

#### 3B. ACL behavior

To compute the behavior differences between ACLs, we use the [compare filters question](https://pybatfish.readthedocs.io/en/latest/notebooks/differentialQuestions.html#Compare-Filters). It returns pairs of lines, one from the filter definition in each snapshot, that match the same flow(s) but treat them differently (i.e. one permits and the other denies the flow).


```python
# compute behavior differences between ACLs
compare_filters = bf.q.compareFilters().answer(
                                            snapshot='snapshot',
                                            reference_snapshot='reference'
                                        ).frame()

# print the result
show(compare_filters)
```


We see that the only difference in the ACL behaviors of the two snapshots is for ACL `105` on `as2dist`. Line `permit ip host 3.0.3.0 host 255.255.255.0` in the snapshot permits some flows that were being denied in the reference snapshhot because of the implicit deny at the end of the ACL. Thus, we have permitted flows that were not being permitted before.

If you were paying attention to the text diff above, the result above may surprise you. The text diff (relevant snippet repeated below) showed that ACL `102` on `as2dist1` changed as well.


```python
!diff -ur networks/drift/reference/configs/as2dist1.cfg networks/drift/snapshot/configs/as2dist1.cfg | grep -A 7 '@@ -113,6 +113,7 @@'
```

    @@ -113,6 +113,7 @@
     no ip http server
     no ip http secure-server
     !
    +access-list 102 permit tcp host 2.128.0.0 host 255.255.0.0
     access-list 102 permit ip host 2.128.0.0 host 255.255.0.0
     access-list 105 permit ip host 1.0.1.0 host 255.255.255.0
     access-list 105 permit ip host 1.0.2.0 host 255.255.255.0


You may have expected a behahvior diff corresponding to this change, but Batfish analysis reveals that that didn't happen. The added line is permitting TCP traffic between two hosts for which IP traffic was already permitted, so no new traffic was permitted. So, either this change was unnecessary or someone mistyped the host addresses. 

### Summary

Batfish enables you to easily understand how your device configs differ from a historial reference or golden versions. It provides structured information about not only changes to settings in configs but also about changes in network behavior. This information provides important context beyond simple text diffs and can be inserted into an automated pipeline that alerts on important changes. 
 
