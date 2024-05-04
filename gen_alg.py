import random
from Weapon import *
from Assignment import *

# tournament selection

def selection(pop):
    """
        Funkcija za biranje najboljeg roditelja
    """
    # Biramo radnom roditelja iz populacije
    selection_ix = random.choice(list(pop.keys()))
    # izvlacimo 3 random roditelja za slucaj da postoji bolji
    for i in range(3):
        ix = random.choice(list(pop.keys()))
        if ix < selection_ix:
            selection_ix = ix
            # Vracamo boljeg roditelja u slucaju pronalaska istog
            return {selection_ix:pop[selection_ix]}
    # inace, vracamo prvog odabranog
    return {selection_ix:pop[selection_ix]}

# Ukrstamo 2 roditelja kako bismo dobili 2 djeteta
def crossover_helper1(c1, c2, c1key, start, end):
    """
        Prvi helper sluzi da povrati vrijednost Mete prvog djeteta
        koja je bila prije Dodjele, zamjeni je sa novom Metom koja je na istoj
        poziciji drugog djeteta i izracuna novu vrijednost mete
    """
    for i in range(start, end):
        ctd1 = round(1 - Weapon.getChanceToDestroy(c1[i].weapon, 
                                                   c1[i].target.name), 1)
        ctd2 = round(1 - Weapon.getChanceToDestroy(c2[i].weapon,
                                                   c2[i].target.name), 1)
        c1key /= ctd1
        c1key *= ctd2
        c1[i] = c2[i]
    return {c1key:c1}

def crossover_helper(c1, c2, pt):
    """
        Ovaj helper izvlaci potrebne informacije djece kako bi se u prethodnom
        moglo izvrsiti ukrstanje
    """
    c1temp = list(c1.values())
    c1temp = c1temp[0]
    c2temp = list(c2.values())
    c2temp = c2temp[0]
    c1key = list(c1.keys())
    c1key = c1key[0]
    c2key = list(c2.keys())
    c2key = c2key[0]
    c1 = crossover_helper1(c1temp, c2temp, c1key, 0, pt)
    c2 = crossover_helper1(c2temp, c1temp, c2key, pt, len(c2temp))
    return [c1, c2]
 
def crossover(p1, p2, r_cross):
    # djeca su prvobitno kopije roditelja
    c1, c2 = p1.copy(), p2.copy()
    end = Weapon.totalWeapons
    # r_cross - sansa da ce se ukrstanje izvrsiti
    if random.random() < r_cross:
        # biramo tacku ukrstanja (da nije pocetak ili kraj liste)
        pt = random.randint(1, end-2)
        return crossover_helper(c1, c2, pt)
    return [c1, c2]

def mutation(child, r_mut):
    # izvlacimo listu Dodjela iz djeteta
    c = list(child.values())
    c = c[0]

    for i in range(len(c)):
        # provjeravamo mogucnost mutacije
        # r_mut - sansa da ce se mutacija izvrsiti
        if random.random() < r_mut:
            # flip a bit
            c = Assignment.singleAssign(c, i)
    # izracunavamo novu vrijednost Dodjele nakon mutacije
    res = 0
    for a in c:
        res += a.target.value
    return {res:c}
 
# GA
def genetic_algorithm(n_pop, r_cross, r_mut):
    # inicijalizujemo populaciju (n_pop dodjela)
    pop = Assignment.randomAssignments(n_pop)

    # cuvamo najbolje rjesenje (biramo ga nasumicno)
    best_eval = random.choice(list(pop.keys()))
    best = {best_eval:pop[best_eval]}
    
    # biramo roditelje
    selected = [selection(pop) for _ in range(n_pop)]
    # kreiramo sledecu generaciju
    children = {}
    for i in range(0, n_pop, 2):
        # odabrane roditelje izvlacimo u parovima
        p1, p2 = selected[i], selected[i+1]
        
        # izvrsavamo ukrstanje i mutaciju
        for c in crossover(p1, p2, r_cross):
            # mutation
            c = mutation(c, r_mut)
            # store the next generation
            children.update(c)
    pop = children
    
    # trazimo novo najbolje rjesenje
    for v in pop:
        if v < best_eval:
            best, best_eval = {v:pop[v]}, v

    print(best)
    return [best, best_eval]
