"""
SDoc

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
# ----------------------------------------------------------------------------------------------------------------------
from sdoc.helper.Html import Html
from sdoc.sdoc2 import node_store
from sdoc.sdoc2.decorator.html.HtmlDecorator import HtmlDecorator


class HyperlinkHtmlDecorator(HtmlDecorator):
    """
    HtmlDecorator for generating HTML code for hyperlinks.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def generate(self, node, file):
        """
        Generates the HTML code for a hyperlink node.

        :param sdoc.sdoc2.node.HyperlinkNode.HyperlinkNode node: The hyperlink node.
        :param file file: The output file.
        """
        file.write(Html.generate_element('a', node.get_html_attributes(), node._argument))


# ----------------------------------------------------------------------------------------------------------------------
node_store.register_format_decorator('hyperlink', 'html', HyperlinkHtmlDecorator)
