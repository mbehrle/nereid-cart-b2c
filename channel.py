# -*- coding: utf-8 -*-
"""
    channel.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""

from trytond.pool import PoolMeta

__metaclass__ = PoolMeta

__all__ = ['SaleChannel']


class SaleChannel:
    """
    Sale Channel
    """
    __name__ = 'sale.channel'

    @classmethod
    def __setup__(cls):
        super(SaleChannel, cls).__setup__()
        source = ('webshop', 'Webshop')
        if source not in cls.source.selection:
            cls.source.selection.append(source)
