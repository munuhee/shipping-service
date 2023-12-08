from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from app import app, db
from app.models.shipping import ShippingOrder

@app.route('/health', methods=['GET'])
def health_check():
    """health check returning a success status"""
    application_status = {
        'status': 'healthy'
    }
    return jsonify(application_status), 200

@app.route('/shipping_orders', methods=['GET'])
def get_shipping_orders():
    """
    Retrieve all shipping orders.

    Returns:
        JSON: List of shipping orders.
    """
    try:
        orders = ShippingOrder.query.all()
        return jsonify([{
            'id': order.id,
            'order_id': order.order_id,
            'address': order.address,
            'status': order.status,
            'shipping_method': order.shipping_method,
            'package_details': order.package_details
        } for order in orders])
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to fetch shipping orders'}), 500

@app.route('/shipping_orders/<int:order_id>', methods=['GET'])
def get_shipping_order(order_id):
    """
    Retrieve a specific shipping order by ID.

    Args:
        order_id (int): ID of the shipping order to retrieve.

    Returns:
        JSON: Shipping order details.
    """
    try:
        order = db.session.get(ShippingOrder, order_id)
        return jsonify({
            'id': order.id,
            'order_id': order.order_id,
            'address': order.address,
            'status': order.status.value,
            'shipping_method': order.shipping_method,
            'package_details': order.package_details
        })
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to fetch shipping order'}), 500

@app.route('/shipping_orders', methods=['POST'])
def create_shipping_order():
    """
    Create a new shipping order.

    Returns:
        JSON: Confirmation message.
    """
    try:
        data = request.json
        new_order = ShippingOrder(
            order_id=data['order_id'],
            address=data['address'],
            status=data['status'].upper(),
            shipping_method=data['shipping_method'],
            package_details=data['package_details']
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'New shipping order created successfully'}), 201
    except (KeyError, SQLAlchemyError) as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create shipping order'}), 500

@app.route('/shipping_orders/<int:order_id>', methods=['PUT'])
def update_shipping_order(order_id):
    """
    Update a specific shipping order by ID.

    Args:
        order_id (int): ID of the shipping order to update.

    Returns:
        JSON: Confirmation message.
    """
    try:
        order = db.session.get(ShippingOrder, order_id)
        data = request.json
        order.order_id = data['order_id']
        order.address = data['address']
        order.status = data['status'].upper()
        order.shipping_method = data['shipping_method']
        order.package_details = data['package_details']
        db.session.commit()
        return jsonify({'message': 'Shipping order updated successfully'})
    except (KeyError, SQLAlchemyError) as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update shipping order'}), 500

@app.route('/shipping_orders/<int:order_id>', methods=['DELETE'])
def delete_shipping_order(order_id):
    """
    Delete a specific shipping order by ID.

    Args:
        order_id (int): ID of the shipping order to delete.

    Returns:
        JSON: Confirmation message.
    """
    try:
        order = db.session.get(ShippingOrder, order_id)
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Shipping order deleted successfully'})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete shipping order'}), 500

@app.route('/track_shipment/<int:order_id>', methods=['GET'])
def track_shipment(order_id):
    shipping_order = ShippingOrder.query.filter_by(order_id=order_id).first()
    if shipping_order:
        # Fetch tracking details from database for the given order_id
        shipment_tracking_info = ShipmentTracking.query.filter_by(order_id=order_id).all()
        if shipment_tracking_info:
            # Format and return tracking information
            # Construct response with tracking details
            return jsonify({'order_id': order_id, 'tracking_info': shipment_tracking_info}), 200
        else:
            return jsonify({'message': 'Tracking information not available'}), 404
    else:
        return jsonify({'message': 'Shipping order not found'}), 404
    
@app.route('/integrate_with_carrier', methods=['POST'])
def integrate_with_carrier():
    data = request.json
    # Assuming request contains necessary details like order_id, selected_carrier, package_details, etc.

    # Perform logic to integrate with the selected carrier API
    # Example: Retrieve rates, create shipping label, and handle carrier-specific operations
    # This could involve making requests to the carrier's API using provided credentials or keys

    # Upon successful integration, update the shipping order status and store tracking information
    shipping_order = ShippingOrder.query.filter_by(order_id=data.get('order_id')).first()
    if shipping_order:
        # Update status to 'Shipped' after successful integration with the carrier
        shipping_order.status = 'Shipped'
        db.session.commit()

        # Simulate storing tracking information in the database
        new_tracking_info = ShipmentTracking(
            order_id=data.get('order_id'),
            status='In transit',
            # Other tracking-related fields
        )
        db.session.add(new_tracking_info)
        db.session.commit()

        return jsonify({'message': 'Integration with carrier successful'}), 200
    else:
        return jsonify({'message': 'Shipping order not found'}), 404

@app.route('/update_shipment_status/<int:order_id>', methods=['PUT'])
def update_shipment_status(order_id):
    data = request.json
    new_status = data.get('status')

    # Update shipment status in the database
    shipping_order = ShippingOrder.query.filter_by(order_id=order_id).first()
    if shipping_order:
        shipping_order.status = new_status
        db.session.commit()

        # Update tracking information based on the new status
        # Example: Update location, estimated delivery time, etc. in the ShipmentTracking table

        return jsonify({'message': 'Shipment status updated successfully'}), 200
    else:
        return jsonify({'message': 'Shipping order not found'}), 404
