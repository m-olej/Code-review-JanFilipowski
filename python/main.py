# Z podanego zbioru danych wyselekcjonuj 5 o największej wartości na jednostkę, znając kategorię obiektu
# Dane znajdują się w folderze "dane" w pliku "zbiór_wejściowy.json" oraz "kategorie.json"
# Wynik przedstaw w czytelnej formie na standardowym wyjściu

from json import load


def ounce(x):

    match x[-1]:
        case "g":
            return float(x[:-1].replace(",", ".")) * 0.0352739
        case "t":
            return float(x[:-2].replace(",", ".")) * 0.0070548
        case _:
            raise ValueError("Invalid unit")


def get_categories(categories_filepath):
    """
    Read categories from json file

    Args:
        categories_filepath (str): path to json file with categories
    Returns:
        dict[tuple, float]: dictionary with prices per ounce for each category purity tuple
    """
    price_per_ounce = {}

    with open(categories_filepath, "r", encoding="utf8") as file:
        data = load(file)
    for product in data:
        price_per_ounce[(product["Typ"], product["Czystość"])] = float(
            product["Wartość za uncję (USD)"]
        )

    return price_per_ounce


def analyze(data, price_per_ounce):
    """
    Analyze data and calculate value for each object

    Args:
        data (list[dict]): list of objects
        price_per_ounce (dict[tuple, float]): dictionary with prices per ounce for each category purity tuple
    Returns:
        list[tuple]: list of tuples with object index and its value
    """

    object_values = []
    for i, gemstone in enumerate(data):
        try:
            object_values.append(
                (
                    i,
                    round(
                        ounce(gemstone["Masa"])
                        * price_per_ounce[(gemstone["Typ"], gemstone["Czystość"])],
                        2,
                    ),
                )
            )
        except KeyError:
            continue

    return object_values


def pretty_print(object_values, data, top=5):

    spacing = "{:<5} {:<10} {:<10} {:<10} {:<10} {:<10} {:<15} {:<20}"

    # print header
    print(
        spacing.format(
            "Lp.",
            "Typ",
            "Masa",
            "Czystość",
            "Wartość",
            "Barwa",
            "Pochodzenie",
            "Właściciel",
        )
    )

    # print top n objects
    for k, i in enumerate(
        reversed([i[0] for i in sorted(object_values, key=lambda x: x[1])[-top:]])
    ):
        item = dict(enumerate(data))[i]
        print(
            spacing.format(
                k + 1,
                item["Typ"],
                item["Masa"],
                item["Czystość"],
                dict(object_values)[i],
                item["Barwa"],
                item["Pochodzenie"],
                item["Właściciel"],
            )
        )


def main():

    DATA_FILE = "../dane/zbiór_wejściowy.json"
    CATEGORIES_FILE = "../dane/kategorie.json"

    # Read data
    with open(DATA_FILE, "r", encoding="utf8") as file:
        data = load(file)

    # Read categories
    price_per_pounce = get_categories(CATEGORIES_FILE)

    # Analyze data
    analyzed_data = analyze(data, price_per_pounce)

    # Print results
    pretty_print(analyzed_data, data, 10)


if __name__ == "__main__":
    main()
