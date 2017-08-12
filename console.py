"""Console thread in charge of everything screen related"""
import time
import curses



class Console(object):

    def __init__(self, stats, args):
        self.stats = stats
        self.args = args

    def run(self):
        curses.wrapper(self.console_main)    

    def console_main(self, stdscr):
        while True:
            num_of_rows = (self.stats.number_of_rows() + 1) * 2
            stdscr.addstr(0, 0, "args: " + str(self.args))
            stdscr.addstr(1, 0, str(self.stats))
            stdscr.addstr(num_of_rows + 3, 0,
                          str(self.stats.get_alerts_string()))
            stdscr.refresh()
            time.sleep(2)