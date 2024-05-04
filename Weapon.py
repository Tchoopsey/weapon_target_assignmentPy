import re

class Weapon:
    totalWeapons = 0
    weaponTypeCount = {}
    chanceToDestroy = {}
    
    def __init__(self, type: str):
        self.type = type
        Weapon.totalWeapons += 1
        Weapon.addToTypeCount(self)
    
    def addToTypeCount(weapon):
        """
            weaponTypeCount sluzi za cuvanje broja Oruzja koje po njihovim
            tipovima, npr, 3 tenka, 5 aviona (ukupno 8)
            {'Tenk':3, 'Avion':5}
        """
        for w in Weapon.weaponTypeCount:
            # Ako se oruzje vec nalazi u rjecniku, podizemo broj njegovog tipa 
            if weapon.type == w:
                Weapon.weaponTypeCount[weapon.type] += 1
                return
        # U suprotnom ga dodajemo u rjecnik
        Weapon.weaponTypeCount[weapon.type] = 1
    
    def __str__(self) -> str:
        return f"{self.type}"
    
    def regExp(string: str, n: int) -> str: 
        """
            Kreira pattern sa kojim cemo provjeravati Mete unutar rjecnika
            chanceToDestroy, npr. [('T1: 10', 10)]
            string - niska koju tracimo (ime Mete)
            int - grupa koju ce vratiti nakon matchovanja patterna i string-a
            (.group(1) vraca ime mete, .group(2) vraca vrijednost)
        """
        pattern = re.compile(r"(T\d+): (\d+)")
        match = pattern.search(string)
        return match.group(n)
    
    def getChanceToDestroy(type: str, name: str) -> float:
        """
            Vraca sansu da Oruzje tipa 'type' unisti Metu 'name'
        """
        if type in Weapon.chanceToDestroy:
            for _ in Weapon.chanceToDestroy[type]:
                if name == Weapon.regExp(_[0], 1):
                    return _[1]

        return -1
    
    def printWeaponsTypeByCount():
        """
            Ispisuje broj kreiranih/iskoristenih Oruzja pojedinacno
        """
        print("Preostalo oruzje: ")
        for w in Weapon.weaponTypeCount:
            print(w, ':', Weapon.weaponTypeCount[w])
        print()
