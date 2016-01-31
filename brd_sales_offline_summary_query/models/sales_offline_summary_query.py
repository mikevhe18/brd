# -*- coding: utf-8 -*-
# © 2016 Andhitia Rama <andhitia.r@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields
from openerp.tools import drop_view_if_exists


class SalesOfflineSummaryQuery(models.Model):

    _name = 'brd.query_sales_offline_summary'
    _description = 'Sales Offline Summary Query'
    _auto = False

    name = fields.Char(
        string='# Order',
        )
    session_id = fields.Many2one(
        string='Session',
        comodel_name='pos.session',
        )
    pos_id = fields.Many2one(
        string='PoS',
        comodel_name='pos.config',
        )
    date_timestamp = fields.Datetime(
        string='Order Timestamp',
        )
    date_order = fields.Date(
        string='Date',
        )
    user_id = fields.Many2one(
        string='Cashier',
        comodel_name='res.users',
        )
    quantity = fields.Float(
        string='Qty.',
        )
    amount_gross = fields.Float(
        string='Gross',
        )
    amount_nett = fields.Float(
        string='Nett',
        )
    amount_taxes = fields.Float(
        string='Taxes',
        )
    amount_nett_incl = fields.Float(
        string='Nett Include Taxes',
        )
    amount_cost = fields.Float(
        string='Cost',
        )
    amount_profit = fields.Float(
        string='Profit',
        )

    def _auto_init(self, cr, context=None):
        drop_view_if_exists(cr, self._table)
        strSQL = """
            CREATE OR REPLACE VIEW %(table)s AS (
                SELECT  a.id AS id,
                        a.name AS name,
                        a.session_id AS session_id,
                        b.config_id AS pos_id,
                        a.user_id AS user_id,
                        a.date_order AS date_timestamp,
                        a.date_order::timestamp::date AS date_order,
                        c.quantity AS quantity,
                        0 AS amount_gross,
                        c.amount_nett AS amount_nett,
                        c.amount_taxes AS amount_taxes,
                        c.amount_nett_incl AS amount_nett_incl,
                        c.amount_cost AS amount_cost,
                        c.amount_profit AS amount_profit
                FROM    pos_order AS a
                JOIN    pos_session AS b ON a.session_id=b.id
                LEFT JOIN   (
                        SELECT  order_id AS order_id,
                                SUM(qty) AS quantity,
                                SUM(amount) AS amount_nett,
                                SUM(taxes) AS amount_taxes,
                                SUM(amount_incl) AS amount_nett_incl,
                                SUM(amount_cost) AS amount_cost,
                                SUM(profit) AS amount_profit
                        FROM    brd_query_sales_offline
                        GROUP BY    order_id
                        ) AS c ON a.id=c.order_id
                )
        """ % {'table': self._table}

        cr.execute(strSQL)

        return super(SalesOfflineSummaryQuery, self)._auto_init(
            cr, context=context)
