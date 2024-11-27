from typing import List, Optional

from neomodel import db

from src.tree.models import Node
from src.tree.schemas import TreePublic


def get_root_node(tree_id: str) -> Optional[Node]:
    query = """
    MATCH (n:Node)-[:BELONGS_TO]->(t:Tree {uid: $tree_id})
    WHERE NOT (n)<-[:PARENT]-()
    RETURN n;
    """
    results, _ = db.cypher_query(query, {'tree_id': tree_id})
    return Node.inflate(results[0][0]) if results else None


def get_node(tree_id: str, node_id: str) -> Optional[Node]:
    query = """
    MATCH (n:Node {name: $node_id})-[:BELONGS_TO]->(t:Tree {uid: $tree_id})
    RETURN n;
    """
    results, _ = db.cypher_query(query, {'tree_id': tree_id, 'node_id': node_id})
    return Node.inflate(results[0][0]) if results else None


def get_all_tree_ids() -> List[str]:
    query = """
    MATCH (t:Tree)
    RETURN t.uid as uid
    """
    results, _ = db.cypher_query(query)
    return [record[0] for record in results]


def build_tree(node: Node) -> TreePublic:
    return TreePublic(id=node.name, children=[build_tree(child) for child in node.children])


def get_tree_hierarchy(tree_id: str) -> TreePublic:
    root = get_root_node(tree_id)
    if not root:
        return None
    return build_tree(root)
