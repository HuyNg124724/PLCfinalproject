from sly import Parser
from components.lexica import MyLexer
from components.ast import statement as ast_module

class MyParser(Parser):
    tokens = MyLexer.tokens

    precedence = (
        ('left', 'EQEQ', 'NOTEQ'),
        ('left', 'LT', 'LE', 'GT', 'GE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD'),
    )

    @_('statements')
    def program(self, p):
        return p.statements

    @_('stmt')
    def statements(self, p):
        return [p.stmt]

    @_('stmt statements')
    def statements(self, p):
        return [p.stmt] + p.statements

    @_('NAME EQUAL expr')
    def stmt(self, p):
        return ast_module.StatementAssign(p.NAME, p.expr)

    @_('IF expr THEN statements END')
    def stmt(self, p):
        return ast_module.StatementIf(p.expr, ast_module.StatementBlock(p.statements))

    @_('IF expr THEN statements ELSE statements END')
    def stmt(self, p):
        return ast_module.StatementIf(p.expr, ast_module.StatementBlock(p.statements0), ast_module.StatementBlock(p.statements1))

    @_('WHILE expr DO statements END')
    def stmt(self, p):
        return ast_module.StatementWhile(p.expr, ast_module.StatementBlock(p.statements))

    @_('DEF NAME LPAREN parameters RPAREN THEN statements END')
    def stmt(self, p):
        return ast_module.StatementFunctionDef(p.NAME, p.parameters, ast_module.StatementBlock(p.statements))

    @_('PRINT LPAREN expr RPAREN')
    def stmt(self, p):
        return ast_module.StatementPrint(p.expr)

    @_('NAME LPAREN arguments RPAREN')
    def stmt(self, p):
        return ast_module.StatementFunctionCall(p.NAME, p.arguments)

    @_('expr EQEQ expr')
    def expr(self, p):
        return ast_module.ExpressionCompare('==', p.expr0, p.expr1)

    @_('expr NOTEQ expr')
    def expr(self, p):
        return ast_module.ExpressionCompare('!=', p.expr0, p.expr1)

    @_('expr LT expr')
    def expr(self, p):
        return ast_module.ExpressionBinary(ast_module.Operations.LT, p.expr0, p.expr1)

    @_('expr LE expr')
    def expr(self, p):
        return ast_module.ExpressionBinary(ast_module.Operations.LE, p.expr0, p.expr1)

    @_('expr GT expr')
    def expr(self, p):
        return ast_module.ExpressionBinary(ast_module.Operations.GT, p.expr0, p.expr1)

    @_('expr GE expr')
    def expr(self, p):
        return ast_module.ExpressionBinary(ast_module.Operations.GE, p.expr0, p.expr1)

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

    @_('NAME')
    def parameters(self, p):
        return [p.NAME]

    @_('NAME COMMA parameters')
    def parameters(self, p):
        return [p.NAME] + p.parameters

    @_('')
    def parameters(self, p):
        return []

    @_('expr')
    def arguments(self, p):
        return [p.expr]

    @_('expr COMMA arguments')
    def arguments(self, p):
        return [p.expr] + p.arguments
    
    @_('expr MOD expr')
    def expr(self, p):
        return ast_module.ExpressionBinary(ast_module.Operations.MOD, p.expr0, p.expr1)

    @_('')
    def arguments(self, p):
        return []
