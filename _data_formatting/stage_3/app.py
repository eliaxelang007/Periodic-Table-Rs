from json import dump, load
from pathlib import Path
from re import findall, sub
from sys import argv
from typing import Literal, Tuple, TypeAlias, TypedDict, cast

JSON: TypeAlias = dict[str,
                       "JSON"] | list["JSON"] | str | int | float | bool | None

EMPTY_STRING: TypeAlias = Literal[""]
ANCIENT: TypeAlias = Literal["Ancient"]


class Element(TypedDict):
    atomic_number: int
    symbol: str
    name: str
    atomic_mass: float
    cpk_hex_color: str | EMPTY_STRING
    electron_configuration: str
    electronegativity: float | EMPTY_STRING
    atomic_radius: int | EMPTY_STRING
    ionization_energy: float | EMPTY_STRING
    electron_affinity: float | EMPTY_STRING
    oxidation_states: list[int] | EMPTY_STRING
    standard_state: str
    melting_point: float | EMPTY_STRING
    boiling_point: float | EMPTY_STRING
    density: float | EMPTY_STRING
    group_block: str
    year_discovered: int | ANCIENT


class ElectronConfigurationPart(TypedDict):
    energy_level: int
    orbital: str
    electrons: int


class Color(TypedDict):
    red: int
    green: int
    blue: int


class ParsedElement(TypedDict):
    atomic_number: int
    symbol: str
    name: str
    atomic_mass: float
    cpk_hex_color: Color | EMPTY_STRING
    electron_configuration: list[ElectronConfigurationPart]
    electronegativity: float | EMPTY_STRING
    atomic_radius: int | EMPTY_STRING
    ionization_energy: float | EMPTY_STRING
    electron_affinity: float | EMPTY_STRING
    oxidation_states: list[int] | EMPTY_STRING
    standard_state: str
    melting_point: float | EMPTY_STRING
    boiling_point: float | EMPTY_STRING
    density: float | EMPTY_STRING
    group_block: str
    year_discovered: int | ANCIENT


def main():
    with open("./_in.json", "r") as file_data:
        unformatted_elements = load(file_data)

    formatted_elements = format_elements(
        cast(list[Element], unformatted_elements))

    with open("./_out.json", "w") as file_data:
        dump(formatted_elements, file_data, indent=3)


def format_elements(unformatted_elements: list[Element]) -> list[ParsedElement]:
    formatted_elements = []

    for element in unformatted_elements:
        formatted_element: ParsedElement = cast(ParsedElement, element.copy())

        formatted_element["electron_configuration"] = parse_electron_configuration(
            element["symbol"], element["electron_configuration"])

        formatted_element["cpk_hex_color"] = hex_to_color(
            element["cpk_hex_color"])

        formatted_element["group_block"] = to_pascal_case(
            element["group_block"])

        formatted_element["standard_state"] = l_trim(
            element["standard_state"], "Expected to be a ")

        formatted_elements.append(
            formatted_element
        )

    return formatted_elements


ElectronConfiguration: TypeAlias = list[ElectronConfigurationPart]

cache: dict[str, ElectronConfiguration] = {}


def parse_electron_configuration(symbol: str, text: str) -> ElectronConfiguration:
    parts = findall(r"(\d+)([spdf])(\d+)", text)

    def from_tuple(_tuple: Tuple[str, str, str]) -> ElectronConfigurationPart:
        return ElectronConfigurationPart(
            energy_level=int(_tuple[0]),
            orbital=_tuple[1],
            electrons=int(_tuple[2])
        )

    electron_configuration = [from_tuple(part) for part in parts]

    shortcut = findall(r"\[(.+)\]", text)

    if len(shortcut) != 0:
        electron_configuration = [*cache[shortcut[0]], *electron_configuration]

    cache[symbol] = electron_configuration

    return electron_configuration


def l_trim(text: str, pattern: str):
    if text.startswith(pattern):
        return text[len(pattern):]
    return text


def to_pascal_case(text: str) -> str:
    return sub(r"\W(\w)", lambda match: match.group(1).title(), text)


def hex_to_color(hex: str | EMPTY_STRING) -> Color | EMPTY_STRING:
    if hex == "":
        return ""

    hex = hex.zfill(6)

    red = int(hex[:2], 16)
    green = int(hex[2:4], 16)
    blue = int(hex[4:6], 16)

    return Color(red=red, green=green, blue=blue)


if __name__ == "__main__":
    main()
