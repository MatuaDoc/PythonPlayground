from astroid import nodes
from pylint.checkers import BaseChecker


class PreferGuardChecker(BaseChecker):
    name = "prefer-guard"

    msgs = {
        "W9507": (
            "Prefer an early exit using 'if not (%s)'",
            "prefer-guard",
            "Used when control flow could be simplified using a guard-style early exit.",
        ),
    }

    def visit_if(self, node: nodes.If) -> None:
        if not node.body or len(node.orelse) != 1:
            return

        exit_types = (
            nodes.Return,
            nodes.Raise,
            nodes.Continue,
            nodes.Break,
        )

        if not isinstance(node.orelse[0], exit_types):
            return

        if isinstance(node.body[-1], exit_types):
            return

        self.add_message(
            "prefer-guard",
            node=node,
            args=(node.test.as_string(),),
        )


def register(linter):
    linter.register_checker(PreferGuardChecker(linter))
