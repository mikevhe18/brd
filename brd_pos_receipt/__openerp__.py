# -*- coding: utf-8 -*-
{
    'name': 'Brodo PoS Receipt',
    'summary': 'PoS Receipt customization for bro.do',
    'version': '1.0',
    'category': 'Point Of Sale',
    'description': """
""",
    "author": "OpenSynergy Indonesia",
    'website': 'https://opensynergy-indonesia.com',
    'data': [
        'views/brd_pos_receipt_js.xml'],
    'depends': [
        'point_of_sale',
        ],
    'qweb': [
        'static/src/xml/brd_pos_receipt.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
