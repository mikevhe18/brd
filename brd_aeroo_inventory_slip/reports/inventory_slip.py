# -*- coding: utf-8 -*-
# © 2016 Andhitia Rama <andhitia.r@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.report.report_sxw import rml_parse


class Parser(rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.data_list = []
        self.localcontext.update({
            'get_product_list': self.get_product_template
        })

    def get_product_template(self):
        # obj_picking = self.pool.get('stock.picking')
        obj_move = self.pool.get('stock.move')
        obj_template = self.pool.get('product.template')
        picking_id = self.context.get('active_id', False)
        # picking = obj_picking.browse(self.cr, self.uid, [picking_id])[0]
        strSQL = """
                SELECT DISTINCT b.product_tmpl_id
                FROM stock_move AS a
                JOIN product_product AS b ON a.product_id = b.id
                WHERE a.picking_id = %s
                """ % (picking_id)
        self.cr.execute(strSQL)
        for a in self.cr.fetchall():
            template_id = a[0]
            template = obj_template.browse(self.cr, self.uid, [template_id])[0]
            dict_1 = {
                'template_id': template.id,
                'template_name': template.name,
                'moves': [],
            }
            criteria = [
                ('picking_id', '=', picking_id),
                ('product_id.product_tmpl_id', '=', template_id)
            ]
            move_ids = obj_move.search(self.cr, self.uid, criteria)
            no = 1
            for move in obj_move.browse(self.cr, self.uid, move_ids):
                dict_2 = {
                    'no': no,
                    'product_name': move.product_id.display_name,
                    'uom': move.product_uom.name,
                    'qty': move.product_uom_qty,
                }
                dict_1['moves'].append(dict_2)
                no += 1
            self.lst_product_template.append(dict_1)
        return self.lst_product_template
