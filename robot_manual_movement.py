from picrawler import Picrawler
from time import sleep
import readchar

crawler = Picrawler()
speed = 90

leg_mode = 0

# LENGTH_SIDE = 77
# X_DEFAULT = 35
# X_TURN = 70
# X_START = 0
# Y_DEFAULT = 35
# Y_TURN = 130
# Y_WAVE =120
# Y_START = 0 
# Z_DEFAULT = -50
# Z_UP = -30
# Z_WAVE = 60
# Z_TURN = -40
# Z_PUSH = -76

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
    A: Side Move left 
    S: Backward
    D: Side Move right
    R: Look Up
    F: Look Down
    P: Stand

    Ctrl^C: Quit
'''

def show_info():
    print("\033[H\033[J",end='')  # clear terminal windows
    print(manual)

# def normal_action(mode):
#    _action = []
#    if stand_position == 0:
#       _action += func(self)
#    else:
#       temp = func(self)
#       new_step = []
#       for step in temp:
#             if mode == 0:
#                new_step = [step[1], step[0], step[3], step[2]]
#             elif mode == 1:
#                new_step = [step[2], step[3], step[0], step[1]]
#             _action += [new_step]
#    return _action

def stand(speed, current): # make the robot stand up
   test = [i for i in current]
   i = 0 # counter
   for leg in test:
      if leg[2] != Z_DEFAULT:
          test[i][2] = Z_DEFAULT
          i += 1

   crawler.do_step(test, speed)

def move_sideLeft(speed, current):
   global leg_mode
   ## [right front],[left front],[left rear],[right rear]
   
   stand(speed, current)
   
   crawler.stand_position = crawler.stand_position + 1 & 1
   current = crawler.current_step_all_leg_value()
   
   # crawler.do_step(current, speed
   
   left_backleg_move =  [
      ## [right front],[left front],[left rear],[right rear]
      
      # Lifts the left rear leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_START, X_TURN, Z_UP],[Y_START, X_DEFAULT, Z_DEFAULT]], 
      
      # move the left rear leg to the left
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT, Z_UP],[Y_START, X_DEFAULT, Z_DEFAULT]],
      
      # Put down the left rear leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT,Z_DEFAULT],[Y_START, X_DEFAULT, Z_DEFAULT]],
      
      # Move the rest legs to the leg
      [[Y_DEFAULT*2.5, X_DEFAULT, Z_DEFAULT],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      # [[Y_DEFAULT-30, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_START, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # Lift the right front leg up
      [[Y_DEFAULT*2.5, X_DEFAULT, Z_UP],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT]],
      # [[Y_DEFAULT-30, X_DEFAULT, Z_UP],[Y_DEFAULT, X_START, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT]],
      
      # Move the right front leg to the left
      [[X_START, Y_DEFAULT, Z_UP],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # # Put down the right front rear leg
      [[X_START, X_TURN, Z_DEFAULT],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # [[X_START, X_TURN, Z_UP],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
   ]
   
   # new_step = [left_backleg_move[2], left_backleg_move[3], left_backleg_move[0], left_backleg_move[1]]
   
   left_frontleg_move =  [
      ## [right front],[left front],[left rear],[right rear]
      # [coord[1], coord[2], coord[3], coord[0]]
      
      # Lifts the right front leg
      [[X_START, X_TURN, Z_DEFAULT],[Y_START, X_TURN, Z_UP],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # move the right front leg to the left
      [[X_START, X_TURN, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT, Z_UP],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # Put down the right front leg
      [[X_START, X_TURN, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # Move the rest legs to the leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT, Z_DEFAULT]],
      
      # Lift the left back leg up
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_START, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT, Z_UP]],
      
      # Move the left back leg to the left
      [[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_START, X_DEFAULT, Z_DEFAULT],[X_START, Y_DEFAULT, Z_UP]],
      
      # # Put down the left back leg
      # [[X_START, Y_DEFAULT, Z_DEFAULT],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_START, Y_DEFAULT, Z_DEFAULT],[X_START, X_DEFAULT, Z_DEFAULT],[Y_START, X_DEFAULT, Z_DEFAULT]], 
   ]
   
   if leg_mode == 0:
      for coord in left_backleg_move:
         crawler.do_step(coord, speed)
         # sleep(1)
         print(coord)
      leg_mode = 1
   else:     
      for coord in left_frontleg_move:
         # new_step = [coord[1], coord[2], coord[3], coord[0]]
         # crawler.do_step(new_step, speed)
         crawler.do_step(coord, speed)
         # sleep(1)
         print(coord)
      leg_mode = 0
   
   
def move_sideRight(speed, current):
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
   
   crawler.do_action('forward', 1, speed)
   
   # Forward with left leg
   # forward =  [
   #    [[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[X_TURN, Y_START,Z_UP],[X_DEFAULT, Y_START, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
   #    [[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT*2,Z_UP],[X_DEFAULT, Y_START, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
   #    [[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT*2,Z_DEFAULT],[X_DEFAULT, Y_START, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
   #    [[X_DEFAULT, Y_START, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT,Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT*2, Z_DEFAULT]],
      
   #    [[X_DEFAULT, Y_START, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT,Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT*2, Z_UP]],
   #    [[X_DEFAULT, Y_START, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT,Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[X_TURN, Y_START, Z_UP]],
   #    [[X_DEFAULT, Y_START, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT,Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_START, Z_DEFAULT]],
   # ]
   
   # for coord in forward:
   #    crawler.do_step(coord, speed)
   #    sleep(1)
   #    print(coord)

def moveDown(speed, current):
   pass

def lookUp(speed, current):
   # spider.do_action('look_up', speed=60)
   # setup = [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]]
   # crawler.do_step(setup, speed)
   
   # if current != [[45, 45, -76], [45, 0, -76], [45, 0, -38], [45, 45, -30]]:
   #    new_step = [[45, 45, (-50 - inc)], [45, 0, (-50 - inc)], [45, 0, (-50 + inc)], [45, 45, (-50 + inc)]]
   
   coords = [
      # stand
      [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
      [[45, 45, -76], [45, 0, -76], [45, 0, -38], [45, 45, -30]],
      # Note when we want to change the speed / look up speed
      # Right and left front has larger - while rl rear has less
   ]



   for coord in coords:
      crawler.do_step(coord, speed)


def lookDown(speed, current):
   # spider.do_action('look_down', speed=60)
    coords = [
        # stand
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -28], [45, 0, -40], [45, 0, -68], [45, 45, -76]],
      #   [[45, 45, -76], [45, 0, -76], [45, 0, -38], [45, 45, -30]], # Test this version similar to look up but opposite
    ]
    for coord in coords:
        crawler.do_step(coord, speed)

def main():
   speed = 90
    
   #  current_pose = [
   #      [45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]
   #  ] # Set the current pose to stand
   
   crawler.do_action('forward', 1, speed)
      
   current_pose = crawler.current_step_all_leg_value()
    
   show_info()
   
   while True:
      key = readchar.readkey()
      key = key.lower()
      current_pose = crawler.current_step_all_leg_value()
      if key in('wsadqezcrfpz'):
         if 'a' == key: # move sideway left
            move_sideLeft(speed, current_pose)
            
         if 'd' == key: # move sideway right
            move_sideRight(speed, current_pose)
            
         if 'r' == key: # move sideway right
            lookUp(speed, current_pose)
         if 'f' == key: # move sideway right
            lookDown(speed, current_pose)
            
         if 'w' == key: # move sideway right
            moveUp(speed, current_pose)
            
         if 'p' == key: # move sideway right
            crawler.do_step('stand', speed)
            
if __name__ == "__main__":
    main()