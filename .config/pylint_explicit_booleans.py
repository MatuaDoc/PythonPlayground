from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer


class ExplicitBooleansChecker(BaseChecker):
    name = "explicit-booleans"

    msgs = {
        "E9506": (
            "Condition '%s' must explicitly evaluate to a bool",
            "non-boolean-condition",
            "Used when a condition relies on implicit truthiness.",
        ),
    }

    def check_condition(self, node):
        if isinstance(node, nodes.BoolOp):
            for value in node.values:
                self.check_condition(value)
            return

        if isinstance(node, nodes.UnaryOp) and node.op == "not":
            self.check_condition(node.operand)
            return

        if isinstance(node, nodes.Compare):
            return

        inferred = safe_infer(node)

        if inferred is None:
            return

        if inferred.pytype() == "builtins.bool":
            return

        self.add_message(
            "non-boolean-condition",
            node=node,
            args=(node.as_string(),),
        )

    def visit_if(self, node):
        self.check_condition(node.test)

    def visit_while(self, node):
        self.check_condition(node.test)

    def visit_ifexp(self, node):
        self.check_condition(node.test)

    def visit_assert(self, node):
        self.check_condition(node.test)

    def visit_comprehension(self, node):
        for condition in node.ifs:
            self.check_condition(condition)

    def visit_matchcase(self, node):
        if node.guard is not None:
            self.check_condition(node.guard)


def register(linter):
    linter.register_checker(ExplicitBooleansChecker(linter))
