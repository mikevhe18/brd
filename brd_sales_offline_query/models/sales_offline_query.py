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

    order_id = fields.Integer(string='Order ID')
    order_name = fields.Char(string='Order Name')
    pos_name = fields.Char(string='Pos Name')
    session_name = fields.Char(string='Session Name')
    user_id = fields.Many2one(
        string='User',
        comodel_name='res.users')
    product_id = fields.Many2one(
        string='Product',
        comodel_name='product.product')
    qty = fields.Float(string='Qty')
    price_unit = fields.Float(string='Price Unit')
    taxes = fields.Float(string='Taxes')
    amount = fields.Float(string='Subtotal')
    payment_method = fields.Char(string='Payment Method')
    date_order = fields.Date(string='Date Order')

    def _auto_init(self, cr, context=None):
        drop_view_if_exists(cr, self._table)
        strSQL = """
            CREATE OR REPLACE VIEW %(table)s AS (
                SELECT  A.order_id AS id,
                        A.name AS order_name,
                        D.name AS pos_name,
                        C.name AS session_name,
                        B.user_id AS user_id,
                        A.product_id AS product_id,
                        A.qty AS qty,
                        A.price_unit AS price_unit,
                        (0.1 * A.price_subtotal) AS taxes,
                        A.price_subtotal AS amount,
                        B.date_order AS date_order,
                        E.payment_method
                FROM	pos_order_line AS A
                JOIN	pos_order AS B ON B.id=A.order_id
                JOIN	pos_session AS C ON B.session_id=C.id
                JOIN	pos_config AS D ON C.config_id=D.id
                JOIN	(
                    SELECT 	A1.id,
                            array_to_string(
                                array_agg(D1.name), ', '
                            ) AS payment_method
                    FROM 	pos_order A1
                    JOIN	pos_session B1 ON A1.session_id=B1.id
                    JOIN	account_bank_statement C1 ON C1.pos_session_id=B1.id
                    JOIN	account_journal D1 ON C1.journal_id=D1.id
                    GROUP BY A1.id
                    ORDER BY A1.id
                ) AS E ON A.order_id=E.id
                ORDER BY A.order_id, B.date_order)
        """ % {'table': self._table}

        cr.execute(strSQL)

        return super(SalesOfflineQuery, self)._auto_init(
            cr, context=context)
