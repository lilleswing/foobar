def expand(loc):
    x, y = loc[0], loc[1]
    return [(x+1, y), (x-1, y), (x, y-1), (x,y+1)]


def anneal(population, infected, strength):
    done = True
    for i in xrange(len(population)):
        for j in xrange(len(population[0])):
            if (i, j) in infected and population[i][j] != -1 and population[i][j] <= strength:
                done = False
                population[i][j] = -1
                infected.update(expand((i,j)))
    return done


def answer(population, x, y, strength):
    infected = set([(y,x)])
    done = anneal(population, infected, strength)
    while not done:
        done = anneal(population, infected, strength)
    return population


answer([[1,2,3], [2,3,4], [3,2,1]], 0, 0 , 2)
