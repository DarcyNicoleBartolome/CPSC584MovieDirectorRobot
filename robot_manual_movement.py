from picrawler import Picrawler
from time import sleep
import readchar

crawler = Picrawler()
speed = 90

LENGTH_SIDE = 77
X_DEFAULT = 45
X_TURN = 70
X_START = 0
Y_DEFAULT = 45
Y_TURN = 130
Y_WAVE =120
Y_START = 0 
Z_DEFAULT = -50
Z_UP = -30
Z_WAVE = 60
Z_TURN = -40
Z_PUSH = -76

manual = '''
Press keys on keyboard to control PiCrawler!
    W: Forward
    A: Turn left
    S: Backward
    D: Turn right

    Ctrl^C: Quit
'''

def show_info():
    print("\033[H\033[J",end='')  # clear terminal windows
    print(manual)


def move_sideLeft(speed, current):
   crawler.do_step('stand', speed)
   ## [right front],[left front],[left rear],[right rear]
   
   
   
   crawler.stand_position = crawler.stand_position + 1 & 1
   
   # forward(self):
   forward =  [
      [[X_DEFAULT, Y_DEFAULT, current[0][2]],[X_TURN, Y_START,Z_UP],[X_DEFAULT, Y_START, current[2][2]],[X_DEFAULT, Y_DEFAULT, current[3][2]]],
      [[X_DEFAULT, Y_DEFAULT, current[0][2]],[X_DEFAULT, Y_DEFAULT*2,Z_UP],[X_DEFAULT, Y_START, current[2][2]],[X_DEFAULT, Y_DEFAULT, current[3][2]]],
      [[X_DEFAULT, Y_DEFAULT, current[0][2]],[X_DEFAULT, Y_DEFAULT*2,current[1][2]],[X_DEFAULT, Y_START, current[2][2]],[X_DEFAULT, Y_DEFAULT, current[3][2]]],
      [[X_DEFAULT, Y_START, current[0][2]],[X_DEFAULT, Y_DEFAULT,current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_DEFAULT, Y_DEFAULT*2, current[3][2]]],
      
      [[X_DEFAULT, Y_START, current[0][2]],[X_DEFAULT, Y_DEFAULT,current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_DEFAULT, Y_DEFAULT*2, Z_UP]],
      [[X_DEFAULT, Y_START, current[0][2]],[X_DEFAULT, Y_DEFAULT,current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_TURN, Y_START, Z_UP]],
      [[X_DEFAULT, Y_START, current[0][2]],[X_DEFAULT, Y_DEFAULT,current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_DEFAULT, Y_START, current[3][2]]],
   ]
   
   current = [[X_DEFAULT, Y_START, current[0][2]],[X_DEFAULT, Y_DEFAULT,current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_DEFAULT, Y_START, current[3][2]]]
   
   left =  [
      ## [right front],[left front],[left rear],[right rear]
      # [[X_DEFAULT, Y_DEFAULT, current[0][2]],[X_START, Y_TURN,Z_UP],[X_DEFAULT, Y_START, current[2][2]],[X_DEFAULT, Y_DEFAULT, current[3][2]]],
      [[X_DEFAULT, Y_DEFAULT, current[0][2]],[X_DEFAULT, Y_DEFAULT, current[1][2]],[X_START, -Y_TURN,Z_UP],[X_DEFAULT, Y_START, current[3][2]]],
      
      # [[X_DEFAULT, Y_DEFAULT, current[0][2]],[X_DEFAULT, Y_DEFAULT*2,Z_UP],[X_DEFAULT, Y_START, current[2][2]],[X_DEFAULT, Y_DEFAULT, current[3][2]]],
      [[X_DEFAULT, Y_DEFAULT, current[0][2]],[X_DEFAULT, Y_DEFAULT, current[1][2]],[X_DEFAULT, Y_DEFAULT*2,Z_UP],[X_DEFAULT, Y_START, current[3][2]]],
      
      # [[X_DEFAULT, Y_DEFAULT, current[0][2]],[X_DEFAULT, Y_DEFAULT*2,current[1][2]],[X_DEFAULT, Y_START, current[2][2]],[X_DEFAULT, Y_DEFAULT, current[3][2]]],
      [[X_DEFAULT, Y_DEFAULT, current[0][2]],[X_DEFAULT, Y_DEFAULT, current[1][2]],[X_DEFAULT, Y_DEFAULT*2,current[2][2]],[X_DEFAULT, Y_START, current[3][2]]],
      
      # [[X_DEFAULT, Y_START, current[0][2]],[X_DEFAULT, Y_DEFAULT,current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_DEFAULT, Y_DEFAULT*2, current[3][2]]],
      [[X_DEFAULT, Y_DEFAULT*2, current[0][2]],[X_DEFAULT, Y_START, current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_DEFAULT, Y_DEFAULT, current[3][2]]],
      
      # [[X_DEFAULT, Y_START, current[0][2]],[X_DEFAULT, Y_DEFAULT,current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_DEFAULT, Y_DEFAULT*2, Z_UP]],
      [[X_DEFAULT, Y_DEFAULT*2, Z_UP],[X_DEFAULT, Y_START, current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_DEFAULT, Y_DEFAULT, current[3][2]]],
      
      # [[X_DEFAULT, Y_START, current[0][2]],[X_DEFAULT, Y_DEFAULT,current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_TURN, Y_START, Z_UP]],
      [[X_DEFAULT, Y_START, Z_UP],[X_DEFAULT, Y_START, current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_DEFAULT, Y_DEFAULT, current[3][2]]],
      
      # [[X_DEFAULT, Y_START, current[0][2]],[X_DEFAULT, Y_DEFAULT,current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_DEFAULT, Y_START, current[3][2]]],
      [[X_DEFAULT, Y_START, current[0][2]],[X_DEFAULT, Y_START, current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_DEFAULT, Y_DEFAULT, current[3][2]]],
   ]
   
   left_forward = [
      [[X_DEFAULT, Y_DEFAULT, current[0][2]],[X_DEFAULT, Y_DEFAULT, current[1][2]],[X_START, Y_TURN, Z_UP],[X_DEFAULT, Y_START, current[3][2]]],
      [[X_DEFAULT, Y_DEFAULT, current[0][2]],[X_DEFAULT, Y_DEFAULT, current[1][2]],[X_DEFAULT, Y_DEFAULT*3,Z_UP],[X_DEFAULT, Y_START, current[3][2]]],
   ]
   
   current = [[X_DEFAULT, Y_START, current[0][2]],[X_DEFAULT, Y_DEFAULT,current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_DEFAULT, Y_START, current[3][2]]]
   

   # for coord in stand:
   #    crawler.do_step(coord, speed)
   
   # for coord in forward:
   #    crawler.do_step(coord, speed)
   #    print(coord)
   #    sleep(3)
      
   for coord in left_forward:
      crawler.do_step(coord, speed)
      sleep(1)
      crawler.do_step(coord, speed)
      sleep(1)
      crawler.do_step(coord, speed)
      print(coord)
   
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

def moveUp(speed, current):
   forward =  [
      [[X_DEFAULT, Y_DEFAULT, current[0][2]],[X_TURN, Y_START,Z_UP],[X_DEFAULT, Y_START, current[2][2]],[X_DEFAULT, Y_DEFAULT, current[3][2]]],
      [[X_DEFAULT, Y_DEFAULT, current[0][2]],[X_DEFAULT, Y_DEFAULT*2,Z_UP],[X_DEFAULT, Y_START, current[2][2]],[X_DEFAULT, Y_DEFAULT, current[3][2]]],
      [[X_DEFAULT, Y_DEFAULT, current[0][2]],[X_DEFAULT, Y_DEFAULT*2,current[1][2]],[X_DEFAULT, Y_START, current[2][2]],[X_DEFAULT, Y_DEFAULT, current[3][2]]],
      [[X_DEFAULT, Y_START, current[0][2]],[X_DEFAULT, Y_DEFAULT,current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_DEFAULT, Y_DEFAULT*2, current[3][2]]],
      
      [[X_DEFAULT, Y_START, current[0][2]],[X_DEFAULT, Y_DEFAULT,current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_DEFAULT, Y_DEFAULT*2, Z_UP]],
      [[X_DEFAULT, Y_START, current[0][2]],[X_DEFAULT, Y_DEFAULT,current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_TURN, Y_START, Z_UP]],
      [[X_DEFAULT, Y_START, current[0][2]],[X_DEFAULT, Y_DEFAULT,current[1][2]],[X_DEFAULT, Y_DEFAULT, current[2][2]],[X_DEFAULT, Y_START, current[3][2]]],
   ]
   
   for coord in forward:
      crawler.do_step(coord, speed)
      sleep(1)

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
    
    current_pose = [
        [45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]
    ] # Set the current pose to stand
    
    show_info()
    
    while True:
        key = readchar.readkey()
        key = key.lower()
        if key in('wsadqezcrf'):
           if 'a' == key: # move sideway left
              move_sideLeft(speed, current_pose)
              
           if 'd' == key: # move sideway right
              move_sideRight(speed)
              
           if 'r' == key: # move sideway right
              lookUp()
           if 'f' == key: # move sideway right
              lookDown()
              
           if 'w' == key: # move sideway right
              moveUp(speed, current_pose)
            
if __name__ == "__main__":
    main()