import os

from time import time
from functools import wraps

def czasFunkcjiOgolny(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        wynik = func(*args, **kwargs)
        koniec = time()
        print(f"Czas funkcji {func.__name__}: {koniec - start}")
        return wynik
    return wrapper


def czasFunkcji(func):
    def wrapper(*args, **kwargs):
        start = time()
        katalogi, sprawdzone = func(*args, **kwargs)
        koniec = time()
        return katalogi, sprawdzone, koniec - start
    return wrapper

def zapisPlikow(func):
    def wrapper(*args, **kwargs):
        wynik = func(*args, **kwargs)
        katalogi, _, _ = wynik
        print(f"wynik: zapisuje ktore trzeba set: {katalogi}")

        with open("pamiecPlikow.txt", "a") as plik:
            calyPlik = plik.readlines()
            for sciezka in katalogi:
                if sciezka not in calyPlik:
                    calyPlik.append(sciezka)

            for sciezka in katalogi:
                plik.write(f"{sciezka}\n")

        return wynik
    return wrapper

def przygotowanie(func):
    def wrapper(nazwa, odKonca, zaczynaOd, maxWynikow, pamiec):
        maxWynikow += 1
        wynik = func(nazwa, odKonca, zaczynaOd, maxWynikow, pamiec)
        return wynik
    return wrapper

def odbiorZapisu(func):
    def wrapper(nazwa, odKonca, zaczynaOd, maxWynikow, pamiec):
        try:

            with open("pamiecPlikow.txt", "r") as plik:

                pamiec = plik.readlines()
                for i in range(len(pamiec)):
                    pamiec[i] = pamiec[i][:-1]


                wynik = func(nazwa, odKonca, zaczynaOd, maxWynikow, pamiec)

        except Exception as e:
            print(f"Przetworzono program bez pamięci, nie znaleziono pliku: 'pamiecPlikow.txt'\nPowód: {e}")

        return wynik
    return wrapper

@odbiorZapisu
@zapisPlikow
@czasFunkcji
@przygotowanie
def przeszukiwanie(nazwa="", odKonca="", zaczynaOd="C:/", maxWynikow=100, pamiec = []):
    katalogi = []
    sprawdzone = 0 
    for root, _, files in os.walk(zaczynaOd):
        if sprawdzone % 10000 == 0:
            print(f"Sprawdzono {sprawdzone} plików...")
              
        for plik in files:
            sprawdzone += 1
            if nazwa in plik:
                if odKonca == "" or plik.endswith(odKonca):
                    wynik = os.path.join(root, plik)
                    katalogi.append(wynik)
                    print("Znaleziono:", wynik)
                    print(f"len: {len(katalogi)}")
                    if len(katalogi) == maxWynikow:
                        return katalogi, sprawdzone

    return katalogi, sprawdzone, czasFunkcji

if __name__ == "__main__":
    (katalogi, sprawdzone, czas) = przeszukiwanie("google", "", "C:/", 10, [])

    [print(f"{i}, {liczba}") for i, liczba in enumerate(katalogi)]
    print(f"Sprawdzono: {sprawdzone} plików w czasie: {czas}.")
