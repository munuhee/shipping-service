"""
This module contains unit tests for the ShippingOrder routes in the Flask application.

It tests the endpoints related to managing shipping orders including fetching all orders,
fetching a specific order, creating, updating, and deleting orders.
"""

import unittest
from flask import json
from app import app, db
from app.models.shipping import ShippingOrder

class TestShippingOrderRoutes(unittest.TestCase):
    """
    A test case for testing the ShippingOrder routes in the Flask application.

    Methods:
    - setUp: Set up a test environment.
    - tearDown: Clean up the test environment.
    - test_get_shipping_orders: Test GET method for fetching all shipping orders.
    - test_get_shipping_order: Test GET method for fetching a specific shipping order.
    - test_create_shipping_order: Test POST method for creating a new shipping order.
    - test_update_shipping_order: Test PUT method for updating a shipping order.
    - test_delete_shipping_order: Test DELETE method for deleting a shipping order.
    """

    def setUp(self):
        """ Set up test environment """
        self.app = app.test_client()

        with app.app_context():
            app.config['TESTING'] = True
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
            db.create_all()

    def tearDown(self):
        """ Remove test environment """
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_health_check(self):
        """ Test the health check endpoint """
        with app.app_context():
            response = self.app.get('/health')
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'healthy')

    def test_get_shipping_orders(self):
        """
        Test GET method for fetching all shipping orders.
        """
        with app.app_context():
            response = self.app.get('/shipping_orders')
            self.assertEqual(response.status_code, 200)

    def test_get_shipping_order(self):
        """
        Test GET method for fetching a specific shipping order.
        """
        with app.app_context():
            shipping_order = ShippingOrder(
                order_id=123,
                address='123 Shipping Street',
                status='PENDING',
                shipping_method='Air',
                package_details='Small package'
            )
            db.session.add(shipping_order)
            db.session.commit()

            response = self.app.get('/shipping_orders/1')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(data['id'], 1)

    def test_create_shipping_order(self):
        """
        Test POST method for creating a new shipping order.
        """
        with app.app_context():
            new_order_data = {
                'order_id': 456,
                'address': '456 Shipping Street',
                'status': 'SHIPPED',
                'shipping_method': 'Sea',
                'package_details': 'Large package'
            }

            response = self.app.post('/shipping_orders', json=new_order_data)
            self.assertEqual(response.status_code, 201)

    def test_update_shipping_order(self):
        """
        Test PUT method for updating a shipping order.
        """
        with app.app_context():
            shipping_order = ShippingOrder(
                order_id=789,
                address='789 Shipping Street',
                status='DELIVERED',
                shipping_method='Ground',
                package_details='Medium package'
            )
            db.session.add(shipping_order)
            db.session.commit()

            update_data = {
                'order_id': 789,
                'address': 'Updated Shipping Street',
                'status': 'PENDING',
                'shipping_method': 'Air',
                'package_details': 'Updated package details'
            }

            response = self.app.put('/shipping_orders/1', json=update_data)
            self.assertEqual(response.status_code, 200)

    def test_delete_shipping_order(self):
        """
        Test DELETE method for deleting a shipping order.
        """
        with app.app_context():
            shipping_order = ShippingOrder(
                order_id=999,
                address='999 Shipping Street',
                status='SHIPPED',
                shipping_method='Air',
                package_details='Small package'
            )
            db.session.add(shipping_order)
            db.session.commit()

            response = self.app.delete('/shipping_orders/1')
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
