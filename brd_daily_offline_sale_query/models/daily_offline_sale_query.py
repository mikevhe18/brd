# -*- coding: utf-8 -*-
# © 2016 Andhitia Rama <andhitia.r@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields
from openerp.tools import drop_view_if_exists


class DailyOfflineSaleQuery(models.Model):

    _name = 'brd.daily_offline_sale_query'
    _description = 'Daily Offline Sale Query'
    _auto = False

    pos_id = fields.Many2one(
        string='PoS',
        comodel_name='pos.config',
        )

    date_order = fields.Date(
        string='Date Order',
        )

    trx_count = fields.Integer(
        string='Transaction Count',
        )

    quantity = fields.Float(
        string='Quantity',
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
        string='Nett Incl. Taxes'
        )

    amount_cost = fields.Float(
        string='Cost',
        )

    amount_profit = fields.Float(
        string='Profit'
        )

    def _auto_init(self, cr, context=None):
        drop_view_if_exists(cr, self._table)
        strSQL = """
            CREATE OR REPLACE VIEW %(table)s AS (
                SELECT  row_number() OVER() AS id,
                        a.pos_id AS pos_id,
                        a.date_order AS date_order,
                        COUNT(a.id) AS trx_count,
                        SUM(a.quantity) AS quantity,
                        SUM(a.amount_gross) AS amount_gross,
                        SUM(a.amount_nett) AS amount_nett,
                        SUM(a.amount_taxes) AS amount_taxes,
                        SUM(a.amount_nett_incl) AS amount_nett_incl,
                        SUM(a.amount_cost) AS amount_cost,
                        SUM(a.amount_profit) AS amount_profit
                FROM   brd_query_sales_offline_summary AS a
                GROUP BY pos_id, date_order
                )
        """ % {'table': self._table}

        cr.execute(strSQL)

        return super(DailyOfflineSaleQuery, self)._auto_init(
            cr, context=context)
