import math
players = 4
rounds =  math.log(players,2)
print "rounds: " + str(rounds)
print "matches: " + str(players/2 * rounds)
