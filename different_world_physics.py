# Noah Yi, GitHub: NoahTheCorgi
# future task: apply Hashlife algorithm

import time
import random

n = 100
N=n*n # total number of cells


# randomized game of life world initial state generation
def determine_new_world():
	wworld = []
	i = 0
	while i < N:
		# wworld.append(" ")
		# random.choice([" ","*"]))
		wworld.append(" ")
		i+=1
	return wworld

def show_world_terminal(world):
	# this is to display on the terminal
	j=0
	L = []
	the_word = ""
	while j < N:
		L.append(world[j:n+j])
		j+=n
	k = 0
	while k < n:
		l = 0
		while l < n:
			the_word = the_word + L[k][l] + ' '
			l+=1
		k += 1
		the_word += '\n'
	print(the_word)

# world/realm physics: original laws by Conway
def create_next_state_original(previous):

	nbhr_count = [0]*N # neighborhood count
	# addressing the corners first:
	# top left corner
	if previous[0] == "*":
		nbhr_count[(0) + (0)*n + 1] +=1
		nbhr_count[(0) + (0)*n + n] +=1
		nbhr_count[(0) + (0)*n + 1 + n] +=1
	# top right corner
	if previous[n-1] == "*":
		nbhr_count[(n-1) + (0)*n - 1] +=1
		nbhr_count[(n-1) + (0)*n + n] +=1
		nbhr_count[(n-1) + (0)*n - 1 + n] +=1
	# bottom left corner
	if previous[(n-1)*n] == "*":
		nbhr_count[(0) + (n-1)*n + 1 ] +=1
		nbhr_count[(0) + (n-1)*n - n ] +=1
		nbhr_count[(0) + (n-1)*n + 1 - n] +=1
	# bottom right corner
	if previous[(n-1)*n + n-1] == "*":
		nbhr_count[(n-1) + (n-1)*n -1] +=1
		nbhr_count[(n-1) + (n-1)*n - n] +=1
		nbhr_count[(n-1) + (n-1)*n - 1 - n] +=1

	# next, addressing the edges without the corners....
	# e1. addressing the top horizontal edge
	b = 1
	while b < n-1:
		if previous[b] == "*":
			nbhr_count[(b) + (0)*n + 1] +=1
			nbhr_count[(b) + (0)*n - 1] +=1
			nbhr_count[(b) + (0)*n + n] +=1
			nbhr_count[(b) + (0)*n +1 + n] +=1
			nbhr_count[(b) + (0)*n - 1 + n] +=1
		b+=1
	# e2. addressing the bottom horizontal edge
	b = 1
	while b < n-1:
		if previous[(n-1)*n + b] == "*":
			nbhr_count[(b) + (n-1)*n + 1] +=1
			nbhr_count[(b) + (n-1)*n - 1] +=1
			nbhr_count[(b) + (n-1)*n - n] +=1
			nbhr_count[(b) + (n-1)*n +1 - n] +=1
			nbhr_count[(b) + (n-1)*n - 1 - n] +=1
		b+=1
	# e3. addresssing the left vertical edge
	a = 1
	while a < n-1:
		if previous[a*n] == "*":
			nbhr_count[(0) + (a)*n -n] +=1
			nbhr_count[(0) + (a)*n -n + 1] +=1
			nbhr_count[(0) + (a)*n +1] +=1
			nbhr_count[(0) + (a)*n +n] +=1
			nbhr_count[(0) + (a)*n +n + 1] +=1
		a+=1
	# e4. addressing the right vertical edge
	a = 1
	while a < n-1:
		if previous[a*n + n-1] == "*":
			nbhr_count[(n-1) + (a)*n -n] +=1
			nbhr_count[(n-1) + (a)*n -n - 1] +=1
			nbhr_count[(n-1) + (a)*n -1] +=1
			nbhr_count[(n-1) + (a)*n +n] +=1
			nbhr_count[(n-1) + (a)*n +n - 1] +=1
		a+=1

	# Finally, we address all the remaining cells
	# 'b' represents the width 'a' represents the height all starting from the top left corner....
	a = 1
	while a < n-1:
		b = 1
		while b < n-1:
			if previous[n*a + b] == "*":
				nbhr_count[(b) + (a)*n + 1 -n] +=1
				nbhr_count[(b) + (a)*n -n] +=1
				nbhr_count[(b) + (a)*n - 1 -n] +=1

				nbhr_count[(b) + (a)*n + 1] +=1
				nbhr_count[(b) + (a)*n - 1] +=1

				nbhr_count[(b) + (a)*n + 1 + n] +=1
				nbhr_count[(b) + (a)*n + n] +=1
				nbhr_count[(b) + (a)*n - 1 + n] +=1
			b+=1
		a+=1
	# now we apply the world physics laws
	i = 0
	while i < N:
		m = nbhr_count[i]
		if previous [i] == "*": # if the cell is alive
			# should be m<2 or m>3 for original conway's set of rules.
			if m < 2 or m > 3:
				previous[i] = " "
		else: # if the cell is dead
			# should be m == 3 for original conway's set of ruless
			if m == 3:
				previous[i] = "*"
		i+=1
	return previous


# world/universe physics: no edge of the world but a planet globe connected + laws by Conway OR Alternatives
# we achieve this by applying modulo n to the index arithmetic accordingly (with minor adjustments for User display).
def create_next_state_planet(previous):

	nbhr_count = [] # neighborhood count
	for k in range(0, n):
		row = [0]*n
		nbhr_count.append(row)

	#'b' represents "x" the width AND 'a' represents "y" the height all starting from the top left corner....
	y = 0
	while y < n:
		x = 0
		while x < n:
			if previous[n*y + x] == "*": # there is nothing wrong here,,,
				nbhr_count[(y+1) % n][(x-1) % n] +=1
				nbhr_count[(y+1) % n][x] +=1
				nbhr_count[(y+1) % n][(x+1) % n] +=1

				nbhr_count[y][(x+1) % n] +=1
				nbhr_count[y][(x-1) % n] +=1

				nbhr_count[(y-1) % n][(x-1) % n] +=1
				nbhr_count[(y-1) % n][x] +=1
				nbhr_count[(y-1) % n][(x+1) % n] +=1
			x+=1
		y+=1

	# now we apply the world physics laws
	y = 0
	while y < n:
		x = 0
		while x < n:
			m = nbhr_count[y][x]
			if previous [n*y + x] == "*": # if the cell is alive
				# should be m < 2 or m > 3 for original conway's set of rules.
				if m < 2 or m > 3:
					previous[n*y + x] = " "
			else: # if the cell is dead
				# should be m == 3 for original conway's set of rules
				if m == 3:
					previous[n*y + x] = "*"
			x+=1
		y+=1

	return previous


def create_next_state_planet_research(previous, lower, lowerDecrease, lowerDeviationChancePercent,\
												upper, upperIncrease, upperDeviationChancePercent):

	# neighborhood count
	nbhr_count = []
	for k in range(0, n):
		row = [0]*n
		nbhr_count.append(row)

	### (Fixed) this is where the indexing bug was ... ###
	# 'b' represents "x" the width AND 'a' represents "y" 
	# , which is the height all starting from the top left corner.
	y = 0
	while y < n:
		x = 0
		while x < n:
			if previous[n*y + x] == "*":
				nbhr_count[(y+1) % n][(x-1) % n] +=1
				nbhr_count[(y+1) % n][x] +=1
				nbhr_count[(y+1) % n][(x+1) % n] +=1

				nbhr_count[y][(x+1) % n] +=1
				nbhr_count[y][(x-1) % n] +=1

				nbhr_count[(y-1) % n][(x-1) % n] +=1
				nbhr_count[(y-1) % n][x] +=1
				nbhr_count[(y-1) % n][(x+1) % n] +=1
			x+=1
		y+=1

	################################################
	# now we apply the world/realm's physics/rules #
	################################################
	y = 0
	while y < n:
		x = 0
		while x < n:
			
			###########################################
			### Research World Physics Customizable ###
			###########################################
			# lower = 2
			# lowerDecrease = 1
			# lowerDeviationChancePercent = 0.05
			# upper = 3
			# upperIncrease = random.randint(1, 8 - upper) # this allows up to maximum 8 neighbors
			# upperDeviationChancePercent = int(1 / (500*(upper + upperIncrease)))
			###########################################
			###########################################
			###########################################

			dice = random.randint(1, 100)
			if (dice/100 <= lowerDeviationChancePercent):
				lower -= lowerDecrease
			dice = random.randint(1, 100)
			if (dice/100 <= upperDeviationChancePercent):
				upper += upperIncrease
			m = nbhr_count[y][x]
			if previous [n*y + x] == "*": # if the cell is alive
				# should be m<2 or m>3 for original conway's set of rules.
				if m < lower or m > upper:
					previous[n*y + x] = " "
			else: # if the cell is dead
				# should be m == 3 for original conway's set of rules
				if m == upper:
					previous[n*y + x] = "*"
			x+=1
		y+=1

	return previous

# can be used to create completely anomalous events
def veryunlikelyeventv2(previous):
	unlikelyevent = []
	for i in range(5):
		unlikelyevent.append(random.choice([0,1]))
	if unlikelyevent == [0,0,0,0,0]: # since five, 1/32 chance,,,
		previous = createlength3star(previous, 7)
	return previous

def createlength3star(previous, count):
	# note: star could be "buggy" with edges
	for i in range(count):
		# note: the same can be flipped again
		r = random.randint(0,N-1)
		verticalORhorizontal = random.choice([0,1])
		# vertical star
		if verticalORhorizontal == 0:
			if r-n >= 0:
				previous[r-n] = "*"
			previous[r] = "*"
			if r+n <= N-1:
				previous[r+n] = "*"
		else: #horizontal star
			if r-1 >= 0:
				previous[r-1] = "*"
			previous[r] = "*"
			if r+1 <= N-1:
				previous[r+1] = "*"
	return previous
