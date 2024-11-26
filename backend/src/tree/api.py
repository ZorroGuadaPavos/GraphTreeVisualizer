import uuid
from typing import Dict

from fastapi import APIRouter, HTTPException

from src.tree import services
from src.tree.schemas import TreeNode

router = APIRouter()


@router.get('/{tree_id}', response_model=TreeNode)
def read_tree(tree_id: uuid.UUID) -> Dict:
    tree_data = services.get_tree_hierarchy(str(tree_id))
    if not tree_data:
        raise HTTPException(status_code=404, detail='tree not found')
    return tree_data
