from asyncio import (WindowsSelectorEventLoopPolicy, create_task, gather, run,
                     set_event_loop_policy)
from json import dump, load
from re import Match, sub
from typing import Any, Callable, Iterable, Tuple, TypeVar

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag


async def main():
    async with ClientSession() as client:
        def wait_for_element(atomic_number: int):
            return create_task(get_element_data(atomic_number, client))

        fill_ins = await gather(*[wait_for_element(atomic_number) for atomic_number in range(1, 118 + 1)])

        with open("./_in.json", "r") as elements_file:
            elements = fill_in(load(elements_file), fill_ins)

            with open("./_out.json", "w") as output:
                dump(elements, output, indent=3)


def fill_in(elements: list[dict[str, Any]], fill_ins: list[dict[str, Any]]):
    for fill_in, element in zip(fill_ins, elements):
        for key, value in element.items():
            if value != "":
                continue

            if key not in fill_in:
                continue

            fill_in_value = fill_in[key]

            if fill_in_value == "":
                continue

            element[key] = fill_in_value

            print(f"{element['name']} - {key}: {fill_in_value}")

    return elements


async def get_element_data(atomic_number: int, client: ClientSession):
    web_data = await get_web_data(atomic_number, client)
    element = parse_web_data(web_data)

    return element


def parse_web_data(web_data: list[list[str]]) -> dict[str, Any]:
    key_replacements = {
        "State at 20°C": "standard_state",
        "Density (g cm−3)": "density",
        "Relative atomic mass": "atomic_mass"
    }

    element = {}

    for row in web_data:
        for key, value in grouped(row, 2):
            new_key = to_snake_case(key_replacements.get(key, key))
            element[new_key] = remove_parens(value)

    return convert_to_types(element)


def convert_to_types(element: dict[str, Any]):
    def temperature_parser(text): return float(
        text.split(",")[2].strip("K").strip(" "))

    def mass_parser(text): return float(text.strip("[]"))

    def empty_unknown(converter: Callable[[str], Any]):
        def inner(text: str):
            if text != "Unknown":
                try:
                    return converter(text)
                except ValueError:
                    return text

            return ""
        return inner

    value_parsers = {
        "boiling_point": temperature_parser,
        "melting_point": temperature_parser,
        "atomic_number": int,
        "density": float,
        "group": int,
        "period": int,
        "atomic_mass": mass_parser
    }

    for key, parser in value_parsers.items():
        element[key] = empty_unknown(parser)(element[key])

    return element


async def get_web_data(atomic_number: int, client: ClientSession):
    ELEMENT_PAGE_URL = f"https://www.rsc.org/periodic-table/element/{atomic_number}/"

    page_data: BeautifulSoup

    async with client.get(ELEMENT_PAGE_URL) as response:
        page_data = BeautifulSoup(await response.text(), features="html.parser")

    property_table = page_data.select_one(
        "table[class=element_hover_table_ca] > tbody"
    )

    assert property_table != None, f"Sorry, we couldn't get a table for the element with the atomic number '{atomic_number}'"

    return parse_table(property_table)[:-1]


def parse_table(table: Tag) -> list[list[str]]:
    parsed_table: list[list[str]] = []

    rows = table.select("tr")
    for row in rows:
        columns = [
            column.text.strip() for column in row.select("td")
        ]

        parsed_table.append(columns)

    return parsed_table


def to_snake_case(text: str) -> str:
    def replacer(match: Match):
        first_group = match.group(1)
        return f"_{first_group[1]}{match.group(2)}"

    return sub(r"(.[A-Z]| [a-z])([a-z])", replacer, text).lower()


def remove_parens(text: str) -> str:
    return sub(r"\s+\(.*\)$", "", text)


T = TypeVar("T")


def grouped(iterable: Iterable[T], group_size: int) -> Iterable[Tuple[T, ...]]:
    return zip(*[iter(iterable)] * group_size)


if __name__ == "__main__":
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    run(main())
