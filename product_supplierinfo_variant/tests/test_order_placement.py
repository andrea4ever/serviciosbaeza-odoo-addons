# -*- coding: utf-8 -*-
# © 2016 A. Gallina (<a.gallina@apuliasoftware.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestOrderPlacement(TransactionCase):

    def _create_procurement(self, product, supplier, route, warehouse):
        # ---- Update Product Supplier Info's
        product.seller_ids = [(0, 0, {'name': supplier.id})]
        # ---- Update Product Route
        product.route_ids = [(6, 0, [route.id])]
        # ---- Create Procurement
        procurement = self.env['procurement.order'].create({
            'product_id': product.id,
            'product_qty': 2.0,
            'name': 'Test1',
            'warehouse_id': warehouse.id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'product_uom': product.uom_id.id,
        })
        # ---- Run Procurement
        procurement.run()
        return procurement

    def _create_procurement2(self, product, supplier, route, warehouse):
        # ---- Update Product Supplier Info's
        product.seller_ids = [(0, 0, {'name': supplier.id})]
        # ---- Update Product Route
        product.route_ids = [(6, 0, [route.id])]
        # ---- Create Procurement
        procurement = self.env['procurement.order'].create({
            'product_id': product.id,
            'product_qty': 2.0,
            'name': 'Test1',
            'warehouse_id': warehouse.id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'product_uom': product.uom_id.id,
        })
        # ---- Run Procurement
        procurement.run()
        return procurement

    def setUp(self):
        super(TestOrderPlacement, self).setUp()
        self.product_1 = self.env.ref('product.product_product_4')
        self.product_2 = self.env.ref('product.product_product_4c')
        self.supplier_1 = self.env.ref('base.res_partner_1')
        self.supplier_2 = self.env.ref('base.res_partner_16')
        self.route_buy = self.env.ref('purchase.route_warehouse0_buy')
        self.warehouse = self.env.ref('stock.warehouse0')
        self.procurement_1 = self._create_procurement(
            self.product_1, self.supplier_1, self.route_buy, self.warehouse)
        self.procurement_2 = self._create_procurement2(
            self.product_2, self.supplier_2, self.route_buy, self.warehouse)

    def test_procurement(self):
        # --- Test if procurement have a purchase order
        self.assertEqual(
            self.procurement_1.state, 'running', msg='Procurement 1 Fail')
        self.assertEqual(
            self.procurement_2.state, 'running', msg='Procurement 2 Fail')

    def test_procurement_data(self):
        self.assertEqual(
            self.procurement_1.purchase_id.partner_id.id, self.supplier_1.id,
            msg='Product Supplier and Order diverged on procurement 1')
        self.assertEqual(
            self.procurement_2.purchase_id.partner_id.id, self.supplier_2.id,
            msg='Product Supplier and Order diverged on procurement 2')
