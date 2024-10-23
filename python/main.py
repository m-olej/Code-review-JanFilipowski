# Z podanego zbioru danych wyselekcjonuj 5 o największej wartości na jednostkę, znając kategorię obiektu
# Dane znajdują się w folderze "dane" w pliku "zbiór_wejściowy.json" oraz "kategorie.json"
# Wynik przedstaw w czytelnej formie na standardowym wyjściu

from json import load

price_per_ounce = {}

with open('../dane/kategorie.json', 'r', encoding="utf8") as file:
    data = load(file)
for product in data:
    price_per_ounce[(product["Typ"], product["Czystość"])] = float(product["Wartość za uncję (USD)"])

def ounze(x):
    if x[-2:] == "ct":
        return float(x[:-2].replace(",", ".")) * 0.0070548
    elif x[-1] == "g":
        return float(x[:-1].replace(",", ".")) * 0.0352739
    else:
        raise ValueError

with open('../dane/zbiór_wejściowy.json', 'r', encoding="utf8") as file:
    data = load(file)

object_values = []
for i, gemstone in enumerate(data):
    try:
        object_values.append((i, ounze(gemstone["Masa"]) * price_per_ounce[(gemstone["Typ"], gemstone["Czystość"])]))
    except KeyError:
        continue
print(f"{'Lp.':<5} {'Typ':<10} {'Masa':<10} {'Czystość':<10} {'Wartość':<10} {'Barwa':<10} {'Pochodzenie':<15} {'Właściciel':<20}")
for k, i in enumerate(reversed([i[0] for i in sorted(object_values, key=lambda x: x[1])[-5:]])):
    item = dict(enumerate(data))[i]
    print(f"{k+1:<5} {item['Typ']:<10} {item['Masa']:<10} {item['Czystość']:<10} {dict(object_values)[i]:<10.2f} {item['Barwa']:<10} {item['Pochodzenie']:<15} {item['Właściciel']:<20}")
