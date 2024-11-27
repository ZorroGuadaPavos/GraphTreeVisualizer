from typing import Dict, List

from fastapi import APIRouter, HTTPException

from src.tree import services
from src.tree.schemas import NodePublic, TreePublic

router = APIRouter()


@router.get('/', response_model=List[str])
def get_all_tree_ids() -> List[str]:
    tree_ids = services.get_all_tree_ids()
    return tree_ids


@router.get('/{tree_id}', response_model=TreePublic)
def read_tree(tree_id: str) -> Dict:
    tree_data = services.get_tree_hierarchy(str(tree_id))
    if not tree_data:
        raise HTTPException(status_code=404, detail='tree not found')
    return tree_data


@router.get('/{tree_id}/nodes/{node_id}', response_model=NodePublic)
def read_node(tree_id: str, node_id: str) -> Dict:
    node = services.get_node(str(tree_id), node_id)
    if not node:
        raise HTTPException(status_code=404, detail='Node not found')
    return NodePublic(id=node.uid, name=node.name, label=node.description)
