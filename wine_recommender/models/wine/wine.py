from extensions import db
from models.common.base import BaseModel
from models.common.enums import WineType, WineRegion

class Wine(BaseModel):
    """Wine model for storing wine information."""
    
    __tablename__ = 'wines'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Enum(WineType), nullable=False)
    region = db.Column(db.Enum(WineRegion), nullable=False)
    year = db.Column(db.Integer)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    
    def __init__(self, name, type, region, price, year=None, description=None, stock=0, image_url=None):
        self.name = name
        self.type = type
        self.region = region
        self.price = price
        self.year = year
        self.description = description
        self.stock = stock
        self.image_url = image_url
    
    def to_dict(self):
        """Convert wine to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type.value,
            'region': self.region.value,
            'year': self.year,
            'price': self.price,
            'description': self.description,
            'stock': self.stock,
            'image_url': self.image_url
        }
    
    @classmethod
    def create_wine(cls, name, type, region, price, year=None, description=None, stock=0, image_url=None):
        """Create a new wine."""
        wine = cls(
            name=name,
            type=type,
            region=region,
            price=price,
            year=year,
            description=description,
            stock=stock,
            image_url=image_url
        )
        wine.save()
        return wine
    
    def update_stock(self, quantity):
        """Update wine stock."""
        self.stock = quantity
        return self.save()
    
    def __repr__(self):
        return f'<Wine {self.name}>' 