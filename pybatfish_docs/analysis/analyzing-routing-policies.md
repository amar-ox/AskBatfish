## Analyzing BGP Route Policies

Route policies for BGP are complex and error prone, which is why some of the biggest outages in the Internet involve misconfigured route policies that end up leaking routes or accepting routes they shouldn't (e.g., [BGP  Leak Causing Internet Outages in Japan and Beyond](https://www.bgpmon.net/bgp-leak-causing-internet-outages-in-japan-and-beyond/), [How a Tiny Error Shut Off the Internet for Parts of the US](https://www.wired.com/story/how-a-tiny-error-shut-off-the-internet-for-parts-of-the-us/), [Telia engineer error to blame for massive net outage](https://www.theregister.com/2016/06/20/telia_engineer_blamed_massive_net_outage/)). While it is often clear to network engineers what the route policy should or should not do (e.g., see [MANRS guidelines](https://www.manrs.org/)), ensuring that the route policy implementation is correct is notoriously hard.

In this notebook we show how you can use Batfish to validate your route policies. Batfish's `testRoutePolicies` question provides an easy way to test route-policy behavior---given a route, it shows how it is transformed (or denied) by the route policy.  Batfish's `searchRoutePolicies` actively searches for routes that cause a policy to violate its intent.

To illustrate these capabilities, we'll use an example network with two border routers, named `border1` and `border2`.  Each router has a BGP session with a customer network and a BGP session with a provider network.  Our goal in this notebook is to validate the in-bound route policy from the customer, called `from_customer`, and the out-bound route policy to the provider, called `to_provider`.

The intent of the `from_customer` route policy is:

 * filter private addresses
 * only permit routes to known prefixes if they have the correct origin AS
 * tag permitted routes with an appropriate community, and update the local preference

The intent of the `to_provider` route policy is:

 * advertise all prefixes that we own
 * advertise all customer routes
 * don't advertise anything else

We'll start, as usual, by initializing the example network that we will use in this notebook.


```python
# Import packages
%run startup.py
from pybatfish.datamodel.route import BgpRouteConstraints
bf = Session(host="localhost")

# Initialize a network and snapshot
NETWORK_NAME = "example_network"
SNAPSHOT_NAME = "example_snapshot"

SNAPSHOT_PATH = "networks/route-analysis"

bf.set_network(NETWORK_NAME)
bf.init_snapshot(SNAPSHOT_PATH, name=SNAPSHOT_NAME, overwrite=True)
```




    'example_snapshot'



### Example 1: Filter private addresses in-bound


When peering with external entities, an almost universally-desired policy is to filter out all announcements of the private IP address space. For our network, we'd like to ensure that the two `from_customer` route policies properly filter such announcements.  

Traditionally you might validate this policy through some form testing that involves the production or a lab device.  With Batfish's `testRoutePolicies` question we can easily test a route policy's behavior without access to a device.


```python
# Create an example route to use for testing
inRoute1 = BgpRoute(network="10.0.0.0/24", 
                    originatorIp="4.4.4.4", 
                    originType="egp", 
                    protocol="bgp")

# Test how our policy treats this route
result = bf.q.testRoutePolicies(policies="from_customer", 
                             direction="in", 
                             inputRoutes=[inRoute1]).answer().frame()
# Pretty print the result
show(result)
```


<style type="text/css">
#T_pybfstyle_row0_col0, #T_pybfstyle_row0_col1, #T_pybfstyle_row0_col2, #T_pybfstyle_row0_col3, #T_pybfstyle_row0_col4, #T_pybfstyle_row0_col5, #T_pybfstyle_row0_col6, #T_pybfstyle_row1_col0, #T_pybfstyle_row1_col1, #T_pybfstyle_row1_col2, #T_pybfstyle_row1_col3, #T_pybfstyle_row1_col4, #T_pybfstyle_row1_col5, #T_pybfstyle_row1_col6 {
  text-align: left;
  vertical-align: top;
}
</style>
<table id="T_pybfstyle">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_pybfstyle_level0_col0" class="col_heading level0 col0" >Node</th>
      <th id="T_pybfstyle_level0_col1" class="col_heading level0 col1" >Policy_Name</th>
      <th id="T_pybfstyle_level0_col2" class="col_heading level0 col2" >Input_Route</th>
      <th id="T_pybfstyle_level0_col3" class="col_heading level0 col3" >Action</th>
      <th id="T_pybfstyle_level0_col4" class="col_heading level0 col4" >Output_Route</th>
      <th id="T_pybfstyle_level0_col5" class="col_heading level0 col5" >Difference</th>
      <th id="T_pybfstyle_level0_col6" class="col_heading level0 col6" >Trace</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_pybfstyle_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_pybfstyle_row0_col0" class="data row0 col0" >border1</td>
      <td id="T_pybfstyle_row0_col1" class="data row0 col1" >from_customer</td>
      <td id="T_pybfstyle_row0_col2" class="data row0 col2" >Network: 10.0.0.0/24<br>AS Path: []<br>Communities: []<br>Local Preference: 0<br>Metric: 0<br>Next Hop IP: None<br>Originator IP: 4.4.4.4<br>Origin Type: egp<br>Protocol: bgp<br>Source Protocol: None<br>Tag: 0<br>Weight: 0</td>
      <td id="T_pybfstyle_row0_col3" class="data row0 col3" >DENY</td>
      <td id="T_pybfstyle_row0_col4" class="data row0 col4" >None</td>
      <td id="T_pybfstyle_row0_col5" class="data row0 col5" >None</td>
      <td id="T_pybfstyle_row0_col6" class="data row0 col6" ><ul><li>Matched route-map from_customer clause 100</li></ul></td>
    </tr>
    <tr>
      <th id="T_pybfstyle_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_pybfstyle_row1_col0" class="data row1 col0" >border2</td>
      <td id="T_pybfstyle_row1_col1" class="data row1 col1" >from_customer</td>
      <td id="T_pybfstyle_row1_col2" class="data row1 col2" >Network: 10.0.0.0/24<br>AS Path: []<br>Communities: []<br>Local Preference: 0<br>Metric: 0<br>Next Hop IP: None<br>Originator IP: 4.4.4.4<br>Origin Type: egp<br>Protocol: bgp<br>Source Protocol: None<br>Tag: 0<br>Weight: 0</td>
      <td id="T_pybfstyle_row1_col3" class="data row1 col3" >DENY</td>
      <td id="T_pybfstyle_row1_col4" class="data row1 col4" >None</td>
      <td id="T_pybfstyle_row1_col5" class="data row1 col5" >None</td>
      <td id="T_pybfstyle_row1_col6" class="data row1 col6" ><ul><li>Matched route-map from_customer clause 100</li></ul></td>
    </tr>
  </tbody>
</table>



The first line of code above creates a `BgpRoute` object that specifies the input route announcement to use for testing, which in this case announces the prefix 10.0.0.0/24, has an originator IP that we arbitrarily chose, and has default values for other parts of the announcement.  The second line uses `testRoutePolicies` to test the behavior of the two `from_customer` route policies on this announcement.

The output of the question shows the results of the test. As we see in the `Action` column, in both border routers, the `from_customer` route policy properly denies this private address. The `Trace` column tell us that this happened because the input route matched clause `100` of the route map.

That result gives us some confidence in our route policies, but it is just a single test.  We can run `testRoutePolicies` on more private addresses to ensure they are denied.  

However, how can we be sure that *all* private addresses are denied by the two in-bound route maps?  For that, we will use the `searchRoutePolicies` question and change our perspective a bit.  Instead of testing individual routes, we will ask Batfish to search for a route-policy behavior that violates our intent.  If we get one or more results, then we've found a bug.  If we get no results, then we can be sure that our configurations satisfy the intent, since Batfish explores *all possible* route-policy behaviors.


```python
# Define the space of private addresses
privateIps = ["10.0.0.0/8:8-32", 
              "172.16.0.0/12:12-32", 
              "192.168.0.0/16:16-32"]

# Specify all route announcements for the private space
inRoutes1 = BgpRouteConstraints(prefix=privateIps)

# Verify that no such announcement is permitted by our policy
result = bf.q.searchRoutePolicies(policies="from_customer", 
                                 inputConstraints=inRoutes1, 
                                 action="permit").answer().frame()
# Pretty print the result
show(result)
```


<style type="text/css">
#T_pybfstyle_row0_col0, #T_pybfstyle_row0_col1, #T_pybfstyle_row0_col2, #T_pybfstyle_row0_col3, #T_pybfstyle_row0_col4, #T_pybfstyle_row0_col5, #T_pybfstyle_row0_col6 {
  text-align: left;
  vertical-align: top;
}
</style>
<table id="T_pybfstyle">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_pybfstyle_level0_col0" class="col_heading level0 col0" >Node</th>
      <th id="T_pybfstyle_level0_col1" class="col_heading level0 col1" >Policy_Name</th>
      <th id="T_pybfstyle_level0_col2" class="col_heading level0 col2" >Input_Route</th>
      <th id="T_pybfstyle_level0_col3" class="col_heading level0 col3" >Action</th>
      <th id="T_pybfstyle_level0_col4" class="col_heading level0 col4" >Output_Route</th>
      <th id="T_pybfstyle_level0_col5" class="col_heading level0 col5" >Difference</th>
      <th id="T_pybfstyle_level0_col6" class="col_heading level0 col6" >Trace</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_pybfstyle_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_pybfstyle_row0_col0" class="data row0 col0" >border2</td>
      <td id="T_pybfstyle_row0_col1" class="data row0 col1" >from_customer</td>
      <td id="T_pybfstyle_row0_col2" class="data row0 col2" >Network: 192.168.0.0/32<br>AS Path: []<br>Communities: []<br>Local Preference: 100<br>Metric: 0<br>Next Hop IP: 0.0.0.1<br>Originator IP: 0.0.0.0<br>Origin Type: egp<br>Protocol: bgp<br>Source Protocol: None<br>Tag: 0<br>Weight: 0</td>
      <td id="T_pybfstyle_row0_col3" class="data row0 col3" >PERMIT</td>
      <td id="T_pybfstyle_row0_col4" class="data row0 col4" >Network: 192.168.0.0/32<br>AS Path: []<br>Communities: [20:30]<br>Local Preference: 300<br>Metric: 0<br>Next Hop IP: 0.0.0.1<br>Originator IP: 0.0.0.0<br>Origin Type: egp<br>Protocol: bgp<br>Source Protocol: None<br>Tag: 0<br>Weight: 0</td>
      <td id="T_pybfstyle_row0_col5" class="data row0 col5" >Communities: [] --> [20:30]<br>Local Preference: 100 --> 300</td>
      <td id="T_pybfstyle_row0_col6" class="data row0 col6" ><ul><li>Matched route-map from_customer clause 400</li></ul></td>
    </tr>
  </tbody>
</table>



The first line above specifies the space of all private IP prefixes.  The second line creates a `BgpRouteConstraints` object, which is like the `BgpRoute` object we saw earlier but represents a set of announcements rather than a single one.  In this case, we are interested in all announcements that announce a prefix in `privateIps`.  Finally, the third line of code uses `searchRoutePolicies` to search for an announcement in the set `inRoutes` that is permitted by the `from_customer` route policy.

There are no results for `border1`, which means that its `from_customer` route policy properly filters *all* private addresses. However, the result for `border2` shows that its version of `from_customer` permits an announcement for the prefix 192.168.0.0/32.  The table also shows the route announcement that will be produced by `from_customer` in this case, along with a "diff" of the input and output announcements. 

Inspecting the configurations, we see that both routers deny all announcements for prefixes in the prefix list `private-ips`. However, the definition of `private-ips` on `border2` accidentally omitted the `ge /16` clause, so only applied to /16 prefixes. Relevant parts of the config at `border2` are:

```
ip prefix-list private-ips seq 15 permit 192.168.0.0/16  // <-- missing ge /16

...

route-map from_customer deny 100
 match ip address prefix-list private-ips
!
....

route-map from_customer permit 400
 set community 20:30
 set local-preference 300
!
```

Batfish is able to correctly model the semantics of route maps and prefix lists and deduce that some prefix with private IPs will get past our policy.

### Example 2: Filter based on origin AS in-bound


Another common BGP policy is to make sure that announcements for certain prefixes (e.g., customer-owned prefixes) are acccepted only if they have a specific origin AS. 

For our example, we assume that announcements for routes with any prefix in the range 5.5.5.0/24:24-32 should originate from the AS 44.  We will use `searchRoutePolicies` to ask: *Is there any permitted announcement for a prefix in the range 5.5.5.0/24:24-32 that does not originate from AS 44?*


```python
# Define expected prefixes
knownPrefixes = "5.5.5.0/24:24-32"

# Define invalid AS-path -- all those that do not have 44 as the origin AS
badOrigin = "!/( |^)44$/"

# Specify the route announcements we must not permit
inRoutes2 = BgpRouteConstraints(prefix=knownPrefixes, asPath=badOrigin)

# Verify that our policy does not permit any such announcement
result = bf.q.searchRoutePolicies(policies="from_customer", 
                                 inputConstraints=inRoutes2, 
                                 action="permit").answer().frame()
show(result)
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
<table border="1" class="dataframe tex2jax_ignore">
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
  </tbody>
</table>
</div>


The first line above defines the known prefixes.  The second line specifies that we are interested in AS-paths that do not end in 44, using the same syntax that Batfish uses for regular-expression [specifiers](https://github.com/batfish/batfish/blob/master/questions/Parameters.md#set-of-enums-or-names).  Specifically, a regular expression is surrounded by `/` characters, and the leading `!` indicates that we are interested in AS-paths that do not match this regular expression.  Since there are no results, we can be sure that the our intent is satisfied.

### Example 3: Set attributes in-bound

As the third and final policy for inbound routes, let's make sure that our `from_customer` route policies tag each permitted route with the community 20:30 and set the local preference to 300.  To start, we can use `testRoutePolicies` to test this property on a specific route announcement.


```python
# Define a test route and test what the policy does to it
inRoute3 = BgpRoute(network="2.0.0.0/8", 
                    originatorIp="4.4.4.4", 
                    originType="egp", 
                    protocol="bgp")
result = bf.q.testRoutePolicies(policies="from_customer", 
                               direction="in", 
                               inputRoutes=[inRoute3]).answer().frame()
show(result)
```


<style type="text/css">
#T_pybfstyle_row0_col0, #T_pybfstyle_row0_col1, #T_pybfstyle_row0_col2, #T_pybfstyle_row0_col3, #T_pybfstyle_row0_col4, #T_pybfstyle_row0_col5, #T_pybfstyle_row0_col6, #T_pybfstyle_row1_col0, #T_pybfstyle_row1_col1, #T_pybfstyle_row1_col2, #T_pybfstyle_row1_col3, #T_pybfstyle_row1_col4, #T_pybfstyle_row1_col5, #T_pybfstyle_row1_col6 {
  text-align: left;
  vertical-align: top;
}
</style>
<table id="T_pybfstyle">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_pybfstyle_level0_col0" class="col_heading level0 col0" >Node</th>
      <th id="T_pybfstyle_level0_col1" class="col_heading level0 col1" >Policy_Name</th>
      <th id="T_pybfstyle_level0_col2" class="col_heading level0 col2" >Input_Route</th>
      <th id="T_pybfstyle_level0_col3" class="col_heading level0 col3" >Action</th>
      <th id="T_pybfstyle_level0_col4" class="col_heading level0 col4" >Output_Route</th>
      <th id="T_pybfstyle_level0_col5" class="col_heading level0 col5" >Difference</th>
      <th id="T_pybfstyle_level0_col6" class="col_heading level0 col6" >Trace</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_pybfstyle_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_pybfstyle_row0_col0" class="data row0 col0" >border1</td>
      <td id="T_pybfstyle_row0_col1" class="data row0 col1" >from_customer</td>
      <td id="T_pybfstyle_row0_col2" class="data row0 col2" >Network: 2.0.0.0/8<br>AS Path: []<br>Communities: []<br>Local Preference: 0<br>Metric: 0<br>Next Hop IP: None<br>Originator IP: 4.4.4.4<br>Origin Type: egp<br>Protocol: bgp<br>Source Protocol: None<br>Tag: 0<br>Weight: 0</td>
      <td id="T_pybfstyle_row0_col3" class="data row0 col3" >PERMIT</td>
      <td id="T_pybfstyle_row0_col4" class="data row0 col4" >Network: 2.0.0.0/8<br>AS Path: []<br>Communities: [20:30]<br>Local Preference: 0<br>Metric: 0<br>Next Hop IP: None<br>Originator IP: 4.4.4.4<br>Origin Type: egp<br>Protocol: bgp<br>Source Protocol: None<br>Tag: 0<br>Weight: 0</td>
      <td id="T_pybfstyle_row0_col5" class="data row0 col5" >Communities: [] --> [20:30]</td>
      <td id="T_pybfstyle_row0_col6" class="data row0 col6" ><ul><li>Matched route-map from_customer clause 400</li></ul></td>
    </tr>
    <tr>
      <th id="T_pybfstyle_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_pybfstyle_row1_col0" class="data row1 col0" >border2</td>
      <td id="T_pybfstyle_row1_col1" class="data row1 col1" >from_customer</td>
      <td id="T_pybfstyle_row1_col2" class="data row1 col2" >Network: 2.0.0.0/8<br>AS Path: []<br>Communities: []<br>Local Preference: 0<br>Metric: 0<br>Next Hop IP: None<br>Originator IP: 4.4.4.4<br>Origin Type: egp<br>Protocol: bgp<br>Source Protocol: None<br>Tag: 0<br>Weight: 0</td>
      <td id="T_pybfstyle_row1_col3" class="data row1 col3" >PERMIT</td>
      <td id="T_pybfstyle_row1_col4" class="data row1 col4" >Network: 2.0.0.0/8<br>AS Path: []<br>Communities: [20:30]<br>Local Preference: 300<br>Metric: 0<br>Next Hop IP: None<br>Originator IP: 4.4.4.4<br>Origin Type: egp<br>Protocol: bgp<br>Source Protocol: None<br>Tag: 0<br>Weight: 0</td>
      <td id="T_pybfstyle_row1_col5" class="data row1 col5" >Communities: [] --> [20:30]<br>Local Preference: 0 --> 300</td>
      <td id="T_pybfstyle_row1_col6" class="data row1 col6" ><ul><li>Matched route-map from_customer clause 400</li></ul></td>
    </tr>
  </tbody>
</table>



The results show what each router does to the test route. This information can be seen in the `Output_Route` column, which shows the full output route announcement, as well as the `Difference` column, which shows the differences between the input and output route announcements. We see that there is an error in `border1`'s configuration:  the permitted route is tagged with community 20:30, but its local preference is not set to 300.  However, `border2` is doing the right thing.   A look at the configuration for `border1` reveals that the `set local-preference` line is accidentally omitted from one clause of the policy.

This example shows why testing is so important.  However, we'd like to make sure that there aren't any other lurking bugs.  We can use `searchRoutePolicies` for this purpose.  First we'll check that *all* permitted routes are tagged with the community 20:30.  To check this property, we will leverage the ability of `searchRoutePolicies` not only to search for particular *input* announcements, but also to search for particular *output* announcements.  In this case, we will ask:  *Is there a permitted route whose output announcement is not tagged with community 20:30?*


```python
# Define invalid communities -- those that do not contain 20:30
outRoutes3a = BgpRouteConstraints(communities="!20:30")
# Verify that our policy does not output routes with such communities
result = bf.q.searchRoutePolicies(policies="from_customer", 
                                 action="permit", 
                                 outputConstraints=outRoutes3a).answer().frame()
show(result)
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
<table border="1" class="dataframe tex2jax_ignore">
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
  </tbody>
</table>
</div>


There are no results, so we know that our intent is satisfied on both routers.  

Now let's do a similar thing to check that the local preference is properly set.  We've already seen that `border1` is not properly setting the local preference, so we'll just check that `border2`'s configuration is correct.


```python
# Verify that all permitted routes have the expected local preference
outRoutes3b = BgpRouteConstraints(localPreference="!300")
result = bf.q.searchRoutePolicies(nodes="border2", 
                                 policies="from_customer", 
                                 action="permit", 
                                 outputConstraints=outRoutes3b).answer().frame()
show(result)
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
<table border="1" class="dataframe tex2jax_ignore">
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
  </tbody>
</table>
</div>


There are no results for `border2`'s `from_customer` policy, so we have the strong assurance that it is properly setting the local preference on *all* permitted routes.

### Example 4: Announce your own addresses out-bound


Ok, now let's validate the `to_provider` route policies. The first thing we want to ensure is that they allow all our addresses to be advertised.  Lets assume that these are addresses in the ranges 1.2.3.0/24:24-32 and 1.2.4.0/24:24-32.  We can use `searchRoutePolicies` to validate this property.  Specifically, we ask:  *Is there an announcement for an address that we own that is denied by `to_provider`?*


```python
# Verify that no route for our address space is ever denied by to_provider policies
ownedSpace=["1.2.3.0/24:24-32", "1.2.4.0/24:24-32"]
inRoutes4 = BgpRouteConstraints(prefix=ownedSpace)
result = bf.q.searchRoutePolicies(policies="to_provider", 
                                 inputConstraints=inRoutes4, 
                                 action="deny").answer().frame()
show(result)
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
<table border="1" class="dataframe tex2jax_ignore">
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
  </tbody>
</table>
</div>


Since there are no results, this implies that no such announcement exists.  Hurray!

### Example 5: Announce your customers' routes out-bound

Next we will check that the `to_provider` route policies are properly announcing our customers' routes.  These are identified by announcements that are tagged with the community 20:30, as we saw earlier.


```python
# Verify that no customer routes (i.e., those tagged with the community 20:30) is ever denied
customerCommunities = "20:30"
inRoutes5 = BgpRouteConstraints(communities=customerCommunities)
result = bf.q.searchRoutePolicies(policies="to_provider", 
                                 inputConstraints=inRoutes5, 
                                 action="deny").answer().frame()
show(result)
```


<style type="text/css">
#T_pybfstyle_row0_col0, #T_pybfstyle_row0_col1, #T_pybfstyle_row0_col2, #T_pybfstyle_row0_col3, #T_pybfstyle_row0_col4, #T_pybfstyle_row0_col5, #T_pybfstyle_row0_col6 {
  text-align: left;
  vertical-align: top;
}
</style>
<table id="T_pybfstyle">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_pybfstyle_level0_col0" class="col_heading level0 col0" >Node</th>
      <th id="T_pybfstyle_level0_col1" class="col_heading level0 col1" >Policy_Name</th>
      <th id="T_pybfstyle_level0_col2" class="col_heading level0 col2" >Input_Route</th>
      <th id="T_pybfstyle_level0_col3" class="col_heading level0 col3" >Action</th>
      <th id="T_pybfstyle_level0_col4" class="col_heading level0 col4" >Output_Route</th>
      <th id="T_pybfstyle_level0_col5" class="col_heading level0 col5" >Difference</th>
      <th id="T_pybfstyle_level0_col6" class="col_heading level0 col6" >Trace</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_pybfstyle_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_pybfstyle_row0_col0" class="data row0 col0" >border2</td>
      <td id="T_pybfstyle_row0_col1" class="data row0 col1" >to_provider</td>
      <td id="T_pybfstyle_row0_col2" class="data row0 col2" >Network: 10.0.0.0/8<br>AS Path: []<br>Communities: [20:30]<br>Local Preference: 100<br>Metric: 0<br>Next Hop IP: 0.0.0.1<br>Originator IP: 0.0.0.0<br>Origin Type: egp<br>Protocol: bgp<br>Source Protocol: None<br>Tag: 0<br>Weight: 0</td>
      <td id="T_pybfstyle_row0_col3" class="data row0 col3" >DENY</td>
      <td id="T_pybfstyle_row0_col4" class="data row0 col4" >None</td>
      <td id="T_pybfstyle_row0_col5" class="data row0 col5" >None</td>
      <td id="T_pybfstyle_row0_col6" class="data row0 col6" ><ul></ul></td>
    </tr>
  </tbody>
</table>



There are no results for `border1`, so it permits announcement of all customer routes.  But `border2` has a bug since it denies some customer routes, a concrete example of which is shown in the `Input_Route` column.  

A look at the configuration reveals that someone has fat-fingered the definition of the community list:

```
ip community-list cust_community permit 2:30
```

Such mistakes are difficult to find with any other tool.

### Example 6: Don't advertise anything else out-bound


Last, we want to make sure that our `to_provider` route policies don't announce any routes other than the ones we own and the ones that our customers own.  We will use `searchRoutePolicies` to ask: *Is there a permitted route whose prefix is not one we own and which is not tagged with the community 20:30?*


```python
# Set of routes that are neither in our owned space nor have the customer community (20:30)
inRoutes6 = BgpRouteConstraints(prefix=ownedSpace, 
                                complementPrefix=True, 
                                communities="!20:30")

# Verify that no such route is permitted
result = bf.q.searchRoutePolicies(policies="to_provider", 
                                 inputConstraints=inRoutes6, 
                                 action="permit").answer().frame()
show(result)
```


<style type="text/css">
#T_pybfstyle_row0_col0, #T_pybfstyle_row0_col1, #T_pybfstyle_row0_col2, #T_pybfstyle_row0_col3, #T_pybfstyle_row0_col4, #T_pybfstyle_row0_col5, #T_pybfstyle_row0_col6 {
  text-align: left;
  vertical-align: top;
}
</style>
<table id="T_pybfstyle">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_pybfstyle_level0_col0" class="col_heading level0 col0" >Node</th>
      <th id="T_pybfstyle_level0_col1" class="col_heading level0 col1" >Policy_Name</th>
      <th id="T_pybfstyle_level0_col2" class="col_heading level0 col2" >Input_Route</th>
      <th id="T_pybfstyle_level0_col3" class="col_heading level0 col3" >Action</th>
      <th id="T_pybfstyle_level0_col4" class="col_heading level0 col4" >Output_Route</th>
      <th id="T_pybfstyle_level0_col5" class="col_heading level0 col5" >Difference</th>
      <th id="T_pybfstyle_level0_col6" class="col_heading level0 col6" >Trace</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_pybfstyle_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_pybfstyle_row0_col0" class="data row0 col0" >border2</td>
      <td id="T_pybfstyle_row0_col1" class="data row0 col1" >to_provider</td>
      <td id="T_pybfstyle_row0_col2" class="data row0 col2" >Network: 10.0.0.0/8<br>AS Path: []<br>Communities: [2:30]<br>Local Preference: 100<br>Metric: 0<br>Next Hop IP: 0.0.0.1<br>Originator IP: 0.0.0.0<br>Origin Type: egp<br>Protocol: bgp<br>Source Protocol: None<br>Tag: 0<br>Weight: 0</td>
      <td id="T_pybfstyle_row0_col3" class="data row0 col3" >PERMIT</td>
      <td id="T_pybfstyle_row0_col4" class="data row0 col4" >Network: 10.0.0.0/8<br>AS Path: []<br>Communities: [2:30]<br>Local Preference: 100<br>Metric: 0<br>Next Hop IP: 0.0.0.1<br>Originator IP: 0.0.0.0<br>Origin Type: egp<br>Protocol: bgp<br>Source Protocol: None<br>Tag: 0<br>Weight: 0</td>
      <td id="T_pybfstyle_row0_col5" class="data row0 col5" ></td>
      <td id="T_pybfstyle_row0_col6" class="data row0 col6" ><ul><li>Matched route-map to_provider clause 200</li></ul></td>
    </tr>
  </tbody>
</table>



The `complementPrefix` parameter above is used to indicate that we are interested in routes whose prefix is *not* in `ownedSpace`.

Since there are no results for `border1` we can be sure that it is not advertising any routes that it shouldn't be.  We already saw in the previous example that `border2` accidentally advertises routes tagged with 2:30, and that error shows up again here.

### Current Status

The `testRoutePolicies` question supports all of the vendors and route-policy features that are supported by Batfish. 

The `searchRoutePolicies` question has been (at the time of this writing) newly added to Batfish.  It supports all of the vendors that are supported by Batfish.  The question supports a host of common route policy behaviors and intents, as shown above, but it does not currently support all routing constructs.  See its [documentation](https://pybatfish.readthedocs.io/en/latest/notebooks/routingProtocols.html#Search-Route-Policies) for details, and feel free to reach out to us with questions or specific needs.  We'll continue to enhance its coverage.

### Summary


In this notebook we showed you two ways to use Batfish to check whether your route policies meet your intent:  
1. The `testRoutePolicies` question allows you to easily test the behavior of a route policy offline, without access to the live network.  
2. The `searchRoutePolicies` question allows you to search for violations of intent, identifying concrete errors if they exist and providing strong correctness guarantees if not.


***
### Get involved with the Batfish community

Join our community on [Slack](https://join.slack.com/t/batfish-org/shared_invite/enQtMzA0Nzg2OTAzNzQ1LTcyYzY3M2Q0NWUyYTRhYjdlM2IzYzRhZGU1NWFlNGU2MzlhNDY3OTJmMDIyMjQzYmRlNjhkMTRjNWIwNTUwNTQ) and [GitHub](https://github.com/batfish/batfish). 
