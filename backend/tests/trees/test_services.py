from src.tree.services import get_all_tree_ids, get_node, get_root_node, get_tree_hierarchy


def test_get_root_node(sample_tree):
    tree, nodes = sample_tree
    root = get_root_node(tree.uid)
    assert root is not None
    assert root.uid == nodes['A']
    assert root.name == 'A'


def test_get_node(sample_tree):
    tree, nodes = sample_tree
    for child_name in ['B', 'C', 'D']:
        node = get_node(tree.uid, nodes[child_name])
        assert node is not None
        assert node.uid == nodes[child_name]
        assert node.name == child_name
        parent_node = node.parent.single()
        assert parent_node.uid == nodes['A']

    # Test B's children
    for child_name in ['B-1', 'B-2', 'B-3']:
        node = get_node(tree.uid, nodes[child_name])
        assert node is not None
        assert node.uid == nodes[child_name]
        assert node.name == child_name
        parent_node = node.parent.single()
        assert parent_node.uid == nodes['B']


def test_get_all_tree_ids(sample_tree):
    tree, nodes = sample_tree
    tree_ids = get_all_tree_ids()
    assert tree.uid in tree_ids


def test_get_tree_hierarchy(sample_tree):
    tree, nodes = sample_tree
    hierarchy = get_tree_hierarchy(tree.uid)
    assert hierarchy is not None
    assert hierarchy.id == nodes['A']
    assert hierarchy.name == 'A'
    assert len(hierarchy.children) == 3
    child_names = ['B', 'C', 'D']
    for child in hierarchy.children:
        assert child.id in [nodes[name] for name in child_names]
        assert child.name in child_names
