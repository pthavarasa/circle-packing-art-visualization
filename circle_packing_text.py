import pygame
from random import randint
from random import choice
from math import hypot
 
W = 1080 # window width
H = 720  # window hight
FPS = 10 # frames per second

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CUSTOM_DARK_BLACK = (21, 18, 14)
CUSTOM_MEDIUM_BLACK = (33, 29, 22)
CUSTOM_LIGHT_BLACK = (56, 49, 38)
CUSTOM_ORANGE = (255, 166, 0)
CUSTOM_LIGHT_ORANGE = (255, 176, 0)

# beginning stage of radius when circle start growing
startRadius = 2

# how many circle start growing at the same time
# if you increase, the radius of circles decrease
totalCirclePerFrame = 20

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
color = CUSTOM_LIGHT_BLACK

# background color
background = CUSTOM_LIGHT_ORANGE

# if you want background as transparent make it true
backgroundTransparent = False

# hightlight text color
hightlight = CUSTOM_LIGHT_BLACK

# if you want to hightlight the text make it True
hightlightText = False

# text that you want to draw circles
text = 'RAJI'

# font size
textSize = 400

# font name
font = 'Comic Sans MS'


class Circle:
	def __init__(self, x, y, r = startRadius):
		self.x = x # position x
		self.y = y # position y
		self.r = r # radius of circle
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
size = [W, H]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Circle Packing")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# array of circle(object)
circles = []


pygame.font.init()
# if you want to do more check the doc
# https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont
myfont = pygame.font.SysFont(font, textSize)
text_width, text_height = myfont.size(text)
textsurface = myfont.render(text, True, hightlight)
screen.fill(BLACK)
screen.blit(textsurface,(W/2-text_width/2,H/2-text_height/2))
pixels = []
hightlightAlph = (hightlight[0],hightlight[1],hightlight[2],255)
for x in range(0, W):
	for y in range(0, H):
		if screen.get_at((x, y)) == hightlightAlph:
			pixels.append([x,y])

 
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
					pygame.draw.circle(image, color, c.getPos(), c.r, fillCircle)
				pygame.image.save(image, "circle_packing.png")
				print "Done"
 
    # --- Drawing
    # Set the screen background
    screen.fill(background)
    if hightlightText: screen.blit(textsurface,(W/2-text_width/2,H/2-text_height/2))
    count = 0
    while(count != totalCirclePerFrame):
		valid = True
		x, y = choice(pixels)
		for c in circles:
			dist = hypot(x-c.x, y-c.y)
			if dist < c.r + gapsBetweenCircles:
				valid = False
				break
		if valid:
			circles.append(Circle(x, y))
			count+=1
		attemptCount += 1
		if attemptCount >= attempt:
			count = totalCirclePerFrame
			
    # Draw the circle
    for c in circles:
    	pygame.draw.circle(screen, color, c.getPos(), c.r, fillCircle)
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
