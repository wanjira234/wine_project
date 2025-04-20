"""
Models package for the wine recommender application.
This package contains all database models used in the application.
"""

from models.common.base import BaseModel
from models.user.user import User
from models.order import Order
from models.order_item import OrderItem
from models.wine.wine import Wine

__all__ = [
    'BaseModel',
    'User',
    'Order',
    'OrderItem',
    'Wine'
]

# This file makes the models directory a Python package
