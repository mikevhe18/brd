# -*- coding: utf-8 -*-
# © 2016 Andhitia Rama <andhitia.r@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Brodo Sales Offline Query',
    'version': '8.0.1.0.0',
    'category': 'Point Of Sale',
    'author': 'Michael Viriyananda,OpenSynergy Indonesia',
    'website': 'https://opensynergy-indonesia.com',
    'data': [
        'security/ir.model.access.csv',
        'security/data_Groups.xml',
        'view/sales_offline_query.xml',
        'menu/menu_Query.xml'
    ],
    'depends': [
        'point_of_sale',
        'brd_reporting',
        ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
