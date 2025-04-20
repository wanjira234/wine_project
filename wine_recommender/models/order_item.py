from extensions import db
from models.common.base import BaseModel

class OrderItem(BaseModel):
    """OrderItem model for storing individual items in an order."""
    
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    wine_id = db.Column(db.String(50), nullable=False)  # Changed to String to store dataset wine ID
    wine_name = db.Column(db.String(200), nullable=False)  # Store wine name directly
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'

    def __init__(self, order_id, wine_id, wine_name, quantity, price_per_unit):
        self.order_id = order_id
        self.wine_id = wine_id
        self.wine_name = wine_name
        self.quantity = quantity
        self.price = price_per_unit
        self.calculate_subtotal()
    
    def to_dict(self):
        """Convert order item to dictionary."""
        return {
            'id': self.id,
            'wine_id': self.wine_id,
            'wine_name': self.wine_name,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.subtotal
        }
    
    def calculate_subtotal(self):
        """Calculate subtotal based on quantity and price."""
        self.subtotal = self.quantity * self.price
        return self.subtotal
    
    def update_quantity(self, new_quantity):
        """Update item quantity and recalculate subtotal."""
        self.quantity = new_quantity
        self.calculate_subtotal()
        return self.save()
    
    @classmethod
    def create_order_item(cls, order_id, wine_id, wine_name, quantity, price_per_unit):
        """Create a new order item."""
        item = cls(
            order_id=order_id,
            wine_id=wine_id,
            wine_name=wine_name,
            quantity=quantity,
            price=price_per_unit
        )
        return item.save() 