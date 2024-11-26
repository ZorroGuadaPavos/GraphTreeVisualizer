from typing import Optional

from pydantic import BaseModel


class TreeNode(BaseModel):
    id: str
    label: str
    children: Optional[list['TreeNode']] = []
