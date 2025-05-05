from abc import ABC, abstractmethod
from enum import Enum
from components import memory

class Operations(Enum):
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIVIDE = '/'

class ASTNode(ABC):
    @abstractmethod
    def run(self):
        pass

class Expression(ASTNode):
    pass

class ExpressionNumber(Expression):
    def __init__(self, value):
        self.value = value

    def run(self):
        return self.value

    def __str__(self):
        return str(self.value)

class ExpressionString(Expression):
    def __init__(self, value):
        self.value = value

    def run(self):
        return self.value

    def __str__(self):
        return f'"{self.value}"'

class ExpressionBoolean(Expression):
    def __init__(self, value):
        self.value = value  # Python bool

    def run(self):
        return self.value

    def __str__(self):
        return str(self.value)

class ExpressionVariable(Expression):
    def __init__(self, name):
        self.name = name

    def run(self):
        return memory.MEMORY.get(self.name)

    def __str__(self):
        return str(self.name)

class ExpressionBinary(Expression):
    def __init__(self, operation, left, right):
        self.operation = operation  # Operations enum
        self.left = left
        self.right = right

    def run(self):
        left_val = self.left.run()
        right_val = self.right.run()
        if self.operation == Operations.PLUS:
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                return left_val + right_val
            elif isinstance(left_val, str) and isinstance(right_val, str):
                return left_val + right_val
            else:
                raise TypeError(f"Unsupported operand types for +: {type(left_val).__name__} and {type(right_val).__name__}")
        elif self.operation == Operations.MINUS:
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                return left_val - right_val
            else:
                raise TypeError(f"Unsupported operand types for -: {type(left_val).__name__} and {type(right_val).__name__}")
        elif self.operation == Operations.TIMES:
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                return left_val * right_val
            else:
                raise TypeError(f"Unsupported operand types for *: {type(left_val).__name__} and {type(right_val).__name__}")
        elif self.operation == Operations.DIVIDE:
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                return left_val / right_val
            else:
                raise TypeError(f"Unsupported operand types for /: {type(left_val).__name__} and {type(right_val).__name__}")

    def __str__(self):
        return f'({self.left} {self.operation.value} {self.right})'

class ExpressionCompare(Expression):
    def __init__(self, op, left, right):
        self.op = op  # '==' or '!='
        self.left = left
        self.right = right

    def run(self):
        left_val = self.left.run()
        right_val = self.right.run()
        if not isinstance(left_val, (int, float)) or not isinstance(right_val, (int, float)):
            raise TypeError(f"Comparison operands must be numeric, got {type(left_val).__name__} and {type(right_val).__name__}")
        if self.op == '==':
            return left_val == right_val
        elif self.op == '!=':
            return left_val != right_val

    def __str__(self):
        return f'({self.left} {self.op} {self.right})'

class Statement(ASTNode):
    pass

class StatementAssign(Statement):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def run(self):
        value = self.expression.run()
        memory.MEMORY.set(self.name, value)
        return None

    def __str__(self):
        return f'{self.name} = {self.expression}'

class StatementIf(Statement):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block  # StatementBlock
        self.else_block = else_block  # StatementBlock or None

    def run(self):
        cond_val = self.condition.run()
        if not isinstance(cond_val, bool):
            raise TypeError(f"Condition of if must be boolean, got {type(cond_val).__name__}")
        if cond_val:
            self.then_block.run()
        elif self.else_block is not None:
            self.else_block.run()
        return None

    def __str__(self):
        result = f"if {self.condition} then\n"
        for stmt in self.then_block.statements:
            result += f"    {stmt}\n"
        if self.else_block is not None:
            result += "else\n"
            for stmt in self.else_block.statements:
                result += f"    {stmt}\n"
        result += "end"
        return result

class StatementWhile(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body  # StatementBlock

    def run(self):
        while True:
            cond_val = self.condition.run()
            if not isinstance(cond_val, bool):
                raise TypeError(f"Condition of while must be boolean, got {type(cond_val).__name__}")
            if not cond_val:
                break
            self.body.run()
        return None

    def __str__(self):
        result = f"while {self.condition} do\n"
        for stmt in self.body.statements:
            result += f"    {stmt}\n"
        result += "end"
        return result

class StatementFunctionDef(Statement):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters  # list of parameter names
        self.body = body  # StatementBlock

    def run(self):
        memory.MEMORY.define_function(self.name, self)
        return None

    def __str__(self):
        params = ', '.join(self.parameters)
        result = f"def {self.name}({params}) then\n"
        for stmt in self.body.statements:
            result += f"    {stmt}\n"
        result += "end"
        return result

class StatementFunctionCall(Statement):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments  # list of Expression

    def run(self):
        memory.MEMORY.call_function(self.name, self.arguments)
        return None

    def __str__(self):
        args = ', '.join(str(arg) for arg in self.arguments)
        return f'{self.name}({args})'

class StatementPrint(Statement):
    def __init__(self, expression):
        self.expression = expression

    def run(self):
        value = self.expression.run()
        memory.MEMORY.add_output(value)
        return None

    def __str__(self):
        return f'print({self.expression})'

class StatementBlock(Statement):
    def __init__(self, statements):
        self.statements = statements  # list of Statement

    def run(self):
        for stmt in self.statements:
            stmt.run()
        return None

    def __str__(self):
        return 'block'
