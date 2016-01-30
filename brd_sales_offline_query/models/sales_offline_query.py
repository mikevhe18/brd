# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Michael Viriyananda
#    Copyright 2016 OpenSynergy Indonesia
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

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
    qty = fields.Float(
        string='Qty',
        )
    price_unit = fields.Float(
        string='Price Unit',
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
    date_order = fields.Date(
        string='Date Order',
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
                        a.qty AS qty,
                        a.price_unit AS price_unit,
                        a.price_subtotal AS amount,
                        a.price_subtotal_incl AS amount_incl,
                        (
                            a.price_subtotal_incl
                            - a.price_subtotal
                        ) AS taxes,
                        b.date_order AS date_order
                FROM	pos_order_line AS a
                JOIN	pos_order AS b ON b.id=a.order_id
                JOIN	pos_session AS c ON b.session_id=c.id
                JOIN	pos_config AS d ON c.config_id=d.id
                ORDER BY a.order_id, b.date_order)
        """ % {'table': self._table}

        cr.execute(strSQL)

        return super(SalesOfflineQuery, self)._auto_init(
            cr, context=context)
