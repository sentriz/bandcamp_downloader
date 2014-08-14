"""
Simple JavaScript/ECMAScript object literal reader

Copyright (c) 2013 darkf
Licensed under the terms of the WTFPL
"""

from slimit.parser import Parser
from slimit.visitors.nodevisitor import ASTVisitor
import slimit.ast as ast

def read_js_object(code):

    def visit(node):
        if isinstance(node, ast.Program):
            dict = {}
            for child in node:
                if not isinstance(child, ast.VarStatement):
                    raise ValueError("All statements should be var statements")
                key, val = visit(child)
                dict[key] = val
            return dict
        elif isinstance(node, ast.VarStatement):
            return visit(node.children()[0])
        elif isinstance(node, ast.VarDecl):
            return (visit(node.identifier), visit(node.initializer))
        elif isinstance(node, ast.Object):
            d = {}
            for property in node:
                key = visit(property.left)
                value = visit(property.right)
                d[key] = value
            return d
        elif isinstance(node, ast.BinOp):
            # simple constant folding
            if node.op == '+':
                if isinstance(node.left, ast.String) and isinstance(node.right, ast.String):
                    return visit(node.left) + visit(node.right)
                elif isinstance(node.left, ast.Number) and isinstance(node.right, ast.Number):
                    return visit(node.left) + visit(node.right)
                else:
                    raise ValueError("Cannot + on anything other than two literals")
            else:
                raise ValueError("Cannot do operator \"{}\"".format(node.op))
        elif isinstance(node, ast.String):
            return node.value.strip('"').strip("'")
        elif isinstance(node, ast.Array):
            return [visit(x) for x in node]
        # elif isinstance(node, ast.Number) or isinstance(node, ast.Identifier) or isinstance(node, ast.Boolean) or isinstance(node, ast.Null):
        #elif any([isinstance(node, getattr(ast, type)) for type in ["Number", "Identifier", "Boolean", "Null"]]):
        #    return node.value
        else:
            raise Exception("Unhandled node: {}".format(node))
            
    return visit(Parser().parse(code))

# testing
if __name__ == "__main__":
    JS = """
    var foo = {x: 10, y: "hi " + "there!"};
    var bar = {derp: ["herp", "it", "up", "forever"]};
    """
    print(read_js_object(JS))