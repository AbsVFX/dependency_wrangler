class DependencyItem(object):
    """
    The DependencyItem is a proxy item that represents a real Python object
    """
    @property
    def upstream_dependencies(self):
        return self._upstream_dependencies

    @property
    def downstream_dependencies(self):
        return self._downstream_dependencies

    @upstream_dependencies.setter
    def upstream_dependencies(self):
        pass

    @downstream_dependencies.setter
    def downstream_dependencies(self):
        pass

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'item': self.object,
            'bypass': self.bypass
        }

    def __init__(self, id, type, item, bypass=False):
        """
        Initialize the DependencyItem object with the unique identifier and the item itself, and
        declares the initial upstream & downstream dependencies private lists
        :param id: (object) the unique identifier for this item
        :param item: (object) the python object that this proxy item will represent
        """
        super(DependencyItem, self).__init__()

        self.id = id
        self.type = type
        self.object = item
        self.bypass = bypass
        self._upstream_dependencies = list()
        self._downstream_dependencies = list()

    def append_upstream_dependency(self, item):
        """
        Appends a DependencyItem to the private *_upstream_dependencies* list
        :param item: (object) the DependencyItem to append
        """
        self._upstream_dependencies.append(item)

    def append_downstream_dependency(self, item):
        """
        Appends a DependencyItem to the private *_downstream_dependencies* list
        :param item: (object) the DependencyItem to append
        """
        self._downstream_dependencies.append(item)