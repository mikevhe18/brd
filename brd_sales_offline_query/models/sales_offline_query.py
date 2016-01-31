# -*- coding: utf-8 -*-
# © 2016 Andhitia Rama <andhitia.r@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields
from openerp.tools import drop_view_if_exists


class SalesOfflineQuery(models.Model):

    _name = 'brd.query_sales_offline'
    _description = 'Sales Offline Query'
    _auto = False

    order_id = fields.Many2one(
        string='Order ID',
        comodel_name='pos.order',
        )
    order_name = fields.Char(
        string='Order Name',
        )
    pos_name = fields.Char(
        string='Pos Name',
        )
    pos_id = fields.Many2one(
        string='PoS',
        comodel_name='pos.config',
        )
    session_name = fields.Char(
        string='Session Name',
        )
    session_id = fields.Many2one(
        string='Session',
        comodel_name='pos.session',
        )
    user_id = fields.Many2one(
        string='User',
        comodel_name='res.users',
        )
    product_id = fields.Many2one(
        string='Product',
        comodel_name='product.product',
        )
    product_template_id = fields.Many2one(
        string='Product Template',
        comodel_name='product.template',
        )
    qty = fields.Float(
        string='Qty',
        )
    price_unit = fields.Float(
        string='Price Unit',
        )
    cost_unit = fields.Float(
        string='Cost Per Unit',
        )
    amount_cost = fields.Float(
        string='Cost',
        )
    profit = fields.Float(
        string='Profit/Loss',
        )
    taxes = fields.Float(
        string='Taxes',
        )
    amount = fields.Float(
        string='Subtotal Without Tax',
        )
    amount_incl = fields.Float(
        string='Subtotal With Tax',
        )
    date_order = fields.Datetime(
        string='Date Order',
        )
    day_order = fields.Date(
        string='Day Order',
        )

    def _auto_init(self, cr, context=None):
        drop_view_if_exists(cr, self._table)
        strSQL = """
            CREATE OR REPLACE VIEW %(table)s AS (
                SELECT  a.id AS id,
                        b.id AS order_id,
                        a.name AS order_name,
                        d.name AS pos_name,
                        c.config_id AS pos_id,
                        c.name AS session_name,
                        b.session_id AS session_id,
                        b.user_id AS user_id,
                        a.product_id AS product_id,
                        h.id AS product_template_id,
                        a.qty AS qty,
                        a.price_unit AS price_unit,
                        f.price_unit AS cost_unit,
                        (
                            f.price_unit
                            *
                            a.qty
                        ) AS amount_cost,
                        a.price_subtotal AS amount,
                        a.price_subtotal_incl AS amount_incl,
                        (
                            a.price_subtotal_incl
                            - a.price_subtotal
                        ) AS taxes,
                        (
                            a.price_subtotal
                            -
                            (
                            f.price_unit
                            *
                            a.qty
                            )
                        ) AS profit,
                        b.date_order AS date_order,
                        b.date_order::timestamp::date AS day_order
                FROM    pos_order_line AS a
                JOIN    pos_order AS b ON b.id=a.order_id
                JOIN    pos_session AS c ON b.session_id=c.id
                JOIN    pos_config AS d ON c.config_id=d.id
                JOIN    stock_picking AS e ON b.picking_id=e.id
                JOIN    stock_move AS f ON e.id=f.picking_id
                JOIN    product_product AS g ON a.product_id=g.id
                JOIN    product_template AS h ON g.product_tmpl_id=h.id
                ORDER BY a.order_id, b.date_order)
        """ % {'table': self._table}

        cr.execute(strSQL)

        return super(SalesOfflineQuery, self)._auto_init(
            cr, context=context)
