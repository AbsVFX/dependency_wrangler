import pytest
from ..wrangler import DependencyWrangler


class SampleDependencyObject(object):
    def __init__(self, _id, _type="Basic"):
        self.id = _id
        self.type = _type
        self._upstream_dependencies = []
        self._downstream_dependencies = []

    def append_upstream_dependency(self, item):
        self._upstream_dependencies.append(item)

    def append_downstream_dependency(self, item):
        self._downstream_dependencies.append(item)

    def upstream_dependencies(self):
        return self._upstream_dependencies

    def downstream_dependencies(self):
        return self._downstream_dependencies

    def invalid_upstream_dependencies(self):
        pass

    def invalid_downstream_dependencies(self):
        pass

def construct_sample_tree_item():
    item_names = ["ItemA", "ItemB", "ItemC", "ItemD", "ItemE"]
    items = [
        SampleDependencyObject(item_name)
        for item_name in item_names
    ]

    for i in range(len(items)):
        if i != 0:
            items[i].append_downstream_dependency(items[i-1])
        if i < len(items)-1:
            items[i].append_upstream_dependency(items[i+1])

    return (item_names, items[0])

def construct_sample_multi_type_tree_item():
    item_names = ["MultiTypeItemA",
                  "MultiTypeItemB",
                  "MultiTypeItemC",
                  "MultiTypeItemD",
                  "MultiTypeItemE"]
    items = [
        SampleDependencyObject(
            _id=item_name, _type=item_name
        )
        for item_name in item_names
    ]

    for i in range(len(items)):
        if i != 0:
            items[i].append_downstream_dependency(items[i-1])
        if i < len(items)-1:
            items[i].append_upstream_dependency(items[i+1])

    return (item_names, items[0])

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

        return wrangler

    def test_dependency_wrangler_class_creation(self):
        """
        Ensure that there are no errors when initializing the DependencyWrangler class, and validate that the
        attributes are initialized correctly
        """

        object_class = SampleDependencyObject
        object_upstream_callback = SampleDependencyObject.upstream_dependencies
        object_downstream_callback = SampleDependencyObject.downstream_dependencies
        object_identifier_attribute = "id"
        object_type_attribute = "type"

        wrangler = DependencyWrangler(
            object_class=object_class,
            object_upstream_callback=object_upstream_callback,
            object_downstream_callback=object_downstream_callback,
            object_identifier_attribute=object_identifier_attribute,
            object_type_attribute=object_type_attribute
        )

        assert wrangler._object_metaclass is object_class
        assert wrangler._object_upstream_callback is object_upstream_callback
        assert wrangler._object_downstream_callback is object_downstream_callback
        assert wrangler._object_identifier_attribute == object_identifier_attribute
        assert wrangler.object_metaclass is object_class
        assert wrangler.object_upstream_callback is object_upstream_callback
        assert wrangler.object_downstream_callback is object_downstream_callback
        assert wrangler.object_identifier_attribute == object_identifier_attribute
        return wrangler

    def test_dependency_wrangler_bypassed_class_creation(self, bypass_types=None):
        """
        Ensure that there are no errors when initializing the DependencyWrangler class, and validate that the
        attributes are initialized correctly
        """

        object_class = SampleDependencyObject
        object_upstream_callback = SampleDependencyObject.upstream_dependencies
        object_downstream_callback = SampleDependencyObject.downstream_dependencies
        object_identifier_attribute = "id"
        object_type_attribute = "type"

        wrangler = DependencyWrangler(
            object_class=object_class,
            object_upstream_callback=object_upstream_callback,
            object_downstream_callback=object_downstream_callback,
            object_identifier_attribute=object_identifier_attribute,
            object_type_attribute=object_type_attribute,
            bypass_types=bypass_types or list()
        )

        assert wrangler._object_metaclass is object_class
        assert wrangler._object_upstream_callback is object_upstream_callback
        assert wrangler._object_downstream_callback is object_downstream_callback
        assert wrangler._object_identifier_attribute == object_identifier_attribute
        assert wrangler.object_metaclass is object_class
        assert wrangler.object_upstream_callback is object_upstream_callback
        assert wrangler.object_downstream_callback is object_downstream_callback
        assert wrangler.object_identifier_attribute == object_identifier_attribute
        return wrangler

    def test_dependency_wrangler_required_class_creation(self, bypass_types=None):
        """
        Ensure that there are no errors when initializing the DependencyWrangler class, and validate that the
        attributes are initialized correctly
        """

        object_class = SampleDependencyObject
        object_upstream_callback = SampleDependencyObject.upstream_dependencies
        object_downstream_callback = SampleDependencyObject.downstream_dependencies
        object_identifier_attribute = "id"
        object_type_attribute = "type"

        wrangler = DependencyWrangler(
            object_class=object_class,
            object_upstream_callback=object_upstream_callback,
            object_downstream_callback=object_downstream_callback,
            object_identifier_attribute=object_identifier_attribute,
            object_type_attribute=object_type_attribute,
            required_types=bypass_types or list()
        )

        assert wrangler._object_metaclass is object_class
        assert wrangler._object_upstream_callback is object_upstream_callback
        assert wrangler._object_downstream_callback is object_downstream_callback
        assert wrangler._object_identifier_attribute == object_identifier_attribute
        assert wrangler.object_metaclass is object_class
        assert wrangler.object_upstream_callback is object_upstream_callback
        assert wrangler.object_downstream_callback is object_downstream_callback
        assert wrangler.object_identifier_attribute == object_identifier_attribute
        return wrangler

    def test_overspecified_dependency_wrangler_class_creation(self):
        object_class = SampleDependencyObject
        object_upstream_callback = SampleDependencyObject.upstream_dependencies
        object_downstream_callback = SampleDependencyObject.downstream_dependencies
        object_identifier_attribute = "id"
        object_type_attribute = "type"

        with pytest.raises(Exception, match=".*specified"):
            DependencyWrangler(
                object_class=object_class,
                object_upstream_callback=object_upstream_callback,
                object_downstream_callback=object_downstream_callback,
                object_identifier_attribute=object_identifier_attribute,
                object_type_attribute=object_type_attribute,
                bypass_types=[0],
                required_types=[0]
            )

    def test_invalid_dependency_wrangler_class_validation(self):
        """
        Verify that an insufficient amount of data to the DependencyWrangler class will break the validation
        function
        """
        object_class = SampleDependencyObject
        object_upstream_callback = SampleDependencyObject.upstream_dependencies
        object_downstream_callback = SampleDependencyObject.downstream_dependencies

        wranglers = [
            DependencyWrangler(),
            DependencyWrangler(object_class=object_class),
            DependencyWrangler(
                object_class=object_class,
                object_upstream_callback=object_upstream_callback
            ),
            DependencyWrangler(
                object_class=object_class,
                object_upstream_callback=object_upstream_callback,
                object_downstream_callback=object_downstream_callback
            )
        ]

        for wrangler in wranglers:
            with pytest.raises(AttributeError, match=".*specified"):
                wrangler.validate()

    def test_dependency_wrangler_class_validation(self):
        """
        Ensure that validation of the DependencyWrangler will pass with all required information
        """
        wrangler = self.test_dependency_wrangler_class_creation()
        assert wrangler.validate() is True

    def test_dependency_wrangler_analysis(self):
        """
        Ensure that the analysis of a simple dependency tree is working and that data has been translated
        accurately and successfully
        """
        wrangler = self.test_dependency_wrangler_class_creation()
        item_names, item = construct_sample_tree_item()
        wrangler.analyse(item)

        for item_name in item_names:
            assert item_name in wrangler.analysed_objects

        for i in range(len(item_names)):
            item_name = item_names[i]
            if i != 0:
                assert item_names[i-1] in [x.id for x in wrangler.items[item_name].downstream_dependencies]
            if i < len(item_names) - 1:
                assert item_names[i+1] in [x.id for x in wrangler.items[item_name].upstream_dependencies]

    def test_bypassed_dependency_wrangler_analysis(self):
        """
        Ensure that the analysis of a simple dependency tree is working and that data has been translated
        accurately and successfully, including when bypassing a specific item type
        """
        item_names, item = construct_sample_multi_type_tree_item()
        bypass_item_type = item_names[2]
        wrangler = self.test_dependency_wrangler_bypassed_class_creation(bypass_item_type)
        wrangler.analyse(item)

        for item_name in item_names:
            assert item_name in wrangler.analysed_objects
            processed_item = wrangler.items[item_name]
            assert bypass_item_type not in processed_item.upstream_dependencies
            assert bypass_item_type not in processed_item.downstream_dependencies

        for i in range(len(item_names)):
            item_name = item_names[i]
            if i != 0:
                if item_names[i-1] != bypass_item_type:
                    assert item_names[i-1] in [x.id for x in wrangler.items[item_name].downstream_dependencies]
                else:
                    assert item_names[i-1] not in [x.id for x in wrangler.items[item_name].downstream_dependencies]
            if i < len(item_names) - 1:
                if item_names[i+1] != bypass_item_type:
                    assert item_names[i+1] in [x.id for x in wrangler.items[item_name].upstream_dependencies]
                else:
                    assert item_names[i+1] not in [x.id for x in wrangler.items[item_name].upstream_dependencies]

    def test_required_dependency_wrangler_analysis(self):
        """
        Ensure that the analysis of a simple dependency tree is working and that data has been translated
        accurately and successfully, including when bypassing a specific item type
        """
        item_names, item = construct_sample_multi_type_tree_item()
        bypass_item_type = [item_names[1], item_names[3]]
        wrangler = self.test_dependency_wrangler_required_class_creation(bypass_item_type)
        wrangler.analyse(item)

        for item_name in item_names:
            assert item_name in wrangler.analysed_objects
            processed_item = wrangler.items[item_name]
            assert bypass_item_type not in processed_item.upstream_dependencies
            assert bypass_item_type not in processed_item.downstream_dependencies

        assert wrangler.available_objects == bypass_item_type