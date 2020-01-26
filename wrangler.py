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

    def __init__(self,
                 object_class=None,
                 object_upstream_callback=None,
                 object_downstream_callback=None,
                 object_identifier_attribute=None,
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
        :param args: (tuple) additional arguments to pass to the *object* initialization function
        :param kwargs: (dict) additional key/value pairs to pass to the *object* initialization function
        """
        super(DependencyWrangler, self).__init__(*args, **kwargs)

        self._object_metaclass = object_class
        self._object_upstream_callback = object_upstream_callback
        self._object_downstream_callback = object_downstream_callback
        self._object_identifier_attribute = object_identifier_attribute

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

        return True
