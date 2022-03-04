import curses
from curses import wrapper
import random
import time
from math import sqrt
from win32gui import GetCursorPos

population = 100
generation = 0
mutation = 5
maxMoves = 100

def genAlgoCurses(stdscr):
	curses.curs_set(0) #disable char cursor
	maxY, maxX = stdscr.getmaxyx()
	# curses.mousemask(1)

	posX, posY = int(maxX//2), int(maxY//2) 
	stdscr.nodelay(False)
	targetX, targetY = int(maxX), 0
	targetAdd = targetY + targetX
	maxFitness = 1/(targetAdd - (maxX + maxY))
	moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
	# moves = [[1, 0], [1, 0], [1, 0], [-1, 0]]
	ParticleStartPosition = [int(maxX//2), int(maxY-4)]
	matingPool = []
	divFactX = 1280/maxX
	divFactY = 800/maxY
	mouseArray = []

	def wallsYN():
		stdscr.addstr(int(maxY//2), int(maxX//2), "make walls? y/n")

	def getTargetPos():
		cursX, cursY = GetCursorPos()
		return [int(cursX//divFactX), int(cursY//divFactY)]

	class Particle():
		def __init__(self, elements):
			self.posX = ParticleStartPosition[0]
			self.posY = ParticleStartPosition[1]
			self.elements = elements
			self.elements = self.mutate() #genotype
			self.endPos = self.endPosition()
			self.fitness = self.calcFitness() # Later evaluated to the inverse of distance from the target
			self.fitnessPercentage = round(self.fitness*10000, 1) # fitness already between 0, 1
			self.matingPoolPercentage = 0
			
		# def calcFitness(self):
		# 	retVal = self.endPos[0] + self.endPos[1]
		# 	if retVal > targetAdd:
		# 		return 1/(retVal - targetAdd)
		# 	else:
		# 		return 1/(targetAdd - retVal)
		def calcFitness(self):
			valX = self.endPos[0]
			valY = self.endPos[1]
			try:
				return 1/(sqrt((valY-targetY)**2 + (valX-targetX)**2))
			except:
				return 1

		def mutate(self):
			for i in range(len(self.elements)):
				if random.randint(0, 100) <= mutation:
					self.elements[i] = random.choice(moves)
			return self.elements

		def endPosition(self):
			x, y = self.posX, self.posY
			for a, b in self.elements:
				x += a
				y += b
			return [x, y]

		def indexMove(self, i):
			if self.posX + self.elements[i][0] < maxX and self.posX + self.elements[i][0] > 0 and self.posY + self.elements[i][1] < maxY and self.posY + self.elements[i][1] > 0:
				self.posY += self.elements[i][1]
				self.posX += self.elements[i][0]

		def setMatingPoolPercentage(self, totalFitness):
			self.matingPoolPercentage = (self.fitness/totalFitness)*100

	def move(key, x, y):
		if key == 'w':
			y -= 1
		elif key == 's':
			y += 1
		elif key == 'd':
			x += 1
		elif key == 'a':
			x -= 1
		return [x, y]

	def checkMouse():
		event = stdscr.getch()
		if event == curses.KEY_MOUSE:
			_, mx, my, _, _ = curses.getmouse()
			mouseArray.append([mx, my])
			# screen.addstr(my, mx, "bruh")
	def printMouse():
		for msX, msY in mouseArray:
			stdscr.addstr(msY, msX, '@')


	key = ''
	curr_key = ''
	generation = 0

	currPopulation = [Particle([random.choice(moves) for nbm in range(maxMoves)]) for plm in range(population)]

	while key!='q':
		try:
			key = stdscr.getkey()
		except:
			pass
		# if key == 'j':
		for jkl in range(200):
			targetX, targetY = getTargetPos()
		
			indexVal = 0


			curr_key = ''
			# posX, posY = move(key, posX, posY)

			# for i in range(maxMoves):
			# 	for p in currPopulation:
			# 		stdscr.clear()
			# 		stdscr.addstr
			maxFitness = 0
			maxFitParticle = 0
			avgFitness = 0
			totalFitness = 0
			for p in currPopulation: # gives the max fitness in current pool
				avgFitness += p.fitness
				totalFitness += p.fitness
				if p.fitness > maxFitness:
					maxFitness = p.fitness
					maxFitParticle = p
			avgFitness = avgFitness/len(currPopulation)
			stdscr.addstr(0, 0, str(maxFitness))

			maxMatingPerc = -999
			for p in currPopulation:
				p.setMatingPoolPercentage(totalFitness)

			for p in currPopulation:
				if p.matingPoolPercentage >= maxMatingPerc:
					maxMatingPerc = p.matingPoolPercentage

			if generation % 20 == 0:
				
				for i in range(maxMoves):
					stdscr.clear()
					time.sleep(0.01)
					for p in currPopulation:
						p.indexMove(i)
						# checkMouse()
						try:
							# printMouse()
							if p == maxFitParticle:
								stdscr.addstr(0, 0, "Generation: "+str(generation))
								stdscr.addstr(1, 0, "matingPool: "+str(len(matingPool)))
								stdscr.addstr(2, 0, "Max Fitness: "+str(maxFitness))
								stdscr.addstr(3, 0, "Average Fitness: "+str(avgFitness))
								stdscr.addstr(4, 0, "currPopulation: "+str(len(currPopulation)))
								stdscr.addstr(5, 0, "Mutation rate: "+str(mutation)+"%")
								stdscr.addstr(6, 0, "Target Position: "+str([targetX, targetY]))
								stdscr.addstr(7, 0, "mouseArray length: "+str(len(mouseArray)))
								stdscr.addstr(8, 0, "max fitnessPercentage: "+str(maxMatingPerc))#str(maxFitParticle.matingPoolPercentage))
								# stdscr.addstr(p.posY, p.posX, str(round(p.fitnessPercentage, 2)) + "++")
								stdscr.addstr(p.posY, p.posX, '█')
							else:
								stdscr.addstr(0, 0, "Generation: "+str(generation))
								# stdscr.addstr(p.posY, p.posX, str(p.fitnessPercentage))
								stdscr.addstr(p.posY, p.posX, '.')
							
						except:
							pass
						stdscr.refresh()

			matingPool = []
			for cp in currPopulation:
				for i in range(int(cp.matingPoolPercentage)):
					matingPool.append(cp)

			tempP = []
			for mk in range(population):
				parentA = (random.choice(matingPool)).elements
				parentB = (random.choice(matingPool)).elements
				child = []
				for k in range(maxMoves):
					if k <= maxMoves/2:
						child.append(parentA[k])
					else:
						child.append(parentB[k])
				tempP.append(child)
			currPopulation = [Particle(elm) for elm in tempP]
			generation += 1

			try:
				key = stdscr.getkey()
			except:
				pass
			if key == 'q':
				break



	stdscr.getch()
wrapper(genAlgoCurses)

# moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
# for a, b in [random.choice(moves) for nbm in range(maxMoves)]:
# 	print(a, b)