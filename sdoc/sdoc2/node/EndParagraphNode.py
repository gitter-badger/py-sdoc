"""
SDoc

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
# ----------------------------------------------------------------------------------------------------------------------
from sdoc.sdoc2 import node_store
from sdoc.sdoc2.node.Node import Node


class EndParagraphNode(Node):
    """
    SDoc2 node for end of paragraphs.

    Note: End of paragraphs will are temporary used during the content tree preparation. Before and after the content
          preparation end of paragraph nodes do not exist.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, options, argument):
        """
        Object constructor.

        :param dict[str,str] options: Not used.
        :param str argument: Not used.
        """
        super().__init__('end_paragraph', options, argument)

    # ------------------------------------------------------------------------------------------------------------------
    def is_block_command(self):
        """
        Returns False.

        :rtype: bool
        """
        return False

    # ------------------------------------------------------------------------------------------------------------------
    def is_inline_command(self):
        """
        Returns False.

        :rtype: bool
        """
        return False

    # ------------------------------------------------------------------------------------------------------------------
    def prepare_content_tree(self):
        """
        Not implemented for end paragraph nodes.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
node_store.register_inline_command('end_paragraph', EndParagraphNode)
