from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer


class ExplicitConversionsChecker(BaseChecker):
    name = "explicit-conversions"

    msgs = {
        "E9505": (
            "Explicit conversion from int to float required",
            "implicit-numeric-conversion",
            "Used when an integer is assigned to a float without an explicit conversion.",
        ),
    }

    def visit_annassign(self, node: nodes.AnnAssign) -> None:
        if node.value is None:
            return

        if node.annotation.as_string() != "float":
            return

        inferred = safe_infer(node.value)

        if isinstance(inferred, nodes.Const) and type(inferred.value) is int:
            self.add_message(
                "implicit-numeric-conversion",
                node=node.value,
            )


def register(linter):
    linter.register_checker(ExplicitConversionsChecker(linter))
