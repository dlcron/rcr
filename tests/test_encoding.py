from random import shuffle

import pytest
from rcr.encoders import encode


def generate_from_counts(values: dict[str, int]) -> list[str]:
    """Generate a list of commands from a dictionary of counts."""
    commands = []
    for name, count in values.items():
        commands.extend([name] * count)
    shuffle(commands)
    return commands


@pytest.mark.parametrize(
    ("commands", "result"), [
        ([], {}),
        (["a"], {"a": "0"}),
        (["a", "b", "b"], {"a": "0", "b": "1"}),
        (["a"] + ["b"] * 2 + ["c"] * 1000, {"c": "1", "b": "01", "a": "00"}),
        (
            generate_from_counts(
                {"a": 1, "b": 2, "c": 4, "d": 8, "e": 16, "f": 32},
            ),
            {"f": "1", "e": "01", "d": "001", "c": "0001", "b": "00001", "a": "00000"},
        ),
    ],
)
def test_encode(commands: list[str], result: dict[str, str]) -> None:
    assert encode(commands) == result
