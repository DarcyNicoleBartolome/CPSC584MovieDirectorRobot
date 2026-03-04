from picrawler import Picrawler
from time import sleep

crawler = Picrawler()

def move_sideLeft(speed):
   crawler.do_step('stand', speed)
   ## [right front],[left front],[left rear],[right rear]
   
   stand = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
    ]
   
   look_left = [
      #   [[45, 0, -50], [45, 45, -50], [45, 45, -50], [45, 0, -50]],
      #   [[0, 45, -50], [45, 45, -50], [45, 45, -50], [45, 0, -50]],
      #   [[0, 45, -50], [45, 45, -35], [45, 45, -50], [45, 0, -50]],
      [[0, 45, -50], [45, 0, -50], [0, 45, -50], [45, 0, -50]],
      [[45, 0, -50], [0, 45, -50], [45, 0, -50], [0, 45, -50]],
    ]

   for coord in stand:
      crawler.do_step(coord, speed)
   for coord in look_left:
      crawler.do_step(coord, speed)
   
def move_sideRight(speed):
   crawler.do_step('stand', speed)
   return

def move_rotateLeftBack():
   pass
   
def move_rotateRightBack():
   pass
   
def rotateLeftFront():
   pass

def rotateRightFront():
   pass

def moveUp():
   pass

def moveDown():
   pass

def lookUp():
   # spider.do_action('look_up', speed=60)
   coords = [
      # stand
      [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
      [[45, 45, -76], [45, 0, -76], [45, 0, -38], [45, 45, -30]],
   ]

   for coord in coords:
      crawler.do_step(coord, 60)


def lookDown():
   # spider.do_action('look_down', speed=60)
    coords = [
        # stand
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -28], [45, 0, -40], [45, 0, -68], [45, 45, -76]],
    ]
    for coord in coords:
        crawler.do_step(coord, 60)

def main():
    speed = 90
    
    show_info()
    while True:
        key = readchar.readkey()
        key = key.lower()
        if key in('wsadqezcrf'):
           if 'a' == key: # move sideway left
              move_sideLeft(speed)
              
           if 'd' == key: # move sideway right
              move_sideRight(speed)
              
           if 'r' == key: # move sideway right
              lookUp()
           if 'f' == key: # move sideway right
              lookDown()
            
              
