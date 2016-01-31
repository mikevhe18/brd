# -*- coding: utf-8 -*-
# © 2016 Andhitia Rama <andhitia.r@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Brodo Daily Offline Product Performance Query',
    'version': '8.0.1.0.0',
    'category': 'Point Of Sale',
    'author': 'Andhitia Rama,OpenSynergy Indonesia',
    'website': 'https://opensynergy-indonesia.com',
    'data': [
        'security/ir.model.access.csv',
        'views/daily_offline_product_performance_query.xml',
        'menu/menu_Report.xml',
    ],
    'depends': [
        'brd_sales_offline_query',
        ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
