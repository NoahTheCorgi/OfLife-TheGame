# NoahTheCorgi

import math
import time
import random

# for simple and straight forward rendering
import arcade

# User also has the option to simulate within the terminal...

from GOL_User import *
from different_world_physics import *

"""
# Main Task: Experiment with various physics rule and detect meaningful patterns and log those rules.
# Future Biggest Task: optimize using the Hashlife algorithm...
"""

# this s value should be an odd number preferrably
# ... unless you implement differently with grid that shows,,,
s = 10  # size of the cell in pixels
# n = n --- this is from different_world_physics; be the number of cells of 1 row or 1 column
N = n*n # the total amount of cells
SCREEN_WIDTH = s*n
SCREEN_HEIGHT = s*n
SCREEN_TITLE = "Of Life, The Game [Realm 0 : Entity 1]"

class OfLifeSimulation(arcade.Window):

	def __init__(self, width, height, title):

		super().__init__(width, height, title, resizable=False) # , fullscreen=True)
		
		# Note:
		# avoid full screen option if not running from excutable...
		# mac os seems to sometimes need user to click outside the window 
		# ... then, come back to the window to enable for user input;
		# otherwise the window might not focus for keyboard input...
		# this seems to be fixed now... 
		# Side note: there might be a window focusing method within pygame...
		# ... but for now, creating an executable avoids this issue,
		# ... or user can simple click another outside window then come back.

		arcade.set_background_color(arcade.color.BLACK)

		# this is an instance of User Class from GOL_User.py
		self.User = User()

		self.nextState = None
		self.paused = None
		self.showgrid = None

		# can be used to set up various animations or time or frame rate control
		self.countframes = 0
		self.right_save_count = 0
		self.left_save_count = 0
		self.up_save_count = 0
		self.down_save_count = 0

		self.right_press = None
		self.left_press = None
		self.up_press = None
		self.down_press = None

		self.right_press_double = None
		self.left_press_double = None
		self.up_press_double = None
		self.down_press_double = None

		self.mouse_press = False
		self.mouselocation_x = None
		self.mouselocation_y = None

		self.mouse_same_cell = None

		self.time = 0;

	def setup(self):

		self.nextState = determine_new_world()
		# "n" is imported from "different_world_physics"
		self.showgrid = False
		self.countframes = 0
		
		# False means it is not paused. True means it is paused.
		self.paused = False

		self.set_update_rate(1/16) # 10 fps

		self.right_press = False
		self.left_press = False
		self.up_press = False
		self.down_press = False

		self.right_press_double = 0
		self.left_press_double = 0
		self.up_press_double = 0
		self.down_press_double = 0

		self.mouselocation_x = 0
		self.mouselocation_y = 0

		self.mouse_same_cell = [-1,-1]

	def on_resize(self, width, height):
		super().on_resize(width, height)


	def on_draw(self):

		arcade.start_render()

		if len(self.nextState) == N:
			k = 0
			while k < n:
				l = 0
				while l < n:
					if self.nextState[k+n*l] == "*":
						arcade.draw_point(s*k+(s-1)/2, s*l+(s-1)/2,arcade.color.WHITE, s)
					l+=1
				k+=1
		# maybe need to strat optimizing code for a smoother simulation and a bigger game world...

		""" draw the circle/radius around the User """
		for i in range(0, len(self.User.shape_location)):
			x_index = self.User.shape_location[i][0]
			y_index = self.User.shape_location[i][1]
			
			self.draw_the_circle([x_index, y_index], [0, 255, 0])

			if (x_index<10 or x_index>=n-10) and (y_index<10 or y_index>=n-10):

				secondary_helper_location_1 = [x_index, y_index]
				secondary_helper_location_2 = [x_index, y_index]
				secondary_helper_location_3 = [x_index, y_index]

				if x_index < 10:
					secondary_helper_location_1[0] = n + x_index # x different y different
					secondary_helper_location_2[0] = n + x_index # x different y the same
					secondary_helper_location_3[0] = x_index # x the same y different # this line is technically redundant
				elif x_index >= n-10:
					secondary_helper_location_1[0] = -(n-x_index) # x different y different
					secondary_helper_location_2[0] = -(n-x_index) # x different y the same
					secondary_helper_location_3[0] = x_index # x the same y different # this line is technically redundant
				if y_index < 10:
					secondary_helper_location_1[1] = n + y_index # x different y different
					secondary_helper_location_2[1] = y_index # x different y the same
					secondary_helper_location_3[1] = n + y_index # x the same y different
				elif y_index >= n-10:
					secondary_helper_location_1[1] = -(n-y_index) # x different y different
					secondary_helper_location_2[1] = y_index # x different y the same
					secondary_helper_location_3[1] = -(n-y_index) # x the same y different

				self.draw_the_arc([secondary_helper_location_1[0], secondary_helper_location_1[1]], [0, 255, 0])
				self.draw_the_arc([secondary_helper_location_2[0], secondary_helper_location_2[1]], [0, 255, 0])
				self.draw_the_arc([secondary_helper_location_3[0], secondary_helper_location_3[1]], [0, 255, 0])

			elif (x_index<10 or x_index>=n-10) or (y_index<10 or y_index>=n-10):
				secondary_helper_location = [x_index, y_index]
				if x_index < 10:
					secondary_helper_location[0] = n + x_index
				elif x_index >= n-10:
					secondary_helper_location[0] = -(n-x_index)
				if y_index < 10:
					secondary_helper_location[1] = n + y_index
				elif y_index >= n-10:
					secondary_helper_location[1] = -(n-y_index)
				self.draw_the_arc([secondary_helper_location[0], secondary_helper_location[1]], [0, 255, 0])
		""" finished drawing the circle """

		""" import User """
		for i in range(0, len(self.User.shape_location)):
			user_x = self.User.shape_location[i][0]
			user_y = self.User.shape_location[i][1]
			if self.User.life > 0:
				arcade.draw_point(round(s*user_x+(s-1)/2), round(s*user_y+(s-1)/2), (0, 55+20*(self.User.life), 0), s)
			else:
				arcade.draw_point(round(s*user_x+(s-1)/2), round(s*user_y+(s-1)/2), (100, 107, 100), s)
		user_x = self.User.shape_location[0][0]
		user_y = self.User.shape_location[0][1]
		if self.User.life > 0:
			arcade.draw_point(round(s*user_x+(s-1)/2), round(s*user_y+(s-1)/2), (0, 55+20*(self.User.life), 0), s)
		else:
			arcade.draw_point(round(s*user_x+(s-1)/2), round(s*user_y+(s-1)/2), (100, 107, 100), s)
		""" finished importing user """

		""" display the time as an implicit score of survival """
		arcade.draw_text("realm-time of survival:: " + str(self.time), 10, 10, arcade.color.RED)

		if self.showgrid == True: # future: this could be optimized by importing a grid image as background
			self.drawgrid()

	def draw_the_circle(self, location, greenish_color):
		if self.countframes < 25:
			arcade.draw_circle_outline(s*location[0]+(s-1)/2, s*location[1]+(s-1)/2, s*10, (greenish_color[0], 26+int((self.countframes)*10)/2, greenish_color[2]), 2, 0, -1)
		elif self.countframes < 50:
			arcade.draw_circle_outline(s*location[0]+(s-1)/2, s*location[1]+(s-1)/2, s*10, (greenish_color[0], 26+(500-int((self.countframes)*10))/2, greenish_color[2]), 2, 0, -1)
		elif self.countframes < 75:
			arcade.draw_circle_outline(s*location[0]+(s-1)/2, s*location[1]+(s-1)/2, s*10, (greenish_color[0], 26+(int((self.countframes)*10)-500)/2, greenish_color[2]), 2, 0, -1)
		else: # 75 <= self.countframes < 100
			arcade.draw_circle_outline(s*location[0]+(s-1)/2, s*location[1]+(s-1)/2, s*10, (greenish_color[0], 26+(1000-int((self.countframes)*10))/2, greenish_color[2]), 2, 0, -1)

	def draw_the_arc(self, location, greenish_color):
		width = 2*s*10 # "width" of the arc, we can do this because we set the angles from 0 to 360 degress
		height = 2*s*10 # "height" of the arc, we can do this because we set the angles from 0 to 360 degress
		if self.countframes < 25:
			arcade.draw_arc_outline(int(s*location[0]+(s-1)/2), int(s*location[1]+(s-1)/2), width, height, (int(greenish_color[0]), int(26+int((self.countframes)*10)/2), int(greenish_color[2])), 0, 360, border_width = 4)
		elif self.countframes < 50:
			arcade.draw_arc_outline(int(s*location[0]+(s-1)/2), int(s*location[1]+(s-1)/2), width, height, (int(greenish_color[0]), int(26+(500-int((self.countframes)*10))/2), int(greenish_color[2])), 0, 360, border_width = 4)
		elif self.countframes < 75:
			arcade.draw_arc_outline(int(s*location[0]+(s-1)/2), int(s*location[1]+(s-1)/2), width, height, (int(greenish_color[0]), int(26+(int((self.countframes)*10)-500)/2), int(greenish_color[2])), 0, 360, border_width = 4)
		else: # 75 <= self.countframes < 100
			arcade.draw_arc_outline(int(s*location[0]+(s-1)/2), int(s*location[1]+(s-1)/2), width, height, (int(greenish_color[0]), int(26+(1000-int((self.countframes)*10))/2), int(greenish_color[2])), 0, 360, border_width = 4)

	def drawgrid(self):
		for i in range (0, n):
			arcade.draw_line(s*i, 0, s*i , n*s , (0,127,0), line_width = 1)
		for j in range (0, n):
			arcade.draw_line(0 , s*j , n*s , s*j , (0,127,0), line_width = 1)

	def cell_mouse_click(self, x_variation, y_variation):
		x = self.mouselocation_x
		y = self.mouselocation_y
		if (((self.User.shape_location[0][0] + x_variation)*s - x)**2 + ((self.User.shape_location[0][1] + y_variation)*s - y)**2) <= (s*10)**2:

			location_x = int((x - (x%s))//s) + 1
			location_y = n-1 - int((y - (y%s))//s) + 1
			location_translated = (n-location_y + 1)*n - (n - location_x + 1)

			if self.mouse_same_cell != [location_x, location_y]:
				if self.nextState[location_translated] == " ":
					self.nextState[location_translated] = "*"
					self.mouse_same_cell = [location_x, location_y]
				else:
					self.nextState[location_translated] = " "
					self.mouse_same_cell = [location_x, location_y]

	def on_update(self, delta_time):

		if self.paused == False:
			self.time += 1

		# use update_most_type_locations in order to
		# keep track of the most right,left,top,bottom indexed locations of player
		# right now the user is just one cell, therefore does not matter much for now,,,
		self.User.update_most_type_locations()

		if self.countframes >= 100:
			self.countframes = 0

		if self.paused == False: # if sim is not paused toggled by "P" key,,,

			self.nextState = create_next_state_planet_research(self.nextState)
			
			##########___This section creates randomized appearance with low probability___##########
			# (completed) task 1:: randomized events -- meaningfully -- probabilistically::
			# (completed) task 2:: work on setting seeds 'meaningfully' -- fractally -- too -lg
			# (completed) task 3:: need to make it a chunk (not a line) -- key use modular arithmetic
			if random.randint(0, 100) <= 36.7: # assuming seed to be uniform:: 36.7 % chance::

				# chunk 1 is completely random within the planet realm
				chunk1 = 33 # total size in count of the chunk, probablistically
				chunk1Side = int(math.sqrt(chunk1))  # approx side length of the chunk square
				lowerbound1 = random.randint(0, N-chunk1Side)
				upperbound1 = lowerbound1 + chunk1Side
				for s in range(0, chunk1Side):
					for i in range(lowerbound1 + s*n, upperbound1 + s*n): # end index is exclusive by python
						choice = random.randint(0, 100)
						if (choice > chunk1):
							self.nextState[i % N] = " "
						else:  # i.e. choice == 1::
							self.nextState[i % N] = "*"

				# chunk 2 must happen "near" chunk 1 and is smaller by factor of e
				chunk2 = int(chunk1/math.e);
				chunk2Side = int(math.sqrt(chunk2))
				lowerbound2 = random.randint(0, lowerbound1 - chunk2Side)
				upperbound2 = lowerbound2 + chunk2Side
				for s in range(0, chunk2Side):
					for i in range(lowerbound2 + s*n, upperbound2 + s*n):  # end index is exclusive by python
						choice = random.randint(0, 100)
						if (choice > chunk2):
							self.nextState[i % N] = " "
						else:  # i.e. choice == 1::
							self.nextState[i % N] = "*"

				# chunk 3 must happen "near" chunk 2 and is smaller by factor of e
				chunk3 = int(chunk2/math.e);
				chunk3Side = int(math.sqrt(chunk3))
				lowerbound3 = random.randint(0, lowerbound2 - chunk3Side)
				upperbound3 = lowerbound3 + chunk3Side
				for s in range(0, chunk3Side):
					for i in range(lowerbound3 + s*n, upperbound3 + s*n):  # end index is exclusive by python
						choice = random.randint(0, 100)
						if (choice > chunk3):
							self.nextState[i % N] = " "
						else:  # i.e. choice == 1::
							self.nextState[i % N] = "*"

			if self.User.life > 0:
				user_location = self.User.shape_location[0][0] + n*self.User.shape_location[0][1]
				if self.nextState[user_location] == " ":
					self.nextState[self.User.shape_location[0][0] + n*self.User.shape_location[0][1]] = "*"
				else:
					self.User.life -= 1
					self.nextState[self.User.shape_location[0][0] + n*self.User.shape_location[0][1]] = "*"

		# Mouse Press #
		if self.mouse_press == True:
			self.cell_mouse_click(0, 0)
			self.cell_mouse_click(0, -n)
			self.cell_mouse_click(0, n)
			self.cell_mouse_click(-n, 0)
			self.cell_mouse_click(-n, -n)
			self.cell_mouse_click(-n, n)
			self.cell_mouse_click(n, 0)
			self.cell_mouse_click(n, -n)
			self.cell_mouse_click(n, n)

		# Accelerated Movements #
		if self.right_press and (abs(self.right_save_count - self.countframes) >= 0):
			for i in range(0, len(self.User.shape_location)):
				self.User.shape_location[i][0] = (self.User.shape_location[i][0] + 1)%n
			self.User.update_most_type_locations()

		if self.left_press and (abs(self.left_save_count - self.countframes) >= 0):
			for i in range(0, len(self.User.shape_location)):
				self.User.shape_location[i][0] = (self.User.shape_location[i][0] - 1)%n
				self.User.update_most_type_locations()

		if self.up_press and (abs(self.up_save_count - self.countframes) >= 0):
			for i in range(0, len(self.User.shape_location)):
				self.User.shape_location[i][1] = (self.User.shape_location[i][1] + 1)%n
				self.User.update_most_type_locations()

		if self.down_press and (abs(self.down_save_count - self.countframes) >= 0):
			for i in range(0, len(self.User.shape_location)):
				self.User.shape_location[i][1] = (self.User.shape_location[i][1] - 1)%n
				self.User.update_most_type_locations()

		################################################################################
		# "Blink" Movements or "skipping" where you double click and you jump
		# Disclaimer: If the User shape is more than just a single cell, will cause disfiguration
		if self.right_press and self.right_press_double == 2:
			for i in range(0, len(self.User.shape_location)):
				self.User.shape_location[i][0] = (self.User.shape_location[i][0] + 10)%n
				self.User.update_most_type_locations()
			self.right_press_double = 0

		if self.left_press and self.left_press_double ==2:
			for i in range(0, len(self.User.shape_location)):
				self.User.shape_location[i][0] = (self.User.shape_location[i][0] - 10)%n
				self.User.update_most_type_locations()
			self.left_press_double = 0

		if self.up_press and self.up_press_double == 2:
			for i in range(0, len(self.User.shape_location)):
				self.User.shape_location[i][1] = (self.User.shape_location[i][1] + 10)%n
				self.User.update_most_type_locations()
			self.up_press_double = 0

		if self.down_press and self.down_press_double == 2:
			for i in range(0, len(self.User.shape_location)):
				self.User.shape_location[i][1] = (self.User.shape_location[i][1] - 10)%n
				self.User.update_most_type_locations()
			self.down_press_double = 0
		#################################################################################

		self.countframes += 1

	################################################################################
	############################___Key_Controls___##################################
	################################################################################
	def on_key_press(self, key, key_modifiers):

		# Pause
		if key==arcade.key.P or key==arcade.key.SPACE:
			if self.paused == False:
				self.paused = True
			else:
				self.paused = False

		# Clear::
		if key == arcade.key.C:
			cleared = []
			for i in range(0, N):
				cleared.append(" ")
			self.nextState = cleared

		# Randomize the world::
		elif key == arcade.key.R:
			randomized = []
			for i in range(0, N):
				choice = random.randint(0, 1)
				if (choice == 0):
					randomized.append(" ")
				else: # i.e. choice == 1::
					randomized.append("*")
			self.nextState = randomized

		# toggle grid lines
		if key == arcade.key.G:
			if self.showgrid == False:
				self.showgrid = True
			else:
				self.showgrid = False

		# User Movement #
		if key==arcade.key.D or key==arcade.key.RIGHT:

			# before right_save_count gets updated, use it for double click jumps
			if self.right_press_double == 0:
				self.right_press_double = 1
			elif self.right_press_double == 1:
				if abs(self.right_save_count - self.countframes)<3:
					self.right_press_double = 2

			# update right_save_count
			if self.right_press == False:
				self.right_save_count = self.countframes
			self.right_press = True

		if key==arcade.key.A or key==arcade.key.LEFT:

			# before left_save_count gets updated, use it for double click jumps
			if self.left_press_double == 0:
				self.left_press_double = 1
			elif self.left_press_double == 1:

				if abs(self.left_save_count - self.countframes)<3:
					self.left_press_double = 2

			if self.left_press == False:
				self.left_save_count = self.countframes
			self.left_press = True

		if key==arcade.key.W or key==arcade.key.UP:

			# before up_save_count gets updated, use it for double click jumps
			if self.up_press_double == 0:
				self.up_press_double = 1
			elif self.up_press_double == 1:
				if abs(self.up_save_count - self.countframes)<3:
					self.up_press_double = 2
			if self.up_press == False:
				self.up_save_count = self.countframes
			self.up_press = True

		if key==arcade.key.S or key==arcade.key.DOWN:

			# before right_save_count gets updated, use it for double click jumps
			if self.down_press_double == 0:
				self.down_press_double = 1
			elif self.down_press_double == 1:
				if abs(self.down_save_count - self.countframes)<3:
					self.down_press_double = 2
			if self.down_press == False:
				self.down_save_count = self.countframes
			self.down_press = True

		# Exit Game #
		if key == arcade.key.ESCAPE:
			self.close()

	def on_key_release(self, key, key_modifiers):

		if key==arcade.key.D or key==arcade.key.RIGHT:
			#self.right_press_once = False
			self.right_press = False

		if key==arcade.key.A or key==arcade.key.LEFT:
			#self.left_press_once = False
			self.left_press = False

		if key==arcade.key.W or key==arcade.key.UP:
			#self.up_press_once = False
			self.up_press = False

		if key==arcade.key.S or key==arcade.key.DOWN:
			#self.down_press_once = False
			self.down_press = False

		if key == arcade.key.ESCAPE:
			self.close()

	def on_mouse_motion(self, x, y, delta_x, delta_y):
		self.mouselocation_x = x
		self.mouselocation_y = y

	def on_mouse_press(self, x, y, button, key_modifiers):
		self.mouselocation_x = x
		self.mouselocation_y = y
		self.mouse_press = True

	def on_mouse_release(self, x, y, button, key_modifiers):
		self.mouse_press = False
		# reset mouse_same_cell
		self.mouse_same_cell = [-1, -1]


def main():
	simulation = OfLifeSimulation(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
	simulation.setup()
	for i in range(0,2):
		simulation.switch_to()
	arcade.run()

if __name__ == "__main__":
	main()
