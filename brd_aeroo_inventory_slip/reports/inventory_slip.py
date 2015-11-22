# -*- encoding: utf-8 -*-
##############################################################################
#
# Author : Andhitia Rama, Michael Viriyananda, Nurazmi
# Copyright (C) 2015 OpenSynergy Indonesia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from report import report_sxw


class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.data_list = []
        self.localcontext.update({'get_address': self.get_address})

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
