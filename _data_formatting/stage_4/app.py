from json import load
from re import sub
from typing import (Any, Callable, Literal, TypeAlias, TypedDict, cast,
                    get_args, get_type_hints)

EMPTY_STRING: TypeAlias = Literal[""]
ANCIENT: TypeAlias = Literal["Ancient"]


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
        elements = cast(list[ParsedElement], load(file_data))

    type_hints = get_type_hints(
        ParsedElement
    )

    optionals = [
        key for key, hint in type_hints.items() if EMPTY_STRING in get_args(hint)
    ]

    with open("./_out.txt", "w") as output:
        for element in elements:
            output.write(to_rust_syntax(
                element, optionals, type_hints) + "\n\n")

    enum_types = [
        key for key, value in type_hints.items() if value == str
    ]

    with open("./_out2.txt", "w") as output2:
        for type_name in enum_types:
            output2.write(strings_to_rust_enum(
                to_pascal_case(type_name), list(dict.fromkeys(
                    [element[type_name] for element in elements]
                ))) + "\n\n")


def strings_to_rust_enum(name: str, items: list[str]) -> str:
    return f"enum {name} {{ {', '.join(items)} }}"


def to_rust_syntax(element: ParsedElement, optionals: list[str], type_hints: dict[str, Any]) -> str:
    ELEMENT_STRUCT_TEMPLATE = """
    pub const {uppercase_name}: &'static Element = &Element {{
        atomic_number: {atomic_number},
        symbol: Symbol::{symbol},
        name: Name::{name},
        atomic_mass: {atomic_mass},
        cpk_hex_color: {cpk_hex_color},
        electron_configuration: {electron_configuration},
        electronegativity: {electronegativity},
        atomic_radius: {atomic_radius},
        ionization_energy: {ionization_energy},
        electron_affinity: {electron_affinity},
        oxidation_states: {oxidation_states},
        standard_state: MatterState::{standard_state},
        melting_point: {melting_point},
        boiling_point: {boiling_point},
        density: {density},
        group_block: GroupBlock::{group_block},
        year_discovered: YearDiscovered::{year_discovered},
    }};
    """.strip()

    fill_ins = cast(dict[str, str], element.copy())

    fill_ins["uppercase_name"] = element["name"].upper()

    def format_optional(optional: Any, formatter: Callable[[Any], Any]):
        return formatter(optional) if optional != "" else ""

    def remove_extra_space(text: str) -> str:
        return " ".join(text.split())

    def format_hex_color(color: Color) -> str:
        return remove_extra_space("""
        Color {{
            red: {red},
            green: {green},
            blue: {blue}
        }}
        """).format(
            **color
        )

    fill_ins["cpk_hex_color"] = format_optional(
        element["cpk_hex_color"], format_hex_color
    )

    def no_quote_list(items: list[Any]) -> str:
        return f"&[{', '.join([f'{item}' for item in items])}]"

    def format_configuration_part(part: ElectronConfigurationPart):
        return remove_extra_space("""
        ElectronConfigurationPart {{
            energy_level: {energy_level},
            orbital: Orbital::{orbital},
            electrons: {electrons}
        }}
        """).format(
            energy_level=part["energy_level"],
            orbital=part["orbital"].upper(),
            electrons=part["electrons"]
        )

    fill_ins["electron_configuration"] = no_quote_list([
        format_configuration_part(part) for part in element["electron_configuration"]
    ])

    def format_year_discovered(year: int | ANCIENT) -> str:
        return f"Year({year})" if year != "Ancient" else "Ancient"

    fill_ins["year_discovered"] = format_year_discovered(
        element["year_discovered"])

    fill_ins["oxidation_states"] = format_optional(
        element["oxidation_states"], no_quote_list)

    for key, value in type_hints.items():
        if value == float or value == float | EMPTY_STRING:
            fill_ins[key] = format_optional(fill_ins[key], float)

    for optional in optionals:
        fill_in = fill_ins[optional]
        fill_ins[optional] = f"Some({fill_in})" if fill_in != "" else "None"

    return ELEMENT_STRUCT_TEMPLATE.format(** fill_ins)


def to_pascal_case(text: str) -> str:
    return capitalize(sub(r"[^a-zA-Z]([a-z])", lambda match: capitalize(match.group(1)), text))


def capitalize(text: str):
    return text[0].capitalize() + text[1:]


if __name__ == "__main__":
    main()
