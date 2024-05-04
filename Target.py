from copy import deepcopy

class Target:
    """
        def __init__(self, value: int)
        Kreira metu, kao argument uzima cjelobrojnu vrijednost
    """
    targetList = []
    chanceToSurvive = {}

    def __init__(self, value: int):
        self.value = value
        self.name = 'T' + str(len(Target.targetList) + 1)
        Target.targetList.append(self)
    
    def printTargetList():
        """Ispisuje listu svih Meta"""
        print("Mete i njihove trenutne vrijednosti: ")
        for t in Target.targetList:
            print(t)
        print()
    
    def targetListNames() -> list:
        """Vraca listu imena Meta"""
        namesList = []
        for t in Target.targetList:
            namesList.append(t.name)
        
        return namesList
    
    def targetListCopy() -> list:
        tl = []
        for t in Target.targetList:
            tl.append(deepcopy(t))
        return tl
    
    def getValueByName(name: str) -> int:
        """Vraca vrijednost navedene Mete"""
        for target in Target.targetList:
            if target.name == name:
                return target.value
        return -1
    
    def getByName(name: str):
        """Vraca Metu sa navedenim imenom"""
        for target in Target.targetList:
            if target.name == name:
                return target
        return -1
    
    def __str__(self) -> str:
        return f"{self.name}: {self.value}"
