import sys
import re
import operator as op
input="""\
################################
#...############################
###G.###########################
##.....#########################
#......#########################
##G...G.########################
#G.....G########################
###...G#########################
###....#########################
######.G.#######################
#######....#####################
###..#.....GG...G.E...##########
##........G...#####...##.#######
#.G..........#######...#..######
#...####G...#########......#####
#..G##.#..G.#########.......####
#...##....E.#########...E.....##
#...##......#########G......####
#...........#########.......####
#............#######...........#
#.....E..G...E#####E...........#
#.G...........G.............E###
#...............E#####.#..######
#..#..G...........####...#######
#..#..............######.#######
####.#...E.......###############
########..##...#################
##...##..###..##################
#.......########################
##...E..########################
###......#######################
################################""" 
input1="""\
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######"""
input2="""\
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######"""
input3="""\
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######"""
input4="""\
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######"""
input5="""\
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######"""
input6="""\
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########"""

#funcs
def readingOrder(someList):
  try:
    if not someList:
      return None
    someList=sorted(someList,key=op.itemgetter(1,0))
    return someList[0]
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def isEmpty(x,y):
  try:
    if cave[y][x]=='.':
      return True
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def isDead(unit):
  if unit[4]<=0:
    return True
def dist(x1,y1,x2,y2):
  try:
    ret = abs(x1-x2) + abs(y1-y2)
    return ret
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def aroundPoint(x,y):
  try:
    ret=[]
    ret.append([x+1,y])
    ret.append([x-1,y])
    ret.append([x,y+1])
    ret.append([x,y-1])
    return ret
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def getEnemies(source,intention):
  global units
  try:
    race=source[2]
    enemies=[]
    arounds = aroundPoint(source[0],source[1])
    enemyRace='N'
    if (race=='E'):
      enemyRace='G'
    elif (race=='G'):
      enemyRace='E'
    else:
      raise Exception("unknown race in getEnemies")
    for unit in units:
      if unit[2]==enemyRace and not isDead(unit):
        if ([unit[0],unit[1]] in arounds and intention=='move'):
          return None
        enemies.append(unit)
    return enemies
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def inRange(targets):
  try:
    if not targets:
      return None
    destinations=[]
    for enemy in targets:
      enemyX,enemyY=enemy[0],enemy[1]
      for around in aroundPoint(enemyX,enemyY):
        if isEmpty(*around):
          destinations.append(around)
    return destinations
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def getReachables(source, targets):
  #fix reachables - make the 'spread' for every direction and then pick one.
  try:
    if not targets:
      return None
    destinations=[]
    myX,myY=source[0],source[1]
    for around in aroundPoint(myX, myY):
      steps=0
      if not isEmpty(*around):
        continue
      coverage=[around]
      newFound=[coverage[0]]
      currdests=[]
      for target in targets: #check adjacencies
        if target in coverage:
          currdests.append([target,steps,around])
      while(not currdests):
        steps+=1
        found=[]
        for coords in newFound:
          x,y=coords[0],coords[1]
          for around2 in aroundPoint(x,y):
            if isEmpty(*around2) and (around2 not in coverage) and (around2 not in found):
              found.append(around2)
        newFound=found[:]
        for finding in newFound:
          coverage.append(finding[:])
        for target in targets:
          if target in coverage:
            currdests.append([target,steps,around])
        if not found:
          break
      destinations+=currdests
    return destinations
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def getNearest(targets):
  """add directions that lead to the nearest reachable"""
  try:
    if not targets:
      return None
    destinations=[]
    min = targets[0][1]
    for target in targets:
      d=target[1]
      if d<min:
        min=d
    for target in targets:
      d=target[1]
      if d==min:
        destinations.append([target[0],target[2]])
    return destinations
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def getChosen(targets):
  try:
    if not targets:
      return None
    destinations=[]
    #order targets by readingOrder of inRange
    possibilities=sorted(targets,key=lambda x:[x[0][1],x[0][0]]) 
    #pick all directions that lead to the same inRange in the shortest path
    choose=possibilities[0][0]
    for possibility in possibilities:
      if possibility[0]==choose:
        destinations.append(possibility[1])
    return destinations
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def getStep(targets):
  try:
    if not targets:
      return None
    ret=readingOrder(targets)
    return ret
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def move(unit):
  try:
    unitX,unitY,unitRace=unit[0],unit[1],unit[2] #old data
    enemies=getEnemies(unit,'move')
    inMyRange=inRange(enemies)
    reachable=getReachables(unit,inMyRange)
    nearest=getNearest(reachable)
    chosen=getChosen(nearest)
    step=getStep(chosen)
    if not step: #nowhere to move
      return unit
    stepX,stepY=step[0],step[1] #new location
    unit=[stepX,stepY,unitRace,unit[3],unit[4]] #update unit
    cave[unitY]=cave[unitY][:unitX]+'.'+cave[unitY][unitX+1:] #update old location
    cave[stepY]=cave[stepY][:stepX]+unitRace+cave[stepY][stepX+1:] #update new location
    return unit
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def getAdjacenemies(source, targets):
  try:
    if not targets:
      return None
    destinations=[]
    myX,myY=source[0],source[1]
    aroundMe=aroundPoint(myX,myY)
    for target in targets:
      if [target[0],target[1]] in aroundMe:
        destinations.append(target)
    return destinations
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def getWeakenemies(targets):
  try:
    if not targets:
      return None
    destinations=[]
    min = targets[0][4]
    for target in targets:
      targetHP=target[4]
      if targetHP<min:
        min=targetHP
    for target in targets:
      if target[4]==min:
        destinations.append(target)
    return destinations
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def getTargenemy(targets):
  try:
    if not targets:
      return None
    ret=readingOrder(targets)
    return ret
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def attack(unit):
  try:
    unitX,unitY,unitRace,unitDMG=unit[0],unit[1],unit[2],unit[3]
    enemies=getEnemies(unit,'attack')
    adjacenemies=getAdjacenemies(unit,enemies)
    weakenemies=getWeakenemies(adjacenemies)
    targenemy=getTargenemy(weakenemies)
    if not targenemy: #no one to attack
      return None
    targenemy[4]-=unitDMG
    return targenemy
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def battleIsOver():
  try:
    if not units:
      return True
    ElfRace,GoblinRace='E','G'
    for unit in units:
      if unit[2]==ElfRace and not isDead(unit):
        break
    else:
      return True
    for unit in units:
      if unit[2]==GoblinRace and not isDead(unit):
        break
    else:
      return True
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
def printCave():
  for row in cave:
    print row
  print 
def main(input, summary=False):
  #vars
  global cave,units,Xsize,Ysize,attackVal,HPVal
  cave=input.split('\n')
  units=[]
  Ysize=len(cave)
  Xsize=len(cave[0])
  attackVal=3
  HPVal=200
  round=0
  #main
  #add units - x,y,race,dmg,hp
  for y in range(Ysize):
    for x in range(Xsize):
      if cave [y][x]=='E' or cave[y][x]=='G':
        unitX,unitY=x,y
        unitRace=cave[y][x]
        unitDMG,unitHP=attackVal,HPVal
        units.append([unitX, unitY, unitRace, unitDMG, unitHP])
  #tick
  while(8):
    unitsLen=len(units)
    units=sorted(units,key=op.itemgetter(1,0))
    for unit in range(unitsLen):
      if isDead(units[unit]):
        continue
      units[unit]=move(units[unit])
      victim=attack(units[unit])
      if victim:
        if isDead(victim):
          victimX,victimY=victim[0],victim[1]
          cave[victimY]=cave[victimY][:victimX]+'.'+cave[victimY][victimX+1:]
          if battleIsOver(): #battle ended and round complete
            last=True
            for deadUnit in range (unit+1,unitsLen):
              if not isDead(units[deadUnit]):
                last=False
            if last:
              round+=1
    dead=[]
    for unit in units:
      if isDead(unit):
        dead.append(unit)
    for died in dead:
      units.remove(died)
    if battleIsOver():
      break
    round+=1
  HPSum=0
  for unit in units:
    HPSum+=unit[4]
  ans=HPSum*round
  WinningRace=units[0][2]
  if WinningRace=='E':
    race='Elves'
  elif WinningRace=='G':
    race='Goblins'
  else:
    race='Aliens'
  if not summary:
    print "The",race,"have won!\nAfter",round,"rounds, there are",len(units),race,"left,"
    print "the sum of their hp is",HPSum,", and the final answer is:",ans
  else:
    print ans
  return ans
if __name__ == '__main__':
  try:
    main(input, False)
  except Exception as e:
    print str(e),sys.exc_info()[2].tb_lineno
  finally:
    raw_input()