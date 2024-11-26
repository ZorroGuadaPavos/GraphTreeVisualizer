from neomodel import RelationshipFrom, RelationshipTo, StringProperty, StructuredNode, UniqueIdProperty


class Node(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    parent = RelationshipFrom('Node', 'PARENT')
    children = RelationshipTo('Node', 'PARENT')
    tree = RelationshipTo('Tree', 'BELONGS_TO')


class Tree(StructuredNode):
    uid = UniqueIdProperty(unique=True)
