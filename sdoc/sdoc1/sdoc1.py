"""
SDoc

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
# ----------------------------------------------------------------------------------------------------------------------
import antlr4
from sdoc.antlr.sdoc1Lexer import sdoc1Lexer
from sdoc.antlr.sdoc1Parser import sdoc1Parser
from sdoc.antlr.sdoc1ParserVisitor import sdoc1ParserVisitor
from sdoc.sdoc1.data_type.ArrayDataType import ArrayDataType
from sdoc.sdoc1.data_type.IdentifierDataType import IdentifierDataType
from sdoc.sdoc1.data_type.IntegerDataType import IntegerDataType
from sdoc.sdoc1.data_type.StringDataType import StringDataType


class Sdoc1(sdoc1ParserVisitor):
    """
    Visitor for SDoc level 1.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._output = None
        """
        Object for streaming the generated output. This object MUST implement the write method.
        """

        self._global_scope = ArrayDataType()
        """
        All defined variables at global scope.

        :type: sdoc.sdoc1.data_type.ArrayDataType.ArrayDataType
        """

        self._include_level = 0
        """
        The level of including other SDoc documents.

        :type: int
        """

        self._options = {'max_include_level': 100}
        """
        The options.

        :type: dict
        """

    # ------------------------------------------------------------------------------------------------------------------
    def set_output(self, output):
        """
        Sets the object for streaming the generated output.

        :param output: This object MUST implement the write method.
        """
        self._output = output

    # ------------------------------------------------------------------------------------------------------------------
    def _set_global_scope(self, scope):
        """
        Sets the global scope for variables.

        :param sdoc.sdoc1.data_type.ArrayDataType.ArrayDataType scope: The global scope.
        """
        self._global_scope = scope

    # ------------------------------------------------------------------------------------------------------------------
    def stream(self, snippet):
        """
        Puts an output snippet on the output stream.

        :param str snippet: The snippet to be appended to the output stream of this parser.
        """
        if snippet is not None:
            self._output.write(snippet)

    # ------------------------------------------------------------------------------------------------------------------
    def visitAssignmentExpressionAssignment(self, ctx):
        """
        Visit a parse tree produced by sdoc1Parser#assignmentExpressionAssignment.

        :param sdoc1Parser.AssignmentExpressionAssignmentContext ctx: The context tree.
        """
        right_hand_side = ctx.assignmentExpression().accept(self)
        left_hand_side = ctx.postfixExpression().accept(self)

        # Left hand side must be an identifier.
        # @todo implement array element.
        if not isinstance(left_hand_side, IdentifierDataType):
            raise RuntimeError("Left hand side '%s' is not an identifier." % str(left_hand_side))
            # @todo more verbose logging, own exception class

        return left_hand_side.set_value(right_hand_side)

    # ------------------------------------------------------------------------------------------------------------------
    def visitPrimaryExpressionIdentifier(self, ctx):
        """
        Visits a parse tree produced by sdoc1Parser#primaryExpressionIdentifier.

        :param sdoc1Parser.PrimaryExpressionIdentifierContext ctx: The context tree.
        """
        return IdentifierDataType(self._global_scope, ctx.EXPR_IDENTIFIER().getText())

    # ------------------------------------------------------------------------------------------------------------------
    def visitPrimaryExpressionIntegerConstant(self, ctx):
        """
        Visits a parse tree produced by sdoc1Parser#PrimaryExpressionIntegerConstantContext.

        :param sdoc1Parser.PrimaryExpressionIntegerConstantContext ctx: The context tree.
        """
        return IntegerDataType(ctx.EXPR_INTEGER_CONSTANT().getText())

    # ------------------------------------------------------------------------------------------------------------------
    def visitPrimaryExpressionStringConstant(self, ctx):
        """
        Visits a parse tree produced by sdoc1Parser#PrimaryExpressionStringConstantContext.

        :param sdoc1Parser.PrimaryExpressionStringConstantContext ctx: The context tree.
        """
        return StringDataType(ctx.EXPR_STRING_CONSTANT().getText()[1:-1])

    # ------------------------------------------------------------------------------------------------------------------
    def visitCmd_comment(self, ctx):
        """
        Visits a parse tree produced by sdoc1Parser#cmd_comment.

        :param sdoc1Parser.Cmd_commentContext ctx: The context tree.
        """
        # @todo If previous char is not a new line (i.e. middle in the line comment) print newline
        # @todo otherwise print new line

        self.stream('')
        # @todo set position

    # ------------------------------------------------------------------------------------------------------------------
    def visitCmd_debug(self, ctx):
        """
        Visits a parse tree produced by sdoc1Parser#cmd_debug.

        :param sdoc1Parser.Cmd_debugContext ctx: The context tree.
        """
        expression = ctx.expression()

        if expression is not None:
            print(expression.accept(self).debug())
        else:
            print(self._global_scope.debug())

    # ------------------------------------------------------------------------------------------------------------------
    def visitCmd_expression(self, ctx):
        """
        Visits a parse tree produced by sdoc1Parser#cmd_expression.

        :param sdoc1Parser.Cmd_expressionContext ctx: The context tree.
        """
        self.visitExpression(ctx.expression())
        # @todo set position

    # ------------------------------------------------------------------------------------------------------------------
    def visitCmd_if(self, ctx):
        """
        Visits a parse tree produced by sdoc1Parser#cmd_if.

        :param sdoc1Parser.Cmd_ifContext ctx: The parse tree.
        """
        n = ctx.getChildCount()
        fired = False
        i = 0
        while i < n and not fired:
            child = ctx.getChild(i)
            token = child.getText()
            i += 1
            if token == '\\if' or token == '\\elif':
                # Skip {
                i += 1

                # Child is the expression to be evaluated.
                child = ctx.getChild(i)
                i += 1
                data = child.accept(self)
                """
                :type: sdoc.sdoc1.data_type.DataType.DataType
                """

                # Skip }
                i += 1

                if data.is_true():
                    # Child is the code inside the if or elif clause.
                    child = ctx.getChild(i)
                    i += 1
                    child.accept(self)
                    fired = True

                else:
                    # Skip the code inside the if or elif clause.
                    i += 1

            elif token == '\\else':
                # Child is the code inside the else clause.
                child = ctx.getChild(i)
                i += 1

                child.accept(self)
                fired = True

            elif token == '\\endif':
                # @todo set position
                pass

    # ------------------------------------------------------------------------------------------------------------------
    def visitCmd_include(self, ctx):
        """
        Includes another SDoc into this SDoc.

        :param sdoc1Parser.Cmd_includeContext ctx: The parse tree.
        """
        # Test the maximum include level.
        if self._include_level >= self._options['max_include_level']:
            raise RuntimeError("Maximum include level exceeded.")   # @todo More verbose logging, own exception class.

        # Open a stream for the sub-document.
        file_name = ctx.SIMPLE_ARG().getText()  # @todo unescape
        stream = antlr4.FileStream(file_name)

        # Create a new lexer and parser for the sub-document.
        lexer = sdoc1Lexer(stream)
        tokens = antlr4.CommonTokenStream(lexer)
        parser = sdoc1Parser(tokens)
        tree = parser.sdoc()
        visitor = Sdoc1()

        # Set or inherit properties from the parser of the parent document.
        visitor._include_level = self._include_level + 1
        visitor.set_output(self._output)
        visitor._set_global_scope(self._global_scope)

        # Run the visitor on the parse tree.
        visitor.visit(tree)

        # @todo test on errors and warnings from parser and pass back to parent parser

    # ------------------------------------------------------------------------------------------------------------------
    def visitCmd_notice(self, ctx):
        """
        Visits a parse tree produced by sdoc1Parser#cmd_notice.

        :param sdoc1Parser.Cmd_noticeContext ctx: The parse tree.
        """
        # @todo print position
        # @todo unescape
        print('Notice: ' + ctx.SIMPLE_ARG().getText())
        # @todo set position

    # ------------------------------------------------------------------------------------------------------------------
    def visitCmd_sdoc2(self, ctx):
        """
        Visits a parse tree produced by sdoc1Parser#sdoc2_cmd.

        :param sdoc1Parser.Cmd_sdoc2Context ctx: The parse tree.
        """
        self.stream(ctx.SDOC2_COMMAND().getText())

    # ------------------------------------------------------------------------------------------------------------------
    def visitText(self, ctx):
        """
        Visits a parse tree produced by sdoc1Parser#text.

        :param sdoc1Parser.TextContext ctx: The parse tree.
        """
        self.stream(ctx.TEXT().getText())

# ----------------------------------------------------------------------------------------------------------------------
