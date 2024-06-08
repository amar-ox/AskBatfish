## Validating Configuration Settings with Batfish

Network engineers routinely need to validate configuration settings of various devices in their network. In a multi-vendor network, this validation can be hard and few tools exist today to enable this basic task. However, the vendor-independent models of Batfish and its querying mechanisms make such validation almost trivial.

In this notebook, we show how to validate configuration settings with Batfish. More specifically, we examine how the configuration of NTP servers can be validated. The same validation scenarios can be performed for other configuration settings of nodes (such as dns servers, tacacs servers, snmp communities, VRFs, etc.) interfaces (such as MTU, bandwidth, input and output access lists, state, etc.), VRFs, BGP and OSPF sessions, and more.

Check out a video demo of this notebook [here](https://youtu.be/qOXRaVs1Uz4).

### Initializing our Network and Snapshot

`SNAPSHOT_PATH` below can be updated to point to a custom snapshot directory, see the [Batfish instructions](https://github.com/batfish/batfish/wiki/Packaging-snapshots-for-analysis) for how to package data for analysis.<br>
More example networks are available in the [networks](https://github.com/batfish/batfish/tree/master/networks) folder of the Batfish repository.


```python
# Import packages
%run startup.py
bf = Session(host="localhost")

# Initialize a network and snapshot
NETWORK_NAME = "example_network"
SNAPSHOT_NAME = "example_snapshot"

SNAPSHOT_PATH = "networks/example"

bf.set_network(NETWORK_NAME)
bf.init_snapshot(SNAPSHOT_PATH, name=SNAPSHOT_NAME, overwrite=True)
```




    'example_snapshot'



The network snapshot that we initialized above is illustrated below. You can download/view devices' configuration files [here](https://github.com/batfish/pybatfish/tree/master/jupyter_notebooks/networks/example). We will focus on the validation for the six **border** routers. 

![example-network](https://raw.githubusercontent.com/batfish/pybatfish/master/jupyter_notebooks/networks/example/example-network.png)

### Extracting configured NTP servers
This can be done using the `nodeProperties()` question.


```python
# Set the property that we want to extract
COL_NAME = "NTP_Servers"

# Extract NTP servers for all routers with 'border' in their name
node_props = bf.q.nodeProperties(
    nodes="/border/", 
    properties=COL_NAME).answer().frame()
node_props
```


The `.frame()` function call above returns a [Pandas](https://pandas.pydata.org/pandas-docs/stable/) data frame that contains the answer.

### Validating NTP Servers Configuration
Depending on the network's policy, there are several possible validation scenarios for NTP-servers configuration:
1. Every node has at least one NTP server configured.
2. Every node has at least one NTP server configured from the reference set.
3. Every node has the reference set of NTP servers configured.
4. Every node has NTP servers that match those in a per-node database.

We demonstrate each scenario below.

#### Validation scenario 1: Every node has at least one NTP server configured
Now that we have the list of NTP servers, let's check if at least one server is configured on the border routers. We accomplish that by using ([lambda expressions](https://docs.python.org/3/reference/expressions.html#lambda)) to identify nodes where the list is empty.


```python
# Find nodes that have no NTP servers configured
ns_violators = node_props[node_props[COL_NAME].apply(
    lambda x: len(x) == 0)]
ns_violators
```



#### Validation scenario 2: Every node has at least one NTP server configured from the reference set.
Now if we want to validate that configured _NTP servers_ should contain at least one _NTP server_ from a reference set, we can use the command below. It identifies any node whose configured set of _NTP servers_ does not overlap with the reference set at all.


```python
# Define the reference set of NTP servers
ref_ntp_servers = set(["23.23.23.23"])

# Find nodes that have no NTP server in common with the reference set
ns_violators = node_props[node_props[COL_NAME].apply(
    lambda x: len(ref_ntp_servers.intersection(set(x))) == 0)]
ns_violators
```

Because `as1border1` has no configured NTP servers, it clearly violates our assertion, and so does `as2border2` which has a configured server but not one that is present in the reference set.

#### Validation scenario 3: Every node has the reference set of NTP servers configured
A common use case for validating _NTP servers_ involves checking that the set of _NTP servers_ exactly matches a desired reference set. Such validation is quite straightforward as well. 


```python
# Find violating nodes whose configured NTP servers do not match the reference set
ns_violators = node_props[node_props[COL_NAME].apply(
    lambda x: ref_ntp_servers != set(x))]
ns_violators
```


As we can see, all border nodes violate this condition.

A slightly advanced version of pandas filtering can also show us which configured _NTP servers_ are missing or extra (compared to the reference set) at each node.


```python
# Find extra and missing servers at each node
ns_extra = node_props[COL_NAME].map(lambda x: set(x) - ref_ntp_servers)
ns_missing = node_props[COL_NAME].map(lambda x: ref_ntp_servers - set(x))

# Join these columns up with the node columns for a complete view
diff_df = pd.concat([node_props["Node"],
                     ns_extra.rename('extra-{}'.format(COL_NAME)),
                     ns_missing.rename('missing-{}'.format(COL_NAME))],
                    axis=1)
diff_df
```



#### Validation scenario 4: Every node has _NTP servers_ that match those in a per-node database.
Every node should match its reference set of _NTP Servers_ which may be stored in an external database. This check enables easy validation of configuration settings that differ acorss nodes.

We assume data from the database is fetched in the following format, where node names are dictionary keys and specific properties are defined in a property-keyed dictionary per node.


```python
# Mock reference-node-data, presumably taken from an external database
database = {'as1border1': {'NTP_Servers': ['23.23.23.23'],
                           'DNS_Servers': ['1.1.1.1']},
            'as1border2': {'NTP_Servers': ['23.23.23.23'],
                           'DNS_Servers': ['1.1.1.1']},
            'as2border1': {'NTP_Servers': ['18.18.18.18', '23.23.23.23'],
                           'DNS_Servers': ['2.2.2.2']},
            'as2border2': {'NTP_Servers': ['18.18.18.18'],
                           'DNS_Servers': ['1.1.1.1']},
            'as3border1': {'NTP_Servers': ['18.18.18.18', '23.23.23.23'],
                           'DNS_Servers': ['2.2.2.2']},
            'as3border2': {'NTP_Servers': ['18.18.18.18', '23.23.23.23'],
                           'DNS_Servers': ['2.2.2.2']},
            }
```

Note that there is an extra property in this dictionary that we don't care about comparing right now: `dns-server`. We will filter out this property below, before comparing the data from `Batfish` to that in the database. 

After a little massaging, the database and `Batfish` data can be compared to generate two sets of servers: missing (i.e., present in the database but not in the configurations) and extra (i.e., present in the configurations but not in the database).


```python
# Transpose database data so each node has its own row
database_df = pd.DataFrame(data=database).transpose()

# Index on node for easier comparison
df_node_props = node_props.set_index('Node')

# Select only columns present in node_props (get rid of the extra dns-servers column)
df_db_node_props = database_df[df_node_props.columns].copy()

# Convert server lists into sets to support arithmetic below
df_node_props[COL_NAME] = df_node_props[COL_NAME].apply(set)
df_db_node_props[COL_NAME] = df_db_node_props[COL_NAME].apply(set)

# Figure out what servers are in the configs but not the database and vice versa
missing_servers = (df_db_node_props - df_node_props).rename(
    columns={COL_NAME: 'missing-{}'.format(COL_NAME)})
extra_servers = (df_node_props - df_db_node_props).rename(
    columns={COL_NAME: 'extra-{}'.format(COL_NAME)})
result = pd.concat([missing_servers, extra_servers], axis=1, sort=False)
result
```


### Continue exploring

We showed you how to extract the database of configured _NTP servers_ for every node and how to test that the settings are correct for a variety of desired test configurations. The underlying principles can be applied to other network configurations, such as [interfaceProperties](https://pybatfish.readthedocs.io/en/latest/notebooks/configProperties.html#Interface-Properties), [bgpProcessConfiguration](https://pybatfish.readthedocs.io/en/latest/notebooks/configProperties.html#BGP-Process-Configuration), [ospfProcessConfiguration](https://pybatfish.readthedocs.io/en/latest/notebooks/configProperties.html#OSPF-Process-Configuration) etc.

For example `interfaceProperties()` question can be used to fetch properties like interface MTU using a simple command.


```python
# Extract interface MTU for Ethernet0/0 interfaces on border routers
interface_mtu = bf.q.interfaceProperties(
    interfaces="/border/[Ethernet0/0]",
    properties="MTU").answer().frame()
interface_mtu
```
