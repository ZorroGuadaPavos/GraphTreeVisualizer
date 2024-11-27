from neomodel import RelationshipFrom, RelationshipTo, StringProperty, StructuredNode, UniqueIdProperty


class Node(StructuredNode):
    uid = UniqueIdProperty(unique=True)
    name = StringProperty(required=True)
    description = StringProperty()
    parent = RelationshipFrom('Node', 'PARENT')
    children = RelationshipTo('Node', 'PARENT')
    tree = RelationshipTo('Tree', 'BELONGS_TO')


class Tree(StructuredNode):
    uid = UniqueIdProperty(unique=True)
    nodes = RelationshipFrom('Node', 'BELONGS_TO')
