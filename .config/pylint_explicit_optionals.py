from astroid import nodes
from pylint.checkers import BaseChecker


class ExplicitOptionalsChecker(BaseChecker):
    name = "explicit-optionals"

    msgs = {
        "E9504": (
            "Use '%s' for an explicit optional-value check",
            "implicit-optional-check",
            "Used when an optional variable is checked through implicit truthiness.",
        ),
    }

    def is_optional(self, annotation):
        if isinstance(annotation, nodes.BinOp):
            if annotation.op == "|":
                return self.is_optional(annotation.left) or self.is_optional(annotation.right)

        if isinstance(annotation, nodes.Const):
            return annotation.value is None

        if isinstance(annotation, nodes.Subscript):
            return annotation.value.as_string() in {
                "Optional",
                "typing.Optional",
            }

        return False

    def check_condition(self, node):
        if isinstance(node, nodes.BoolOp):
            for value in node.values:
                self.check_condition(value)
            return

        negated = False

        if isinstance(node, nodes.UnaryOp) and node.op == "not":
            negated = True
            node = node.operand

        if not isinstance(node, nodes.Name):
            return

        scope, _ = node.lookup(node.name)

        for definition in scope.locals.get(node.name, []):
            parent = definition.parent

            if not isinstance(parent, nodes.AnnAssign):
                continue

            if not self.is_optional(parent.annotation):
                continue

            comparison = "is None" if negated else "is not None"

            self.add_message(
                "implicit-optional-check",
                node=node,
                args=(f"{node.name} {comparison}",),
            )
            return

    def visit_if(self, node):
        self.check_condition(node.test)

    def visit_while(self, node):
        self.check_condition(node.test)

    def visit_ifexp(self, node):
        self.check_condition(node.test)

    def visit_assert(self, node):
        self.check_condition(node.test)


def register(linter):
    linter.register_checker(ExplicitOptionalsChecker(linter))
