from typing import Optional

from pydantic import BaseModel


class TreePublic(BaseModel):
    id: str
    children: Optional[list['TreePublic']] = []


class NodePublic(BaseModel):
    id: str
    label: str
