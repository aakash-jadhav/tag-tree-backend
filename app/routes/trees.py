from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TreeRecord
from app.schemas import Tag, TreeItemResponse, TreePayload

router = APIRouter(prefix="/trees", tags=["trees"])


def _serialize_row(row: TreeRecord) -> TreeItemResponse:
    tree = Tag.model_validate(row.data)
    return TreeItemResponse(id=row.id, tree=tree)


@router.post("", response_model=TreeItemResponse, status_code=201)
def create_tree(payload: TreePayload, db: Session = Depends(get_db)):
    record = TreeRecord(data=payload.tree.model_dump(mode="json"))
    db.add(record)
    db.commit()
    db.refresh(record)
    return _serialize_row(record)


@router.get("", response_model=list[TreeItemResponse])
def list_trees(db: Session = Depends(get_db)):
    rows = db.query(TreeRecord).order_by(TreeRecord.created_at.asc()).all()
    return [_serialize_row(r) for r in rows]


@router.put("/{tree_id}", response_model=TreeItemResponse)
def update_tree(tree_id: UUID, payload: TreePayload, db: Session = Depends(get_db)):
    record = db.get(TreeRecord, tree_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Tree not found")
    record.data = payload.tree.model_dump(mode="json")
    record.updated_at = datetime.now(timezone.utc)
    db.add(record)
    db.commit()
    db.refresh(record)
    return _serialize_row(record)
