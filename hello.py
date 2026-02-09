from picrawler import Picrawler
from time import sleep

crawler = Picrawler()

new_step=[[45, 45, -75], [45, 0, -75], [45, 0, -30], [45, 45, -75]]
stand_step = crawler.move_list['stand'][0]

def main():

    speed = 80

    while True:
       
        crawler.do_action('forward',10,speed)
        sleep(0.05)
        
        crawler.do_action('turn left',2,speed)
      #   crawler.do_action('turn left',2,speed)
        sleep(0.05)
        crawler.do_action('forward',10,speed)
        sleep(0.05)
        
        crawler.do_action('turn left',2,speed)
      #   crawler.do_action('turn left',2,speed)
        sleep(0.05)
        crawler.do_action('forward',10,speed)
        sleep(0.05)
        
        crawler.do_action('turn left',2,speed)
      #   crawler.do_action('turn left',2,speed)
        sleep(0.05)
        crawler.do_action('forward',10,speed)
        sleep(0.05)
        
        crawler.do_action('turn left',2,speed)
      #   crawler.do_action('turn left',2,speed)
        
        print(f"stand step: {stand_step}")
        crawler.do_step(stand_step, speed)
        sleep(3)
        
        print(f"new step: {new_step}")
        crawler.do_step(new_step,speed)
        sleep(3)

if __name__ == "__main__":
    main()