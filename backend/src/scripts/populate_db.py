import logging

from neomodel import config, db

from src.core.config import settings
from src.tree.models import Node, Tree

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('populate_db')

config.DATABASE_URL = settings.DATABASE_URL

JSON_DATA = {
    'data': [
        {'name': 'A', 'description': 'This is a description of A', 'parent': ''},
        {'name': 'B', 'description': 'This is a description of B', 'parent': 'A'},
        {'name': 'C', 'description': 'This is a description of C', 'parent': 'A'},
        {'name': 'D', 'description': 'This is a description of D', 'parent': 'A'},
        {'name': 'B-1', 'description': 'This is a description of B-1', 'parent': 'B'},
        {'name': 'B-2', 'description': 'This is a description of B-2', 'parent': 'B'},
        {'name': 'B-3', 'description': 'This is a description of B-3', 'parent': 'B'},
    ]
}

JSON_DATA = {
    'data': [
        {'name': 'A', 'description': 'This is a description of A', 'parent': ''},
        {'name': 'B', 'description': 'This is a description of B', 'parent': 'A'},
        {'name': 'C', 'description': 'This is a description of C', 'parent': 'A'},
        {'name': 'D', 'description': 'This is a description of D', 'parent': 'A'},
        {'name': 'B-1', 'description': 'This is a description of B-1', 'parent': 'B'},
        {'name': 'B-2', 'description': 'This is a description of B-2', 'parent': 'B'},
        {'name': 'B-3', 'description': 'This is a description of B-3', 'parent': 'B'},
        {'name': 'B-1-1', 'description': 'This is a description of B-1-1', 'parent': 'B-1'},
        {'name': 'B-1-2', 'description': 'This is a description of B-1-2', 'parent': 'B-1'},
        {'name': 'B-2-1', 'description': 'This is a description of B-2-1', 'parent': 'B-2'},
        {'name': 'B-2-1-1', 'description': 'This is a description of B-2-1-1', 'parent': 'B-2-1'},
        {'name': 'B-3-1', 'description': 'This is a description of B-3-1', 'parent': 'B-3'},
        {'name': 'B-3-1-1', 'description': 'This is a description of B-3-1-1', 'parent': 'B-3-1'},
        {'name': 'B-3-1-2', 'description': 'This is a description of B-3-1-2', 'parent': 'B-3-1'},
        {'name': 'C-1', 'description': 'This is a description of C-1', 'parent': 'C'},
        {'name': 'C-1-1', 'description': 'This is a description of C-1-1', 'parent': 'C-1'},
        {'name': 'D-1', 'description': 'This is a description of D-1', 'parent': 'D'},
        {'name': 'D-1-1', 'description': 'This is a description of D-1-1', 'parent': 'D-1'},
        {'name': 'D-1-2', 'description': 'This is a description of D-1-2', 'parent': 'D-1'},
        {'name': 'E', 'description': 'This is a description of E', 'parent': 'A'},
        {'name': 'E-1', 'description': 'This is a description of E-1', 'parent': 'E'},
        {'name': 'E-1-1', 'description': 'This is a description of E-1-1', 'parent': 'E-1'},
        {'name': 'E-1-1-1', 'description': 'This is a description of E-1-1-1', 'parent': 'E-1-1'},
        {'name': 'E-2', 'description': 'This is a description of E-2', 'parent': 'E'},
    ]
}


def clear_database():
    """
    Clear all nodes and relationships in the database.
    """
    db.cypher_query('MATCH (n) DETACH DELETE n')


def populate_database():
    tree = Tree().save()
    logger.info(f'Created Graph with uid: {tree.uid}')
    nodes = {}

    for item in JSON_DATA['data']:
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

    for item in JSON_DATA['data']:
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


if __name__ == '__main__':
    logger.info('Clearing database...')
    # clear_database()
    populate_database()
    logger.info('Database populated.')
