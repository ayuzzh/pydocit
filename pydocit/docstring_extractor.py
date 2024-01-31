import ast


class Visitor(ast.NodeVisitor):
    """The parsed source code of the file should be passed to extract
    docstrings and functions and class definitions."""

    def __init__(self):
        self.classes = {}
        self.functions = {}
        self.docstring = {}
        self.imports = []

        self.current_class = None
        self.current_function = None

    def visit_ClassDef(self, node):
        bases = []
        for i in node.bases:
            bases.append(ast.unparse(i))

        self.classes[node.name] = {
            "name": node.name,
            "methods": {},
            "bases": bases,
            "docstring": ast.get_docstring(node),
            "source": ast.unparse(node),
        }
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        returns = None
        if node.returns is not None:
            returns = ast.unparse(node.returns)

        args = {}
        list_of_args = []

        for i in node.args.args:
            _source = ast.unparse(i)

            annotation = None
            if i.annotation is not None:
                annotation = ast.unparse(i.annotation)

            type_comment = None
            if i.type_comment is not None:
                type_comment = ast.unparse(i.type_comment)

            list_of_args.append(i.arg)
            args[i.arg] = {
                "name": i.arg,
                "annotations": annotation,
                "default": None,
                "type_comment": type_comment,
                "def_source": _source,
            }

        for m, n in zip(reversed(node.args.defaults), reversed(list_of_args)):
            default = None
            if m is not None:
                default = ast.unparse(m)
            args[n]["default"] = default

        if self.current_function is None:
            if self.current_class:
                self.classes[self.current_class]["methods"][node.name] = {
                    "args": args,
                    "docstring": ast.get_docstring(node),
                    "returns": returns,
                    "source": ast.unparse(node),
                }
            else:
                self.functions[node.name] = {
                    "args": args,
                    "docstring": ast.get_docstring(node),
                    "returns": returns,
                    "source": ast.unparse(node),
                }

        # For wrapping up the function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = None

    def visit_Import(self, node):
        for i in node.names:
            self.imports.append(i.name)

    def visit_ImportFrom(self, node):
        for i in node.names:
            self.imports.append(f"{node.module}.{i.name}")

    def call_visit(self, tree):
        self.docstring = ast.get_docstring(tree)
        super().visit(tree)

    def out(self):
        return {
            "functions": self.functions,
            "classes": self.classes,
            "docstring": self.docstring,
            "imports": self.imports,
        }
