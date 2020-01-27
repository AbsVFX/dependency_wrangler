from item import DependencyItem

class DependencyWrangler(object):
    """
    The DependencyWrangler class analyzes a dependency tree, reconstructs the tree in an object-oriented way and allows
    for bypassing of unwanted or irrelevant objects in a simple way.
    """

    @property
    def object_metaclass(self):
        return self._object_metaclass

    @object_metaclass.setter
    def object_metaclass(self):
        pass

    @property
    def object_upstream_callback(self):
        return self._object_upstream_callback

    @object_upstream_callback.setter
    def object_upstream_callback(self):
        pass

    @property
    def object_downstream_callback(self):
        return self._object_downstream_callback

    @object_downstream_callback.setter
    def object_downstream_callback(self):
        pass

    @property
    def object_identifier_attribute(self):
        return self._object_identifier_attribute

    @object_identifier_attribute.setter
    def object_identifier_attribute(self):
        pass

    @property
    def object_type_attribute(self):
        return self._object_type_attribute

    @object_type_attribute.setter
    def object_type_attribute(self):
        pass
    
    @property
    def object_identifier_callback(self):
        return self._object_identifier_callback

    @object_identifier_callback.setter
    def object_identifier_callback(self):
        pass

    @property
    def object_type_callback(self):
        return self._object_type_callback

    @object_type_callback.setter
    def object_type_callback(self):
        pass

    @property
    def analysed_objects(self):
        return self._dependency_tree.keys()

    @property
    def available_objects(self):
        return [
            key for key,value in self._dependency_tree.items()
            if not value.bypass
        ]

    @property
    def items(self):
        return self._dependency_tree

    @items.setter
    def items(self):
        pass

    def __init__(self,
                 object_class=None,
                 object_upstream_callback=None,
                 object_downstream_callback=None,
                 object_identifier_callback=None,
                 object_type_callback=None,
                 object_type_attribute=None,
                 object_identifier_attribute=None,
                 bypass_types=None,
                 *args, **kwargs):
        """
        Initialize the DependencyWrangler class with the required attributes.
        The *object_class* will be used to hold the base class of the dependency objects that this class will be
        interacting with.
        Both *object_upstream_callback* and *object_downstream_callback* will be used to communicate with the object
        within the current object within the iteration that the tree analysis is at, and will be expected to
        return a list of objects in either direction.
        The *object_identifier_attribute* is a unique name given to each object within the dependency tree. This will
        be used within a key/value pair system to allow for identifying a pre-processed tree from any point within
        the tree.

        :param object_class: (object) The baseclass of all objects within the dependency tree
        :param object_upstream_callback: (callable) A function to call on an object to retrieve the upstream
        dependencies
        :param object_downstream_callback: (callable) A function to call on an object to retrieve downstream
        dependencies
        :param object_identifier_attribute: (object) The attribute on all objects that contains the unique id
        :param object_type_attribute: (object) The attribute on all objects that contains the type
        :param bypass_types: (list/str) List of strings defining types of objects to bypass when analysing the tree
        :param args: (tuple) additional arguments to pass to the *object* initialization function
        :param kwargs: (dict) additional key/value pairs to pass to the *object* initialization function
        """
        super(DependencyWrangler, self).__init__(*args, **kwargs)

        self._object_metaclass = object_class
        self._object_upstream_callback = object_upstream_callback
        self._object_downstream_callback = object_downstream_callback
        self._object_identifier_attribute = object_identifier_attribute
        self._object_type_attribute = object_type_attribute
        self._object_identifier_callback = object_identifier_callback
        self._object_type_callback = object_type_callback
        self._bypass_types = bypass_types or list()

        self._dependency_tree = dict()

    def validate(self):
        """
        Validate that the DependencyWrangler class has been initialized and populated correctly, by iterating through
        each required attribute for analysis and ensuring that they have a value that is not None set to them. If any
        attribute fails the validation, an *AttributeError* will be raised with the specific attribute that has an
        invalid value in the error.
        :return: (bool) True if validation passes
        """
        if not self.object_metaclass:
            raise AttributeError(
                "A metaclass hasn't been specified"
            )

        if not self.object_downstream_callback:
            raise AttributeError(
                "A callback for obtaining downstream dependencies has not been specified."
            )

        if not self.object_upstream_callback:
            raise AttributeError(
                "A callback for obtaining upstream dependencies has not been specified"
            )

        if not self.object_identifier_attribute:
            raise AttributeError(
                "The attribute name pointing to the unique identifier has not been specified"
            )

        if not self.object_type_attribute:
            raise AttributeError(
                "The attribute name pointing to the type has not been specified"
            )

        return True

    def _define_item(self, item_identifier, item_type, item):
        """
        Creates a DependencyItem object which contains both the upstream and downstream dependencies
        for this object within the iteration. It will also append the created object to the internal list of
        processed objects
        :param item_identifier: (object) unique name of the object in iteration
        :param item: (object) the actual object that the DependencyItem object will represent
        :return: (DependencyObject) the internal object representing the actual object
        """
        item_bypassed = (item_type in self._bypass_types)
        processed_item = DependencyItem(item_identifier, item_type, item, item_bypassed)
        self._dependency_tree[item_identifier] = processed_item
        return processed_item

    def analyse(self, item):
        """
        Analyse & constructs the dependency tree from a specified object. This function will use the callbacks defined
        this class to obtain the upstream and downstream dependencies against the actual object itself.
        :param item: (object) the object to analyse the tree from
        :return: (DependencyItem) returns a DependencyItem object that represents the item specified
        """
        # Run validation to ensure that this instance of the DependencyWrangler is populated correctly
        self.validate()
        # Extract the unique identifier & type from the specified item
        if self.object_identifier_callback:
            item_identifier = self.object_identifier_callback(item)
        else:
            item_identifier = getattr(item, self.object_identifier_attribute)
        if self.object_type_callback:
            item_type = self.object_type_callback(item)
        else:
            item_type = getattr(item, self.object_type_attribute)
        # Only process this object if it hasn't been processed already. This would be the case when working upwards
        # through a tree, and making our way back down to catch any lingering dependencies in a more complex dependency
        # tree
        if item_identifier not in self.analysed_objects:
            # Create an internal item that represents the real item that is currently within the iteration
            processed_item = self._define_item(item_identifier, item_type, item)
            # Loop through upstream dependencies and re-call this analyse function
            for dependency in self.object_upstream_callback(item):
                dependency_item = self.analyse(dependency)
                if dependency_item.type in self._bypass_types:
                    for sub_dependency in dependency_item.upstream_dependencies:
                        processed_item.append_upstream_dependency(sub_dependency)
                else:
                    processed_item.append_upstream_dependency(dependency_item)
            # Loop through downstream dependencies and re-call this analyse function
            for dependency in self.object_downstream_callback(item):
                dependency_item = self.analyse(dependency)
                if dependency_item.type in self._bypass_types:
                    for sub_dependency in dependency_item.upstream_dependencies:
                        processed_item.append_downstream_dependency(sub_dependency)
                else:
                    processed_item.append_downstream_dependency(dependency_item)
        # Return the item that has been created and or referenced in this iteration
        return self.items[item_identifier]