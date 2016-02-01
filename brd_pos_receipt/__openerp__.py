# -*- coding: utf-8 -*-
# © 2016 Andhitia Rama <andhitia.r@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Brodo PoS Receipt',
    'version': '1.0',
    'category': 'Point Of Sale',
    "author": "OpenSynergy Indonesia",
    'website': 'https://opensynergy-indonesia.com',
    'data': [
        'views/brd_pos_receipt_js.xml'],
    'depends': [
        'point_of_sale',
        'pos_stock',
        'pos_order_discount',
        'pos_carry_bag',
        'wk_pos_order_notes'
        ],
    'qweb': [
        'static/src/xml/brd_pos_receipt.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
