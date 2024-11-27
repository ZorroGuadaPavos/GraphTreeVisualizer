from neomodel import db
from src.tree.models import Node, Tree


def populate_database(json_data):
    tree = Tree().save()
    nodes = {}

    for item in json_data['data']:
        node = Node(name=item['name'], description=item['description']).save()
        nodes[item['name']] = node.uid
        db.cypher_query(
            """
            MATCH (n:Node)
            WHERE n.uid = $node_uid
            WITH n
            MATCH (g:Tree)
            WHERE g.uid = $tree_uid
            MERGE (n)-[:BELONGS_TO]->(g)
            """,
            {'tree_uid': tree.uid, 'node_uid': node.uid},
        )

    for item in json_data['data']:
        if item['parent']:
            parent_uid = nodes[item['parent']]
            child_uid = nodes[item['name']]
            db.cypher_query(
                """
                MATCH (parent:Node {uid: $parent_uid})
                WITH parent
                MATCH (child:Node {uid: $child_uid})
                MERGE (parent)-[:PARENT]->(child)
                """,
                {'parent_uid': parent_uid, 'child_uid': child_uid},
            )
    return tree, nodes
