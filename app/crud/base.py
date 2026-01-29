from typing import Type, List
from sqlalchemy.orm import Session
from pydantic import BaseModel

class CRUDBase:
    def __init__(self, model: Type):
        self.model = model

    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session) -> List:
        return db.query(self.model).all()

    def create(self, db: Session, obj_in: BaseModel):
        obj = self.model(**obj_in.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj, obj_in: BaseModel):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        obj = self.get(db, id)
        db.delete(obj)
        db.commit()
        return obj