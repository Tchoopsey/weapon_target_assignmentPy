from Weapon import *
from Target import *

import random

class Assignment:
    assignments = []
    
    def __init__(self, weapon, target) -> None:
        self.weapon = weapon
        self.target = target
        self.asngName = "_asng(" + weapon + ':' + target.name + ')';
    
    def addAsng(asng) -> bool:
        """
            Dodaje Dodjelu u listu dodjela
        """
        Assignment.assignments.append(asng)
    
    def generateChanceToDestroy() -> dict:
        """
            Nasumicno generisanje sanse za unistenje Mete prema tipu Oruzja
        """
        for weapon in Weapon.weaponTypeCount:
            targets = []
            for target in Target.targetList:
                targets.append((str(target), round(random.uniform(0.1, 0.9), 1)))
            Weapon.chanceToDestroy[weapon] = targets
        return Weapon.chanceToDestroy
    
    def printChanceToDestroy(CTD: dict):
        """
            Ispisuje sansu unistavanja svakog Oruzja za svaku Metu
        """
        print("Sansa pojedinacnih oruzja da unisti pojedinacne mete:")
        for w in CTD:
            print(w, ":", CTD[w])
    
    def printAssignments():
        """
            Ispisuje listu dodjela
        """
        print("Lista kreiranih dodjela: ")
        for a in Assignment.assignments:
            print(a)
        print()
    
    def wta(weapon, target):
        # Pozivamo konstruktor Dodjele unutar funkcije
        # za dodavanje Dodjele u listu dodjela (pohrana)
        # Umanjujemo ukupan broj oruzja, kao i broj
        # oruzja po tipu
        Assignment.addAsng(Assignment(weapon, target))
        Weapon.totalWeapons -= 1
        Weapon.weaponTypeCount[weapon] -= 1
        # Sansa da Meta prezivi je 1 ("100%") 
        # Oduzimanjem od toga sanse da ce Meta biti unistena
        # dobicemo pravu vrijednost sanse za prezivjavanje Mete
        # koju mnozimo sa njenom vrijednoscu prezivljavanja
        ctd = round(1 - Weapon.getChanceToDestroy(weapon, target.name), 1)
        target.value *= ctd
    
    
    def manualAssign():
        Weapon.printWeaponsTypeByCount()
        Target.printTargetList()
        # Na pocetku izvrsavanja dodjele, generiseno nasumicne sanse
        # svakog oruzja da unisti svaku metu
        chanceToDestroy = Assignment.generateChanceToDestroy()
        Assignment.printChanceToDestroy(chanceToDestroy)

        while(Weapon.totalWeapons != 0):
            print('-'*20)
            weapon = input("Oruzje: ")
            if weapon not in Weapon.weaponTypeCount or \
            Weapon.weaponTypeCount[weapon] == 0:
                print("Uneseno oruzje ne postoji, pokusajte ponovo!")
                continue

            target = input("Meta: ")
            if target not in Target.targetListNames():
                print("Unesena meta ne postoji, pokustajte ponovo!")
                continue
            
            # stvaramo sumu vrijednosti prezivljavanja
            Assignment.wta(weapon, Target.getByName(target))
            
            print()
            Assignment.printAssignments()
            Weapon.printWeaponsTypeByCount()
            Target.printTargetList()
            Assignment.printChanceToDestroy(chanceToDestroy)
        
        result = 0 # glavni rezultat
        for t in Target.targetList:
            result += t.value
        
        print("Konacna ukupna vrijednost prezivljavanja protivnika:")
        
        return result
    
    def printAllAssignments(assignment: list):
        for res in assignment:
            print(res)
            for a in assignment[res]:
                print(a)
    
    def wta2(assignments: list, weapon, target) -> list:
        assignments.append(Assignment(weapon, target))
        assignments = Assignment.sort(assignments)
        ctd = round(1 - Weapon.getChanceToDestroy(weapon, target.name), 1)
        print(ctd)
        target.value *= ctd
        round(target.value, 2)
    
    def sort(l: list) -> list:
        for i in range(len(l) - 1):
            for j in range(i+1, len(l)):
                if l[i].weapon > l[j].weapon:
                    l[i], l[j] = l[j], l[i]
        return l
    
    def singleAssign(assignments: list, k: int):
        assignment = {}
        targetListTemp = Target.targetListCopy()
        randomTarget = random.choice(targetListTemp)
        revAsng = assignments
        revAsng.reverse()
        for i in revAsng:
            if randomTarget.name == i.target.name:
                randomTarget.value = i.target.value
                break
        ctd1 = round(1 - Weapon.getChanceToDestroy(assignments[k].weapon,
                                                   assignments[k].target.name), 1)
        
        ctd2 = round(1 - Weapon.getChanceToDestroy(assignments[k].weapon,
                                                  randomTarget.name), 1)
        assignments[k].target.value = round(assignments[k].target.value / ctd1, 1)
        randomTarget.value = round(ctd2 * randomTarget.value)
        assignments[k].target = randomTarget
        return assignments
    
    def randomAssignments(n_pop: int):
        chanceToDestroy = Assignment.generateChanceToDestroy()
        Assignment.printChanceToDestroy(chanceToDestroy)
        assignment = {}

        for i in range(n_pop):
            assignments = []
            nWeapon = Weapon.totalWeapons
            weaponTypeCountTemp = Weapon.weaponTypeCount.copy()
            targetListTemp = Target.targetListCopy()
            print('-'*20)
            print()
            print("Assing attempt " + str(i))
            print() 

            while nWeapon:
                print(weaponTypeCountTemp)
                for t in targetListTemp:
                    print(t)
                weapon = random.choice(list(weaponTypeCountTemp.keys()))
                if weaponTypeCountTemp[weapon] == 0:
                    continue
                target = random.choice(targetListTemp)
                print(weapon, target)
                Assignment.wta2(assignments, weapon, target)
                nWeapon -= 1
                weaponTypeCountTemp[weapon] -= 1
                
                for a in assignments:
                    print(a)
            result = 0

            for t in targetListTemp:
                result += t.value
            assignment[result] = assignments
        
        Assignment.printAllAssignments(assignment)
        return assignment
    
    def __str__(self) -> str:
        return f"{self.asngName}"
    
