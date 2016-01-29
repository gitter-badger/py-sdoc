"""
SDoc

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
# ----------------------------------------------------------------------------------------------------------------------
from sdoc.sdoc2 import node_store
from sdoc.sdoc2.node.Node import Node


class ItemizeNode(Node):
    """
    SDoc2 node for itemize.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        super().__init__('itemize')

    # ------------------------------------------------------------------------------------------------------------------
    def get_hierarchy_level(self):
        """
        Returns 0.

        :rtype: int
        """
        return 0

    # ------------------------------------------------------------------------------------------------------------------
    def get_hierarchy_name(self):
        """
        Returns 'item'

        :rtype: str
        """
        return 'item'

    # ------------------------------------------------------------------------------------------------------------------
    def is_block_command(self):
        """
        Returns True.

        :rtype: bool
        """
        return True

    # ------------------------------------------------------------------------------------------------------------------
    def is_hierarchy_root(self):
        """
        Returns True.

        :rtype: bool
        """
        return True

    # ------------------------------------------------------------------------------------------------------------------
    def is_inline_command(self):
        """
        Returns False.

        :rtype: bool
        """
        return False

    # ------------------------------------------------------------------------------------------------------------------
    def is_phrasing(self):
        """
        Returns True.

        :rtype: bool
        """
        return False


# ----------------------------------------------------------------------------------------------------------------------
node_store.register_block_command('itemize', ItemizeNode)