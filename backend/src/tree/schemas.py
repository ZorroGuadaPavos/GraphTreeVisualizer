from typing import Optional

from pydantic import BaseModel


class TreePublic(BaseModel):
    name: str
    id: str
    children: Optional[list['TreePublic']] = []


class NodePublic(BaseModel):
    name: str
    id: str
    label: str
