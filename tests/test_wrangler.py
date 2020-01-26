from ..wrangler import DependencyWrangler


class SampleDependencyObject(object):
    def __init__(self, id):
        self.id = id

    def upstream_dependencies(self):
        pass

    def downstream_dependencies(self):
        pass


class TestDependencyWrangler:
    def test_empty_dependency_wrangler_class_creation(self):
        """
        Ensure that there are no errors when initializing the DependencyWrangler class, and validate that the
        attributes are initialized correctly
        """
        wrangler = DependencyWrangler()

        assert wrangler._object_metaclass is None
        assert wrangler._object_upstream_callback is None
        assert wrangler._object_downstream_callback is None
        assert wrangler._object_identifier_attribute is None
        assert wrangler.object_metaclass is None
        assert wrangler.object_upstream_callback is None
        assert wrangler.object_downstream_callback is None
        assert wrangler.object_identifier_attribute is None

    def test_dependency_wrangler_class_creation(self):
        """
        Ensure that there are no errors when initializing the DependencyWrangler class, and validate that the
        attributes are initialized correctly
        """

        object_class = SampleDependencyObject
        object_upstream_callback = SampleDependencyObject.upstream_dependencies
        object_downstream_callback = SampleDependencyObject.downstream_dependencies
        object_identifier_attribute = "id"

        wrangler = DependencyWrangler(
            object_class=object_class,
            object_upstream_callback=object_upstream_callback,
            object_downstream_callback=object_downstream_callback,
            object_identifier_attribute=object_identifier_attribute
        )

        assert wrangler._object_metaclass is object_class
        assert wrangler._object_upstream_callback is object_upstream_callback
        assert wrangler._object_downstream_callback is object_downstream_callback
        assert wrangler._object_identifier_attribute == object_identifier_attribute
        assert wrangler.object_metaclass is object_class
        assert wrangler.object_upstream_callback is object_upstream_callback
        assert wrangler.object_downstream_callback is object_downstream_callback
        assert wrangler.object_identifier_attribute == object_identifier_attribute
