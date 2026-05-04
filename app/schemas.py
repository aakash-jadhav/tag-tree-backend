from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class Tag(BaseModel):
    """Recursive tag: exactly one of `data` (leaf) or `children` (branch)."""

    name: str = Field(..., min_length=1)
    data: str | None = None
    children: list[Tag] | None = None

    @model_validator(mode="before")
    @classmethod
    def normalize_dict(cls, data: Any) -> Any:
        if isinstance(data, dict):
            out = dict(data)
            if out.get("children") is None and "children" in out:
                del out["children"]
            if out.get("data") is None and "data" in out:
                del out["data"]
            return out
        return data

    @model_validator(mode="after")
    def validate_leaf_or_branch(self) -> Tag:
        has_data = self.data is not None
        has_children = self.children is not None

        if has_data and has_children:
            raise ValueError("Tag cannot have both `data` and `children`")
        if not has_data and not has_children:
            raise ValueError("Tag must have either `data` or `children`")
        return self


class TreePayload(BaseModel):
    tree: Tag


class TreeItemResponse(BaseModel):
    id: UUID
    tree: Tag

    model_config = {"from_attributes": False}
