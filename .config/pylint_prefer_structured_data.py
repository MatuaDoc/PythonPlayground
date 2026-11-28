from astroid import nodes
from pylint.checkers import BaseChecker


class PreferStructuredDataChecker(BaseChecker):
    name = "prefer-structured-data"

    msgs = {
        "W9508": (
            "Consider using a dataclass for '%s'",
            "prefer-structured-data",
            "Used when a dictionary appears to represent a fixed data structure.",
        ),
    }

    def visit_annassign(self, node: nodes.AnnAssign) -> None:
        if not isinstance(node.target, nodes.AssignName):
            return

        if not isinstance(node.value, nodes.Dict):
            return

        annotation = node.annotation

        if not isinstance(annotation, nodes.Subscript):
            return

        if annotation.value.as_string() not in {"dict", "Dict", "typing.Dict"}:
            return

        if not isinstance(annotation.slice, nodes.Tuple):
            return

        parameters = annotation.slice.elts

        if len(parameters) != 2:
            return

        if parameters[0].as_string() != "str":
            return

        value_type = parameters[1].as_string()

        if "|" not in value_type and value_type != "object":
            return

        items = node.value.items

        if len(items) < 2:
            return

        for key, _ in items:
            if not isinstance(key, nodes.Const):
                return

            if not isinstance(key.value, str):
                return

            if not key.value.isidentifier():
                return

        self.add_message(
            "prefer-structured-data",
            node=node.target,
            args=(node.target.name,),
        )


def register(linter):
    linter.register_checker(PreferStructuredDataChecker(linter))
