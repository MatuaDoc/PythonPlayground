from astroid import nodes
from pylint.checkers import BaseChecker


class RequiredAnnotationsChecker(BaseChecker):
    name = "required-annotations"

    msgs = {
        "E9501": (
            "Variable '%s' requires a type annotation",
            "missing-variable-annotation",
            "Used when a variable is assigned without an explicit type annotation.",
        ),
    }

    def visit_assign(self, node: nodes.Assign) -> None:
        for target in node.targets:
            if isinstance(target, nodes.AssignName):
                self.check_variable(target)

    def check_variable(self, target: nodes.AssignName) -> None:
        name = target.name
        scope = target.scope()

        if name == "_":
            return

        for definition in scope.locals.get(name, []):
            if definition.lineno >= target.lineno:
                continue

            parent = definition.parent

            if isinstance(parent, nodes.AnnAssign):
                return

            if isinstance(
                parent,
                (nodes.Arguments, nodes.For, nodes.AsyncFor),
            ):
                return

        self.add_message(
            "missing-variable-annotation",
            node=target,
            args=(name,),
        )


def register(linter):
    linter.register_checker(RequiredAnnotationsChecker(linter))
