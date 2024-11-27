import json
import logging
import os

from neomodel import config, db

from src.core.config import settings
from src.tree.models import Node, Tree

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('populate_db')

config.DATABASE_URL = settings.DATABASE_URL


def clear_database():
    """
    Clear all nodes and relationships in the database.
    """
    db.cypher_query('MATCH (n) DETACH DELETE n')


def load_json(json_path):
    with open(json_path) as f:
        return json.load(f)


def populate_database(json_data):
    tree = Tree().save()
    logger.info(f'Created Graph with uid: {tree.uid}')
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


def get_json_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.json')]


def process_json_files():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    json_files = get_json_files(data_dir)
    for json_file in json_files:
        json_path = os.path.join(data_dir, json_file)
        json_data = load_json(json_path)
        populate_database(json_data)


if __name__ == '__main__':
    logger.info('Clearing database...')
    clear_database()
    process_json_files()
    logger.info('Database populated.')
