from sly import Parser
from components.lexica import MyLexer
from components.ast import statement as ast_module


class MyParser(Parser):
    tokens = MyLexer.tokens
    # Precedence from lowest to highest
    precedence = (
        ('left', 'EQEQ', 'NOTEQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
    )

    # The start symbol
    @_('statements')
    def program(self, p):
        return p.statements

    @_('stmt')
    def statements(self, p):
        return [p.stmt]

    @_('stmt statements')
    def statements(self, p):
        return [p.stmt] + p.statements

    # Statement rules
    @_('NAME EQUAL expr')
    def stmt(self, p):
        return ast_module.StatementAssign(p.NAME, p.expr)

    @_('IF expr THEN statements END')
    def stmt(self, p):
        return ast_module.StatementIf(p.expr, ast_module.StatementBlock(p.statements))

    @_('IF expr THEN statements ELSE statements END')
    def stmt(self, p):
        return ast_module.StatementIf(p.expr, ast_module.StatementBlock(p.statements0),
                                       ast_module.StatementBlock(p.statements1))

    @_('WHILE expr DO statements END')
    def stmt(self, p):
        return ast_module.StatementWhile(p.expr, ast_module.StatementBlock(p.statements))

    @_('DEF NAME LPAREN parameters RPAREN statements END')
    def stmt(self, p):
        return ast_module.StatementFunctionDef(p.NAME, p.parameters, ast_module.StatementBlock(p.statements))

    @_('PRINT LPAREN expr RPAREN')
    def stmt(self, p):
        return ast_module.StatementPrint(p.expr)

    @_('NAME LPAREN arguments RPAREN')
    def stmt(self, p):
        return ast_module.StatementFunctionCall(p.NAME, p.arguments)

    # Expression rules
    @_('expr EQEQ expr')
    def expr(self, p):
        return ast_module.ExpressionCompare('==', p.expr0, p.expr1)

    @_('expr NOTEQ expr')
    def expr(self, p):
        return ast_module.ExpressionCompare('!=', p.expr0, p.expr1)

    @_('expr PLUS expr')
    def expr(self, p):
        return ast_module.ExpressionBinary(ast_module.Operations.PLUS, p.expr0, p.expr1)

    @_('expr MINUS expr')
    def expr(self, p):
        return ast_module.ExpressionBinary(ast_module.Operations.MINUS, p.expr0, p.expr1)

    @_('expr TIMES expr')
    def expr(self, p):
        return ast_module.ExpressionBinary(ast_module.Operations.TIMES, p.expr0, p.expr1)

    @_('expr DIVIDE expr')
    def expr(self, p):
        return ast_module.ExpressionBinary(ast_module.Operations.DIVIDE, p.expr0, p.expr1)

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return ast_module.ExpressionNumber(p.NUMBER)

    @_('STRING')
    def expr(self, p):
        return ast_module.ExpressionString(p.STRING)

    @_('TRUE')
    def expr(self, p):
        return ast_module.ExpressionBoolean(p.TRUE)

    @_('FALSE')
    def expr(self, p):
        return ast_module.ExpressionBoolean(p.FALSE)

    @_('NAME')
    def expr(self, p):
        return ast_module.ExpressionVariable(p.NAME)

    # Parameter list (for function definitions)
    @_('NAME')
    def parameters(self, p):
        return [p.NAME]

    @_('NAME COMMA parameters')
    def parameters(self, p):
        return [p.NAME] + p.parameters

    @_('')
    def parameters(self, p):
        return []

    # Argument list (for function calls)
    @_('expr')
    def arguments(self, p):
        return [p.expr]

    @_('expr COMMA arguments')
    def arguments(self, p):
        return [p.expr] + p.arguments

    @_('')
    def arguments(self, p):
        return []
