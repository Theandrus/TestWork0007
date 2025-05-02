from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .. import schemas, models, auth
from ..database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.TaskOut)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
) -> models.Task:
    db_task = models.Task(**task.dict(), owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[schemas.TaskOut])
def read_tasks(
    status: Optional[str] = Query(None),
    priority: Optional[int] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
) -> List[models.Task]:
    query = db.query(models.Task).filter(models.Task.owner_id == current_user.id)
    if status:
        query = query.filter(models.Task.status == status)
    if priority is not None:
        query = query.filter(models.Task.priority == priority)
    if date_from:
        query = query.filter(models.Task.created_at >= date_from)
    if date_to:
        query = query.filter(models.Task.created_at <= date_to)
    return query.all()

@router.get("/search", response_model=List[schemas.TaskOut])
def search_tasks(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
) -> List[models.Task]:
    return (
        db.query(models.Task)
        .filter(models.Task.owner_id == current_user.id)
        .filter(
            (models.Task.title.ilike(f"%{q}%")) |
            (models.Task.description.ilike(f"%{q}%"))
        )
        .all()
    )

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
) -> models.Task:
    db_task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.owner_id == current_user.id)
        .first()
    )
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    for var, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, var, value)
    db.commit()
    db.refresh(db_task)
    return db_task
