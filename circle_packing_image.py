import pygame
from random import randint
from random import choice
from math import hypot
import sys

if len(sys.argv) != 2:
	print "Image missing in argument!!!"
	print "Exemple : 'python "+sys.argv[0]+ " images/python_logo.png'"
	exit()

# width and hight depend on the image that you load
W = 1080 # window width
H = 720  # window hight
FPS = 60 # frames per second

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CUSTOM_DARK_BLACK = (21, 18, 14)
CUSTOM_MEDIUM_BLACK = (33, 29, 22)
CUSTOM_LIGHT_BLACK = (56, 49, 38)

# beginning stage of radius when circle start growing
startRadius = 2

# how many circle start growing at the same time
# if you increase, the radius of circles decrease
totalCirclePerFrame = 100

# gap between circles, if 0 every circles are touching other circles around
gapsBetweenCircles = 2

attemptCount = 0
attempt = 1000

# fil the circle with the color you chose
# if fillCircle == 0, fill the rectangle
# if fillCircle > 0,  used for line thickness
# if fillCircle < 0,  nothing will be drawn
fillCircle = 0

# fill circle color
color = CUSTOM_DARK_BLACK

# background color
background = CUSTOM_MEDIUM_BLACK

# if you want background as transparent make it true
backgroundTransparent = False

# hightlight text color
hightlight = CUSTOM_LIGHT_BLACK

# if you want to hightlight the text make it True
hightlightText = False

# text that you want to draw circles
text = 'HI'

# font size
textSize = 500

# font name
font = 'Comic Sans MS'


class Circle:
	def __init__(self, x, y, color, r = startRadius):
		self.x = x # position x
		self.y = y # position y
		self.r = r # radius of circle
		self.color = color
		self.growing = True
	def getPos(self): # return position (array)
		return [self.x, self.y]
	def grow(self): # every itaration the circle grow 1 pixel
		if self.growing:
			self.r+=1
	def isEdges(self): # check if the circle touching window edges
		return self.x + self.r >= W or self.x - self.r <= 0 or self.y + self.r >= H or self.y - self.r <= 0
 
pygame.init()
 
# Set the height and width of the screen
image = pygame.image.load(sys.argv[1])
size = image.get_rect().size
W, H = size
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Circle Packing")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# array of circle(object)
circles = []


screen.fill((0,0,0))
screen.blit(image, image.get_rect())
screensurf = pygame.display.get_surface()
pixels = []
for y in range(0, H):
	for x in range(0, W):
		pixels.append(screensurf.get_at((x,y)))
 
# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
				print "Saving File."
				if backgroundTransparent:
					image = pygame.Surface((W, H), pygame.SRCALPHA, 32)
					image = image.convert_alpha()
				else:
					image = pygame.Surface((W, H))
					pygame.draw.rect(image, background, [0, 0, W, H])
				for c in circles:
					pygame.draw.circle(image, (c.color[0], c.color[1], c.color[2]), c.getPos(), c.r, fillCircle)
				pygame.image.save(image, "circle_packing.png")
				print "Done"
 
    # --- Drawing
    # Set the screen background
    screen.fill(background)
    if hightlightText: screen.blit(textsurface,(W/2-text_width/2,H/2-text_height/2))
    count = 0
    while(count != totalCirclePerFrame):
		valid = True
		x = randint(0,W-1)
		y = randint(0,H-1)
		for c in circles:
			dist = hypot(x-c.x, y-c.y)
			if dist < c.r + gapsBetweenCircles:
				valid = False
				break
		if valid:
			circles.append(Circle(x, y, pixels[y * W + x]))
			count+=1
		attemptCount += 1
		if attemptCount >= attempt:
			count = totalCirclePerFrame
			
    # Draw the circle
    for c in circles:
    	pygame.draw.circle(screen, (c.color[0], c.color[1], c.color[2]), c.getPos(), c.r, fillCircle)
    	if c.isEdges():
    		c.growing = False
    	elif c.growing:
    		for other in circles:
    			if other != c:
    				dist = hypot(c.x-other.x, c.y-other.y)
    				if(dist - gapsBetweenCircles < c.r + other.r):
    					c.growing = False
    					break
    	c.grow()
 
    # --- Wrap-up
    # frames per second
    clock.tick(FPS)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Close everything down
pygame.quit()
