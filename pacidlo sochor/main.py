import csv
from datetime import datetime
import json
import os
import sys

import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table

console = Console()


def file_reader(filename):
    dochazka = []

    if not os.path.exists(filename):
        console.print(
            f"[red]Soubor '{filename}' nebyl nalezen. Zkontrolujte prosím jeho existenci.[/red]"
        )
        return dochazka

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            dochazka.append(row)

    return dochazka


def file_printer(dochazka):
    if not dochazka:
        console.print("Žádná data k zobrazení.")
        return

    table = Table(title="Docházka zaměstnanců")
    table.add_column("Číslo čipu", justify="right")
    table.add_column("Zaměstnanec", justify="left")
    table.add_column("Příchod", justify="right")
    table.add_column("Odchod", justify="right")

    for zaznam in dochazka:
        table.add_row(
            zaznam["číslo čipu"],
            zaznam["zaměstnanec"],
            zaznam["příchod"],
            zaznam["odchod"],
        )

    console.print(table)


def ulozit_jako_json(dochazka, vystupni_soubor="dochazka.json"):
    if not dochazka:
        console.print("Žádná data k uložení.")
        return

    try:
        with open(vystupni_soubor, "w", encoding="utf-8") as file:
            json.dump(dochazka, file, ensure_ascii=False, indent=4)
        console.print(
            f"[green]Data byla úspěšně uložena do souboru '{vystupni_soubor}'.[/green]"
        )
    except Exception as e:
        console.print(f"[red]Chyba při ukládání souboru: {e}[/red]")


def nejkratsi_a_nejdelsi_smena(dochazka):
    if not dochazka:
        console.print("Žádná data k analýze.")
        return

    seznam_smen = []

    for zaznam in dochazka:
        prichod = datetime.strptime(zaznam["příchod"], "%Y-%m-%d %H:%M")
        odchod = datetime.strptime(zaznam["odchod"], "%Y-%m-%d %H:%M")

        smena = odchod - prichod

        seznam_smen.append(
            {"zaměstnanec": zaznam["zaměstnanec"], "délka": smena}
        )

    nejkratsi = seznam_smen[0]
    nejdelsi = seznam_smen[0]

    for zaznam in seznam_smen:
        if zaznam["délka"] < nejkratsi["délka"]:
            nejkratsi = zaznam
        if zaznam["délka"] > nejdelsi["délka"]:
            nejdelsi = zaznam

    console.print()
    console.rule("Statistika směn")
    console.print(
        f"Nejkratší směna: {nejkratsi['zaměstnanec']} ({nejkratsi['délka']})"
    )
    console.print(
        f"Nejdelší směna: {nejdelsi['zaměstnanec']} ({nejdelsi['délka']})"
    )
    console.rule()


def ziskej_delku(zaznam):
    return zaznam["délka"]


def serazene_smeny(dochazka):
    if not dochazka:
        console.print("Žádná data k analýze.")
        return

    seznam_smen = []

    for zaznam in dochazka:
        prichod = datetime.strptime(zaznam["příchod"], "%Y-%m-%d %H:%M")
        odchod = datetime.strptime(zaznam["odchod"], "%Y-%m-%d %H:%M")

        smena = odchod - prichod

        seznam_smen.append(
            {
                "zaměstnanec": zaznam["zaměstnanec"],
                "příchod": zaznam["příchod"],
                "odchod": zaznam["odchod"],
                "délka": smena,
            }
        )

    seznam_smen.sort(key=ziskej_delku)

    table = Table(title="Seřazené směny podle délky")
    table.add_column("Zaměstnanec", justify="left")
    table.add_column("Příchod", justify="right")
    table.add_column("Odchod", justify="right")
    table.add_column("Délka", justify="right")

    for zaznam in seznam_smen:
        table.add_row(
            zaznam["zaměstnanec"],
            zaznam["příchod"],
            zaznam["odchod"],
            str(zaznam["délka"]),
        )

    console.print(table)


def vykreslit_graf(dochazka):
    if not dochazka:
        console.print("Žádná data pro vykreslení grafu.")
        return

    zamestnanci = []
    hodiny = []

    for zaznam in dochazka:
        prichod = datetime.strptime(zaznam["příchod"], "%Y-%m-%d %H:%M")
        odchod = datetime.strptime(zaznam["odchod"], "%Y-%m-%d %H:%M")
        doba_hodiny = (odchod - prichod).total_seconds() / 3600

        zamestnanci.append(zaznam["zaměstnanec"])
        hodiny.append(doba_hodiny)

    plt.figure(figsize=(10, 5))
    plt.bar(zamestnanci, hodiny, color="skyblue", edgecolor="navy")
    plt.xlabel("Zaměstnanec")
    plt.ylabel("Délka směny (hodiny)")
    plt.title("Přehled délky směn jednotlivých zaměstnanců")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    console.print(
        "[green]Otevírám okno s grafem... (Zavřete okno grafu pro návrat do programu)[/green]"
    )
    plt.show()


def menu():
    console.print()
    console.rule()
    console.print(" ANALYZA DOCHAZKY", justify="center")
    console.rule()
    console.print()

    console.print("1 - Zobrazit všechny záznamy")
    console.print("2 - Uložit jako JSON")
    console.print("3 - Nejkratší a nejdelší směna")
    console.print("4 - Seřadit směny podle délky")
    console.print("5 - Vykreslit graf délky směn")
    console.print("0 - Ukončení programu")


def main():
    dochazka = file_reader("dochazka.csv")

    while True:
        menu()
        volba = input("\nVolba: ").strip()

        if volba == "1":
            file_printer(dochazka)
        elif volba == "2":
            ulozit_jako_json(dochazka)
        elif volba == "3":
            nejkratsi_a_nejdelsi_smena(dochazka)
        elif volba == "4":
            serazene_smeny(dochazka)
        elif volba == "5":
            vykreslit_graf(dochazka)
        elif volba == "0":
            console.print("Ukončuji program. Na shledanou!")
            break
        else:
            console.print(
                "[red]Neplatná volba. Zvolte prosím číslo z nabídky.[/red]"
            )


if __name__ == "__main__":
    main()