def singleton(cls):
    instances = {}
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance

@singleton
class Memory:
    def __init__(self):
        self.scopes = [{}]  # list of dicts, first is global scope
        self.functions = {}
        self.output = []

    def get(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise NameError(f"Variable '{name}' is not defined")

    def set(self, name, value):
        # set variable in current (top) scope
        self.scopes[-1][name] = value

    def add_output(self, value):
        self.output.append(str(value))

    def get_output(self):
        return '\n'.join(self.output)

    def clear(self):
        self.scopes = [{}]
        self.functions = {}
        self.output = []

    def define_function(self, name, func_def):
        self.functions[name] = func_def

    def call_function(self, name, arguments):
        # Built-in print as function
        if name == 'print':
            for arg in arguments:
                value = arg.run()
                self.add_output(value)
            return None
        if name not in self.functions:
            raise NameError(f"Function '{name}' is not defined")
        func_def = self.functions[name]
        args_values = [arg.run() for arg in arguments]
        if len(args_values) != len(func_def.parameters):
            raise TypeError(f"Function '{name}' expects {len(func_def.parameters)} arguments")
        # Push new scope for function parameters
        local_scope = {}
        for param_name, arg_val in zip(func_def.parameters, args_values):
            local_scope[param_name] = arg_val
        self.scopes.append(local_scope)
        func_def.body.run()
        # Pop the function scope
        self.scopes.pop()
        return None

# Global memory instance
MEMORY = Memory()