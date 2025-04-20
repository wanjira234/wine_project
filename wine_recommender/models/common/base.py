from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from extensions import db

class BaseModel(db.Model):
    """Base model class that adds common functionality to all models."""
    
    __abstract__ = True  # Tells SQLAlchemy not to create a table for this model
    
    def save(self):
        """Save the model instance to the database."""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Delete the model instance from the database."""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_by_id(cls, id):
        """Get a model instance by ID."""
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls):
        """Get all instances of the model."""
        return cls.query.all()

class BaseModel(db.Model):
    """Base model class that includes common fields and methods."""
    
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def save(self):
        """Save the model instance to the database."""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Delete the model instance from the database."""
        db.session.delete(self)
        db.session.commit()

    def soft_delete(self):
        """Soft delete the model instance by setting is_active to False."""
        self.is_active = False
        self.save()

    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            'id': getattr(self, 'id', None),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        } 