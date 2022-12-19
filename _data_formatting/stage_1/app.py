from json import dump, load
from math import floor
from pathlib import Path
from re import Match, sub
from sys import argv
from typing import Any, TypeAlias, TypedDict, TypeVar, cast, get_type_hints

T = TypeVar("T")
Option: TypeAlias

JSON: TypeAlias = dict[str,
                       "JSON"] | list["JSON"] | str | int | float | bool | None


class Table(TypedDict):
    Columns: dict[str, list[str]]
    Row: list[dict[str, list[str]]]


class UnformattedElements(TypedDict):
    Table: Table


class Element(TypedDict):
    atomic_number: int
    symbol: str
    name: str
    atomic_mass: float
    cpk_hex_color: str
    electron_configuration: str
    electronegativity: float
    atomic_radius: int
    ionization_energy: float
    electron_affinity: float
    oxidation_states: list[int]
    standard_state: str
    melting_point: float
    boiling_point: float
    density: float
    group_block: str
    year_discovered: int


def main():
    with open("./_in.json", "r") as file_data:
        unformatted_elements: UnformattedElements = load(file_data)

    formatted_elements = format_elements(unformatted_elements)

    with open("./_out.json", "w") as file_data:
        dump(formatted_elements, file_data, indent=3)


def format_elements(unformatted_elements: UnformattedElements) -> JSON:
    table = unformatted_elements["Table"]
    columns = [to_snake_case(column) for column in table["Columns"]["Column"]]

    formatted_elements: JSON = []

    elements = [row["Cell"] for row in table["Row"]]

    converters = {
        int: try_num,
        float: try_num,
        list[int]: lambda text: [int(part) for part in text.split(", ")],
        str: lambda x: x
    }

    type_hints = get_type_hints(Element)

    for element in elements:
        formatted_element: dict[str, Any] = {}

        for key, value in zip(columns, element):
            if value != "":
                converted = converters[type_hints[key]](value)
            else:
                converted = ""

            formatted_element[key] = converted

        formatted_elements.append(formatted_element)

    return formatted_elements


def try_num(text: str) -> str | float | int:
    try:
        output = float(text)
        floored = floor(output)

        if floored == output:
            return int(floored)

        return output
    except ValueError:
        return text


def to_snake_case(text: str) -> str:
    def replacer(match: Match):
        return f"{match.group(1)}_{match.group(2).lower()}{match.group(3)}"

    return sub(r"(.)([A-Z])([a-z])", replacer, text).lower()


if __name__ == "__main__":
    main()
