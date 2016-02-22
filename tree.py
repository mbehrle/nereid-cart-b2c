# -*- coding: utf-8 -*-
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from sql import Literal


__all__ = ['Node']
__metaclass__ = PoolMeta


class Node:
    __name__ = "product.tree_node"

    def _get_products(self):
        """
        Return a query based on the node settings. This is separated for
        easy subclassing. The returned value would be a tuple with the
        dollowing elements:

            * The Model instance
            * Select query instance
            * The Table instance for the SQL Pagination

        """
        pool = Pool()
        Node = pool.get('product.tree_node')
        Product = pool.get('product.product')
        ProductTemplate = pool.get('product.template')
        ProductNodeRelation = pool.get('product.product-product.tree_node')
        Listing = pool.get('product.product.channel_listing')
        Channel = pool.get('sale.channel')

        ProductTable = Product.__table__()
        TemplateTable = ProductTemplate.__table__()
        RelTable = ProductNodeRelation.__table__()
        NodeTable = Node.__table__()
        ListingTable = Listing.__table__()
        ChannelTable = Channel.__table__()

        current_channel = Transaction().context.get('current_channel')
        if self.display == 'product.product':
            query = ProductTable.join(
                TemplateTable,
                condition=(TemplateTable.id == ProductTable.template)
            ).join(
                RelTable,
                condition=(RelTable.product == ProductTable.id)
            ).join(
                NodeTable,
                condition=(RelTable.node == NodeTable.id)
            ).join(
                ListingTable,
                condition=(ProductTable.id == ListingTable.product)
            ).join(
                ChannelTable,
                condition=(ChannelTable.id == ListingTable.channel)
            ).select(
                where=(
                    TemplateTable.active &
                    (ChannelTable.source == 'webshop') &
                    (ListingTable.state == 'active') &
                    (ListingTable.channel == current_channel) &
                    ProductTable.active &
                    (NodeTable.left >= Literal(self.left)) &
                    (NodeTable.right <= Literal(self.right))
                ),
                order_by=RelTable.sequence.asc
            )
            return Product, query, ProductTable

        elif self.display == 'product.template':
            query = TemplateTable.join(
                ProductTable,
                condition=(TemplateTable.id == ProductTable.template)
            ).join(
                RelTable,
                condition=(RelTable.product == ProductTable.id)
            ).join(
                NodeTable,
                condition=(RelTable.node == NodeTable.id)
            ).join(
                ListingTable,
                condition=(ProductTable.id == ListingTable.product)
            ).join(
                ChannelTable,
                condition=(ChannelTable.id == ListingTable.channel)
            ).select(
                where=(
                    TemplateTable.active &
                    (ChannelTable.source == 'webshop') &
                    (ListingTable.state == 'active') &
                    (ListingTable.channel == current_channel) &
                    ProductTable.active &
                    (NodeTable.left >= Literal(self.left)) &
                    (NodeTable.right <= Literal(self.right))
                ),
                order_by=RelTable.sequence.asc
            )
            return ProductTemplate, query, TemplateTable
