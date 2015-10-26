from tkinter import *
from math import sqrt
import tkinter.ttk as ttk
import os
import threading
import time

class PrimeFinder():
    'PrimeFinder is the object that will search for primes, and set the appropriate label'
    'to the most recent prime found. In the future, PrimeFinder will be able to return'
    'a set of all values so that they can be plotted on a graph displayed by the GUI'
    
    def __init__(self, l_display_prime, l_av_time, l_primes_found):
        self.l_display_prime = l_display_prime
        self.l_av_time = l_av_time
        self.l_primes_found = l_primes_found
        self.prime_list = [2]
        self.running = False
        self.av_time_start = 0
        self.av_time_stop = 0
        self.primes_found = 1
        self.old_primes_found = 1
        
    def start(self):
        self.running = True
        time.sleep(0.5)
        run_thread = threading.Thread(target=self.run)
        run_thread.setDaemon(True)
        self.av_time_start = time.clock()
        run_thread.start()
        
    def stop(self):
        self.running = False
    
    def update_av_time(self):
        self.av_time_stop = time.clock()
        if(self.primes_found == self.old_primes_found):
            self.l_av_time['text'] = '{0:.5f}'.format(
                self.av_time_stop-self.av_time_start)
            return
        self.l_av_time['text'] = '{0:.5f}'.format(
            (self.av_time_stop - self.av_time_start)/
            (self.primes_found - self.old_primes_found))
        self.old_primes_found = self.primes_found
        self.av_time_start = time.clock()

    def run(self):
        poss_prime = 1
        while(self.running):
            poss_prime += 2
            poss_prime_sqrt = int(sqrt(poss_prime))
            for i in self.prime_list:
                if(i > poss_prime_sqrt):
                    self.prime_list.append(int(poss_prime))
                    self.primes_found += 1
                    break
                if(poss_prime % i == 0):
                    break
            self.l_display_prime['text'] = str(self.prime_list[-1])
            self.l_primes_found['text'] = str(self.primes_found)
            if(self.primes_found % 1000 == 0):
                time.sleep(0.01)
                self.update_av_time()

root = Tk()

screen_width = 320
screen_height = 240
x_win_coord = 200
y_win_coord = 200

root.geometry('{}x{}+{}+{}'.format(screen_width, screen_height, x_win_coord, y_win_coord))
root.title('Prime Display')

def make_num_display_frame(use_frame):
    use_frame.grid(column=0, row=0, sticky='nsew')
    
    l_curr_prime = Label(use_frame, text='1')
    l_av_time = Label(use_frame, text='0.0')
    l_num_primes = Label(use_frame, text='1')
    
    ll_curr_prime = Label(use_frame, text='Current Prime:')
    ll_av_time = Label(use_frame, text='Average time: ')
    ll_num_primes = Label(use_frame, text='Primes found: ')
    
    pf = PrimeFinder(l_curr_prime, l_av_time, l_num_primes)
    
    b_start = Button(use_frame, text='Start finding primes!',
        command=lambda: pf.start())
    b_stop = Button(use_frame, text='Stop finding primes!',
        command=lambda: pf.stop())
    
    ll_curr_prime.grid(column=0, row=0, sticky='new')
    ll_av_time.grid(column=0, row=1, sticky='new')
    ll_num_primes.grid(column=0, row=2, sticky='new')
    
    l_curr_prime.grid(column=1, row=0, sticky='e')
    l_av_time.grid(column=1, row=1, sticky='e')
    l_num_primes.grid(column=1, row=2, sticky='e')
    
    b_start.grid(column=0, row=3, sticky='sw')
    b_stop.grid(column=1, row=3, sticky='se')
    

num_display_frame = Frame(root)
make_num_display_frame(num_display_frame)
num_display_frame.tkraise()

# use only on mac, otherwise use lift on window.
os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost ''' +
            '''of process "Python" to true' ''')

root.mainloop()

