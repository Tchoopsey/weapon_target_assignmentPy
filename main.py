from Weapon import *
from Target import *
from Assignment import *
from gen_alg import *

def main():
    wL = ['Tenk', 'Tenk', 'Avion', 'Mornarica', 'Tenk', 'Avion']
    for w in wL:
        Weapon(w)
    
    tL = [5, 10, 20]
    for t in tL:
        Target(t)
    
    #print(Assignment.manualAssign())
    # Assignment.randomAssignments(100)
    genetic_algorithm(100, 0.5, 0.5)
 
if __name__ == "__main__":
    main()
