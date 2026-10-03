from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestMaterial(TransactionCase):
    def setUp(self):
        super(TestMaterial, self).setUp()
        self.supplier = self.env['res.partner'].create({'name': 'Test Supplier'})

    def test_create_valid_material(self):
        material = self.env['material.material'].create({
            'code': 'M001',
            'name': 'Cotton Fabric',
            'type': 'fabric',
            'buy_price': 150,
            'supplier_id': self.supplier.id,
        })
        self.assertEqual(material.code, 'M001')
        self.assertEqual(material.name, 'Cotton Fabric')
        self.assertEqual(material.type, 'fabric')
        self.assertEqual(material.buy_price, 150)
        self.assertEqual(material.supplier_id.id, self.supplier.id)

    def test_buy_price_constraint(self):
        with self.assertRaises(ValidationError):
            self.env['material.material'].create({
                'code': 'M002',
                'name': 'Cheap Fabric',
                'type': 'fabric',
                'buy_price': 50,
                'supplier_id': self.supplier.id,
            })