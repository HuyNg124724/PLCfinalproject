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
        self.scopes = [{}]  # stack of variable scopes (global first)
        self.functions = {}  # map function names to function def objects
        self.output = []

    def get(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise NameError(f"Variable '{name}' is not defined")

    def set(self, name, value):
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
        if name not in self.functions:
            raise NameError(f"Function '{name}' is not defined")

        func_def = self.functions[name]

        if len(arguments) != len(func_def.parameters):
            raise TypeError(f"Function '{name}' expects {len(func_def.parameters)} arguments, got {len(arguments)}")

        # Evaluate argument values in caller's scope
        arg_values = [arg.run() for arg in arguments]

        # New local scope for this call
        local_scope = dict(zip(func_def.parameters, arg_values))
        self.scopes.append(local_scope)

        func_def.body.run()

        self.scopes.pop()


MEMORY = Memory()
