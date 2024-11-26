import uuid
from typing import Optional

from neomodel import db

from src.tree.models import Node
from src.tree.schemas import TreeNode


def get_root_node(tree_id: uuid.UUID) -> Optional[Node]:
    query = """
    MATCH (n:Node)-[:BELONGS_TO]->(t:Tree {uid: $tree_id})
    WHERE NOT (n)<-[:PARENT]-()
    RETURN n;
    """
    results, _ = db.cypher_query(query, {'tree_id': tree_id})
    return Node.inflate(results[0][0]) if results else None


def build_tree(node: Node) -> TreeNode:
    return TreeNode(id=node.name, label=node.description, children=[build_tree(child) for child in node.children])


def get_tree_hierarchy(tree_id: str) -> TreeNode:
    root = get_root_node(tree_id)
    if not root:
        return None
    return build_tree(root)
