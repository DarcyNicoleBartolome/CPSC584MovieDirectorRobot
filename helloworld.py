from picrawler import Picrawler
from time import sleep

crawler = Picrawler()

def main():
    speed = 80

    #* ---- Move in a square ----
    for _ in range(4):
        crawler.do_action('forward', 10, speed)   # go straight
        sleep(0.1)
        crawler.do_action('turn right', 2, speed)  # 90° turn
        sleep(0.1)

    # * Testing Right arm Pose
    # ---- Stop in stand position ----
    # new_stand = [[45, 45, -75], [45, 45, -75], [45, 45, -75], [45, 45, -75]]
    # crawler.do_step(new_stand, speed)
    # sleep(1)
    
    # crawler.do_step("stand", speed)
    # sleep(1)

    # ---- Raise front RIGHT arm ----
    # right_arm_up = [[45, 45, 90], [45, 45, -65] , [45, 45, -65], [45, 45, -65]]
    # crawler.do_step(right_arm_up, speed)
    # sleep(2) 

    #* Lower right arm (back to stand)
    crawler.do_step('stand', speed)
    sleep(1)

    #* ---- Raise front LEFT arm ----
    left_arm_up = [[45, 45, -75], [45, 45, 80], [45, 0, -75], [45, 45, -75]]
    crawler.do_step(left_arm_up, speed)
    for _ in range(2):
        left_arm_up = [[45, 45, -75], [45, 65, 80], [45, 0, -75], [45, 45, -75]]
        crawler.do_step(left_arm_up, speed)
        left_arm_up = [[45, 45, -75], [45, 25, 80], [45, 0, -75], [45, 45, -75]]
        crawler.do_step(left_arm_up, speed)
        left_arm_up = [[45, 45, -75], [45, 45, 80], [45, 0, -75], [45, 45, -75]]
        crawler.do_step(left_arm_up, speed)
    sleep(2)

    #* Lower left arm (back to stand)
    crawler.do_step('stand', speed)


if __name__ == "__main__":
    main()
