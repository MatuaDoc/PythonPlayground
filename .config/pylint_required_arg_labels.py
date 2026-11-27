from pathlib import Path

from astroid import bases, nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer


class RequiredArgumentLabelsChecker(BaseChecker):
    name = "required-argument-labels"

    msgs = {
        "E9502": (
            "Argument '%s' must be passed by name",
            "missing-argument-label",
            "Used when an argument is passed positionally instead of by name.",
        ),
    }

    def visit_call(self, node: nodes.Call) -> None:
        if not node.args:
            return

        function = safe_infer(node.func)
        offset = 0

        if isinstance(function, bases.BoundMethod):
            offset = function.implicit_parameters()

        while isinstance(function, bases.UnboundMethod):
            function = function._proxied

        if not isinstance(function, nodes.FunctionDef):
            return

        module = function.root()

        if not module.file:
            return

        path = Path(module.file).resolve()

        if not path.is_relative_to(Path.cwd()):
            return

        if any(part in {".venv", "venv", "site-packages"} for part in path.parts):
            return

        positional_only = function.args.posonlyargs or []
        parameters = positional_only + (function.args.args or [])

        for index, argument in enumerate(node.args):
            if isinstance(argument, nodes.Starred):
                break

            position = index + offset

            if position < len(positional_only):
                continue

            if position >= len(parameters):
                break

            self.add_message(
                "missing-argument-label",
                node=argument,
                args=(parameters[position].name,),
            )


def register(linter):
    linter.register_checker(RequiredArgumentLabelsChecker(linter))
