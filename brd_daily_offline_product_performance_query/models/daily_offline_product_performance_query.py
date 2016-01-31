# -*- coding: utf-8 -*-
# © 2016 Andhitia Rama <andhitia.r@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields
from openerp.tools import drop_view_if_exists


class DailyOfflineProductPerformanceQuery(models.Model):

    _name = 'brd.daily_offline_product_performance_query'
    _description = 'Daily Offline Product Performance Query'
    _auto = False
    _order = 'date_order'

    product_template_id = fields.Many2one(
        string='Product Template',
        comodel_name='product.template',
        )

    pos_id = fields.Many2one(
        string='PoS',
        comodel_name='pos.config',
        )

    date_order = fields.Date(
        string='Date Order',
        )

    quantity = fields.Float(
        string='Quantity',
        )

    total = fields.Float(
        string='Total'
        )

    def _auto_init(self, cr, context=None):
        drop_view_if_exists(cr, self._table)
        strSQL = """
            CREATE OR REPLACE VIEW %(table)s AS (
                SELECT  row_number() OVER() AS id,
                        a.product_template_id AS product_template_id,
                        a.pos_id AS pos_id,
                        a.day_order AS date_order,
                        SUM(a.qty) AS quantity,
                        SUM(a.amount) AS total
                FROM   brd_query_sales_offline AS a
                GROUP BY product_template_id,day_order,pos_id
                )
        """ % {'table': self._table}

        cr.execute(strSQL)

        return super(DailyOfflineProductPerformanceQuery, self)._auto_init(
            cr, context=context)
