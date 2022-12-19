from json import dump, load
from sys import argv


def main():
    assert len(
        argv) == 2 + 1, "Usage: python ./app.py [element_attribute, modifier]"

    """
    Usages:
    python app.py name "'{attribute}'.upper()"
    """

    arguments = argv[1:]

    element_attribute = arguments[0]
    modifier = arguments[1]

    with open("./_final.json") as final_element_file:
        final_elements = load(final_element_file)

        with open(f"./{element_attribute}.json", "w") as output_file:
            dump([
                eval(modifier.format(attribute=attribute)) for attribute in [
                    element[element_attribute] for element in final_elements
                ]
            ], output_file)


if __name__ == "__main__":
    main()
