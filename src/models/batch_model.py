from src.init_db import db

class Batch(db.Model):
    __tablename__ = "batches"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    batch_id = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    piglet_count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.Date, nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.Date, nullable=True, default=db.func.now(), onupdate=db.func.now()
    )

    def __init__(self, batch_id, status, piglet_count):
        self.batch_id = batch_id
        self.status = status
        self.piglet_count = piglet_count

    def __repr__(self):
        return f"<Batch {self.batch_id}, {self.status}, {self.piglet_count}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'batch_id': self.batch_id,
            'status': self.status,
            'piglet_count': self.piglet_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
