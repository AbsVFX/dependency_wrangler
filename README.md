# Dependency Wrangler
Originally designed to combat dependency orchestration between Side FX Houdini and Thinkbox Deadline for complex FX 
workflows, The Dependency Wrangler module handles the analysis of a node-based graph to filter out use-able nodes for a
specific use case, in addition to providing an overview of nodes within a given tree in a universal manor

## Usage
This library is compatible with both Python 2.7+ and Python 3.8+. 
### Side FX: Houdini
In this example, the Dependency Wrangler will get all items within a tree from a custom Houdini Asset within the ROP
context and extract nodes that can be executed with applied dependencies on a Render Farm, based upon the way the
Network View has been built
```python
from dependency_wrangler import DependencyWrangler
import hou

# Create the Dependency Wrangler Connector
wrangler = DependencyWrangler(
    object_class=hou.Node,
    object_upstream_callback=hou.Node.inputs,
    object_downstream_callback=hou.Node.outputs,
    object_identifier_callback=hou.Node.name,
    object_type_callback=hou.Node.type,
    bypass_types=["Merge", "Switch"]
)
```

### The Foundry: NUKE
Nodes of a specific type within the same stream of a given node can be filtered out, manipulated and
even purged. In this example, the Dependency Wrangler will get all items connected to the tree that are not of type
Merge and Copy.
```python
from dependency_wrangler import DependencyWrangler
import nuke

# Create The Dependency Wrangler Connector
wrangler = DependencyWrangler(
    object_class=nuke.Node,
    object_upstream_callback=nuke.Node.dependencies,
    object_downstream_callback=nuke.Node.dependent,
    object_identifier_callback=nuke.Node.name,
    object_type_callback=nuke.Node.Class,
    bypass_types=["Merge2", "Copy"]
)

# Analyse the Dependency Tree from the selected node
wrangler.analyse(nuke.selectedNode())

# Obtain the filtered node list
node_list = wrangler.available_nodes
```