from datetime import datetime
from extensions import db
from models.common.base import BaseModel

class Order(BaseModel):
    """Order model for storing order information."""
    
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='pending')
    total_amount = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.Text, nullable=True)
    billing_address = db.Column(db.Text, nullable=True)
    payment_status = db.Column(db.String(20), nullable=False, default='pending')
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    user = db.relationship('User', lazy=True)
    
    def __repr__(self):
        return f'<Order {self.id}>'
    
    def __init__(self, user_id, total_amount, shipping_address=None, billing_address=None):
        self.user_id = user_id
        self.total_amount = total_amount
        self.shipping_address = shipping_address
        self.billing_address = billing_address or shipping_address
    
    def to_dict(self):
        """Convert order to dictionary."""
        return {
            'id': self.id,
            'order_date': self.order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'total_amount': self.total_amount,
            'shipping_address': self.shipping_address,
            'billing_address': self.billing_address,
            'payment_status': self.payment_status,
            'items': [item.to_dict() for item in self.items]
        }
    
    @classmethod
    def create_order(cls, user_id, total_amount, shipping_address=None, billing_address=None):
        """Create a new order."""
        order = cls(
            user_id=user_id,
            total_amount=total_amount,
            shipping_address=shipping_address,
            billing_address=billing_address
        )
        return order.save()
    
    def update_status(self, new_status):
        """Update order status."""
        self.status = new_status
        return self.save()
    
    def update_payment_status(self, new_status):
        """Update payment status."""
        self.payment_status = new_status
        return self.save()
    
    def add_item(self, wine_id, wine_name, quantity, price_per_unit):
        """Add an item to the order."""
        from models.order_item import OrderItem
        item = OrderItem(
            order_id=self.id,
            wine_id=wine_id,
            wine_name=wine_name,
            quantity=quantity,
            price_per_unit=price_per_unit
        )
        item.save()
        self.calculate_total()
        return item
    
    def calculate_total(self):
        """Calculate total amount from items."""
        total = sum(item.subtotal for item in self.items)
        self.total_amount = total
        return self.save() 