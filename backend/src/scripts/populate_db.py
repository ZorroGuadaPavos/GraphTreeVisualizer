import logging
import uuid

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


def clear_database():
    """
    Clear all nodes and relationships in the database.
    """
    db.cypher_query('MATCH (n) DETACH DELETE n')


def populate_database():
    # clear_database()  # Removed redundant call
    tree = Tree(uid=str(uuid.uuid4())).save()
    logger.info(f'Created Graph with uid: {tree.uid}')
    # ...existing code...
    nodes = {}

    for item in JSON_DATA['data']:
        node = Node(name=item['name'], description=item['description']).save()
        nodes[item['name']] = node
        db.cypher_query(
            """
            MATCH (n:Node)
            WHERE ID(n) = $node_id
            WITH n
            MATCH (g:Tree)
            WHERE ID(g) = $tree_id
            MERGE (n)-[:BELONGS_TO]->(g)
            """,
            {'tree_id': tree.id, 'node_id': node.id},
        )

    for item in JSON_DATA['data']:
        if item['parent']:
            parent_name = item['parent']
            child_name = item['name']
            db.cypher_query(
                """
                MATCH (parent:Node {name: $parent_name})
                WITH parent
                MATCH (child:Node {name: $child_name})
                MERGE (parent)-[:PARENT]->(child)
                """,
                {'parent_name': parent_name, 'child_name': child_name},
            )


if __name__ == '__main__':
    logger.info('Clearing database...')
    clear_database()
    populate_database()
    logger.info('Database populated.')
