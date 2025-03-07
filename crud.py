from sqlalchemy.orm import Session
from sqlalchemy import update
from typing import Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import models
import schemas


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(title=task.title, description=task.description, completed=task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return db_task
    return None


def update_task(db: Session, task_id: int, title: str = None, description: str = None, completed: bool = None):
    db_task = get_task(db, task_id)
    if db_task:
        if title is not None:
            db_task.title = title
        if description is not None:
            db_task.description = description
        if completed is not None:
            db_task.completed = completed
        db.commit()
        db.refresh(db_task)
        return db_task
    return None
