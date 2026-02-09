from picrawler import Picrawler
from time import sleep

crawler = Picrawler()

def main():

    speed = 80

    while True:
       
        crawler.do_action('forward',5,speed)
        sleep(0.05)
        
        crawler.do_action('turn left',2,speed)
        crawler.do_action('turn left',2,speed)
        sleep(0.05)
        crawler.do_action('forward',5,speed)
        sleep(0.05)
        
        crawler.do_action('turn left',2,speed)
        crawler.do_action('turn left',2,speed)
        sleep(0.05)
        crawler.do_action('forward',5,speed)
        sleep(0.05)
        
        crawler.do_action('turn left',2,speed)
        crawler.do_action('turn left',2,speed)
        sleep(0.05)
        crawler.do_action('forward',5,speed)
        sleep(0.05)
        
        crawler.do_action('turn left',2,speed)
        crawler.do_action('turn left',2,speed)
        
        crawler.do_step('stand',speed)
        sleep(1)

if __name__ == "__main__":
    main()