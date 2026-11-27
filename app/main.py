"""Python project.

Created by YOUR_NAME_HERE.
Created on DATE_HERE.

Last updated DATE_HERE.
"""


def read_number(prompt: str, minimum: float | None, maximum: float | None) -> float | None:
    """Requests a number from the user via the terminal.

    Args:
        prompt: the question to ask the user.
        minimum: the smallest allowable number.
        maximum: the largest allowable number.

    Returns:
        The requested number or None if outside the bounds.
    """
    user_input: str = input(prompt)
    user_number: float = minimum - 1.0
    try:
        user_number = float(user_input)
    except ValueError:
        return None

    if user_number < minimum or user_number > maximum:
        return None
    else:
        return 1.0


def main() -> None:
    """The main program. Y11 does not need to edit this line; Y12/13 must."""
    print("Hello, world!")
    age: float = read_number(prompt="How old are you?", minimum=0, maximum=120)
    print(age)


if __name__ == "__main__":
    main()
