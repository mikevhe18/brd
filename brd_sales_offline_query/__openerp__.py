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

{
    'name': 'Brodo Sales Offline Query',
    'summary': 'Sales Offline Query customization for bro.do',
    'version': '8.0.1.0.0',
    'category': 'Point Of Sale',
    'description': """
        This module represent another function of reporting system.
        The customize is create a Sales Offline Query.
    """,
    'author': 'Michael Viriyananda,OpenSynergy Indonesia',
    'website': 'https://opensynergy-indonesia.com',
    'data': [
        'view/sales_offline_query.xml',
        'menu/menu_Query.xml'
    ],
    'depends': [],
    'qweb': [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
