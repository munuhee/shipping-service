"""
Module representing shipping-related SQLAlchemy models and an enumeration.

Classes:
- ShippingStatus: Enumeration of shipping statuses.
- ShippingOrder: Represents a shipping order.
- ShippingCarrier: Represents a shipping carrier.
- ShipmentTracking: Represents shipment tracking information.
"""

from enum import Enum
from app import db

class ShippingStatus(Enum):
    """Enumeration of shipping statuses."""
    PENDING = 'pending'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'

class ShippingOrder(db.Model):
    """
    Represents a shipping order.

    Attributes:
    - id: Integer, primary key
    - order_id: Integer, unique order identifier
    - address: String, shipping address
    - status: String, current status of the order
    - shipping_method: String, method used for shipping
    - package_details: String, details about the package
    """

    __tablename__ = 'shipping_orders'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    status = db.Column(
        db.Enum(ShippingStatus, name='order_status'),
        default=ShippingStatus.PENDING,
        nullable=False
        )
    shipping_method = db.Column(db.String(100))
    package_details = db.Column(db.String(255))

    def __repr__(self):
        return f"ShippingOrder(id={self.id}, order_id={self.order_id}, address='{self.address}', status='{self.status}')"

class ShippingCarrier(db.Model):
    """
    Represents a shipping carrier.

    Attributes:
    - id: Integer, primary key
    - name: String, name of the carrier
    - api_key: String, API key for carrier's services
    - supported_services: String, list of supported services
    - api_endpoints: String, endpoints for carrier's API
    """

    __tablename__ = 'shipping_carriers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    api_key = db.Column(db.String(100), nullable=False)
    supported_services = db.Column(db.String(255))
    api_endpoints = db.Column(db.String(255))

    def __repr__(self):
        return f"ShippingCarrier(id={self.id}, name='{self.name}', api_key='{self.api_key}')"

class ShipmentTracking(db.Model):
    """
    Represents shipment tracking information.

    Attributes:
    - id: Integer, primary key
    - order_id: Integer, related order's identifier
    - status: String, current status of the shipment
    - location: String, current location of the shipment
    - estimated_delivery: DateTime, estimated delivery date
    - tracking_number: String, tracking number for the shipment
    - last_updated: DateTime, timestamp of the last update
    """

    __tablename__ = 'shipment_tracking'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))
    estimated_delivery = db.Column(db.DateTime)
    tracking_number = db.Column(db.String(50))
    last_updated = db.Column(db.DateTime)

    def __repr__(self):
        return f"ShipmentTracking(id={self.id}, order_id={self.order_id}, status='{self.status}', location='{self.location}')"
