from abc import ABC, abstractmethod
from datetime import datetime


class Szoba(ABC):
    @abstractmethod
    def __init__(self, szobaszam):
        self.szobaszam = szobaszam
        self.ar = 10000

    @abstractmethod
    def OsszAr(self):
        pass


class EgyagyasSzoba(Szoba):
    def __init__(self, emelet, eszobaszam, erkely, parkolo, komfort, wifi, wc):
        super().__init__(eszobaszam)
        self.emelet = emelet
        self.erkely = erkely
        self.parkolo = parkolo
        self.komfort = komfort
        self.wifi = wifi
        self.wc = wc

    def OsszAr(self):
        Ar = self.ar + (self.emelet * 5000) - 5000
        if self.erkely:
            Ar += 3000
        if self.parkolo:
            Ar += 3000
        if self.komfort:
            Ar += 5000
        if self.wifi:
            Ar += 1500
        if self.wc:
            Ar += 2500
        return Ar


class KetagyasSzoba(Szoba):
    def __init__(self, emelet, kszobaszam, udvar, legkondi, konyha, medence, gym):
        super().__init__(kszobaszam)
        self.emelet = emelet
        self.udvar = udvar
        self.legkondi = legkondi
        self.konyha = konyha
        self.medence = medence
        self.gym = gym

    def OsszAr(self):
        Ar = self.ar + (self.emelet * 5000) - 5000
        if self.udvar:
            Ar += 5000
        if self.legkondi:
            Ar += 3000
        if self.konyha:
            Ar += 3000
        if self.medence:
            Ar += 5000
        if self.gym:
            Ar += 2500
        return Ar


class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def uj_szoba(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szobaszam):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                return szoba.OsszAr()
        return None


class Foglalas:
    def __init__(self, szoba, honap, nap):
        self.szoba = szoba
        self.honap = honap
        self.nap = nap
        self.foglalasok = []

    def foglalaslemondas(self, szalloda):
        szalloda.szobak.remove(self)
        print("Foglalás lemondva.")


def szobafoglalas():
    tipus = input("Milyen típusú szobát szeretne foglalni? (egyágyas/kétágyas): ").strip().lower()
    megfelelo_szobak = [szoba for szoba in szalloda.szobak if (tipus == "egyágyas" and isinstance(szoba, EgyagyasSzoba)) or (tipus == "kétágyas" and isinstance(szoba, KetagyasSzoba))]

    if not megfelelo_szobak:
        print("Nincs ilyen típusú szoba.")
        return

    print("Elérhető szobák:", end='')
    for szoba in megfelelo_szobak:
        print(" ", szoba.szobaszam, end='')
    print()

    fszobaszam = input("Melyik szobát szeretné lefoglalni? Írja be a szobaszámot: ").strip()
    kivalasztottszoba = next((szoba for szoba in megfelelo_szobak if szoba.szobaszam == fszobaszam), None)

    if not kivalasztottszoba:
        print("Nincs ilyen szobaszám.")
        return

    print(f"A {kivalasztottszoba.szobaszam} szoba tulajdonságai: ")
    print(f"Az {kivalasztottszoba.emelet}. emeleten van")
    if isinstance(kivalasztottszoba, EgyagyasSzoba):
        print(f"Erkély: {kivalasztottszoba.erkely}")
        print(f"Parkoló: {kivalasztottszoba.parkolo}")
        print(f"Komfort: {kivalasztottszoba.komfort}")
        print(f"WiFi: {kivalasztottszoba.wifi}")
        print(f"WC: {kivalasztottszoba.wc}")
    elif isinstance(kivalasztottszoba, KetagyasSzoba):
        print(f"Udvar: {kivalasztottszoba.udvar}")
        print(f"Légkondi: {kivalasztottszoba.legkondi}")
        print(f"Konyha: {kivalasztottszoba.konyha}")
        print(f"Medence: {kivalasztottszoba.medence}")
        print(f"Gym: {kivalasztottszoba.gym}")

    ar = kivalasztottszoba.OsszAr()
    print(f"A szoba ára: {ar} Ft/Nap")

    biztos = input("Biztos le szeretné foglalni? (igen/nem): ").strip().lower()
    if biztos != "igen":
        print("Foglalás megszakítva.")
        return
    try:
        fhonap = int(input("Adja meg a hónapot (1-12): ").strip())
        fnap = int(input("Adja meg a napot (1-31): ").strip())
    except ValueError:
        print("Hibás dátum megadás.")
        return

    maidatum = datetime.now().date()
    foglalasdatum = datetime(datetime.now().year, fhonap, fnap).date()
    if foglalasdatum <= maidatum:
        print("Nem lehetséges lefoglalni, a múltban van az időpont!")
        return
    if (fhonap, fnap) in foglalasok.get(int(fszobaszam), []):
        print("Ez a szoba már foglalt ezen a napon.")
        return
    foglalasok[int(fszobaszam)].append((fhonap, fnap))
    print(f"A szoba lefoglalva {fhonap} hó {fnap}-ára.")


def foglalaslemondas():
    try:
        szobaszam = int(input("Adja meg a szobaszámot: ").strip())
        honap = int(input("Adja meg a hónapot (1-12): ").strip())
        nap = int(input("Adja meg a napot (1-31): ").strip())
    except ValueError:
        print("Hibás adatbevitel. Kérem, adjon meg helyes számokat.")
        return

    foglalasok_szoba = foglalasok.get(szobaszam)

    if foglalasok_szoba and (honap, nap) in foglalasok_szoba:
        foglalasok_szoba.remove((honap, nap))
        print(f"A foglalás lemondva {honap} hó {nap}-ára a {szobaszam} szobaszámú szobában.")
        if not foglalasok_szoba:
            del foglalasok[szobaszam]
    else:
        print("Nincs foglalás ezen a napon a megadott szobaszámmal.")


def foglalaslistazas():
    if not foglalasok:
        print("Nincsenek foglalások.")
        return

    print("Foglalások listája:")
    for szobaszam, datumok in foglalasok.items():
        print(f"Szobaszám: {szobaszam}")
        for honap, nap in datumok:
            print(f"    {honap}. hónap {nap}. nap")


szalloda = Szalloda("Bogar Szálló")
szalloda.uj_szoba(KetagyasSzoba(1, "11", True, True, True, True, True))
szalloda.uj_szoba(KetagyasSzoba(1, "12", True, False, True, True, False))
szalloda.uj_szoba(KetagyasSzoba(1, "13", True, True, False, False, True))
szalloda.uj_szoba(KetagyasSzoba(2, "21", False, True, False, False, True))
szalloda.uj_szoba(KetagyasSzoba(2, "22", False, False, True, False, False))
szalloda.uj_szoba(EgyagyasSzoba(2, "23", False, False, False, True, True))
szalloda.uj_szoba(EgyagyasSzoba(3, "31", True, True, True, True, True))
szalloda.uj_szoba(EgyagyasSzoba(3, "32", True, True, False, True, False))
szalloda.uj_szoba(EgyagyasSzoba(3, "33", False, False, False, False, True))

foglalasok = {
    11: [(5, 25), (6, 2)],
    12: [(6, 12)],
    13: [(5, 27), (7, 14)],
    21: [(5, 30), (6, 3)],
    22: [(5, 26), (5, 27), (5, 28)],
    23: [(6, 5)],
    31: [(6, 17), (6, 22)],
    32: [(5, 27), (6, 27)],
    33: [(6, 13), (6, 14)]
}

for szoba in szalloda.szobak:
    if isinstance(szoba, Szoba):
        for szobaszam, foglalasdatumok in foglalasok.items():
            if szoba.szobaszam == szobaszam:
                for honap, nap in foglalasdatumok:
                    foglalas = Foglalas(szoba, honap, nap)
                    szalloda.uj_szoba(foglalas)

#Fő progi

print("Üdvözöljük a ", szalloda.nev, "szállodában!")
print("Írja be mit szeretne csinálni: \nSzoba foglálsa, Foglalás lemondása, Foglalások listázása")
print('Ha végzett írja be a "Kész" szót')
valasz = ""
while valasz != "Kész":
    valasz = input("    >")
    if valasz == "Szoba foglalása":
        szobafoglalas()
    elif valasz == "Foglalás lemondása":
        foglalaslemondas()
    elif valasz == "Foglalások listázása":
        foglalaslistazas()
    elif valasz == "Kész":
        break
    else:
        print("Nem értem a parancsot, kérem írja be újra!")