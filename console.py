"""Console thread in charge of everything screen related"""
import time
import curses


class Console(object):

    def __init__(self, stats, args):
        self.stats = stats
        self.args = args
        self.stdscr = None
        self.current_number_of_lines = 0

    def run(self):
        curses.wrapper(self.console_main)    

    def console_main(self, stdscr):
        self.stdscr = stdscr
        while True:
            self.current_number_of_lines = 0

            args_str = "args: " + str(self.args)
            section_count_str = str(self.stats.get_section_count_tabular_string())
            overall_stats_header = "\nOverall Traffic Statistics: \n"
            verb_count_str = str(self.stats.get_http_verbs_tabular_string()) + "\n"
            status_count_str = str(self.stats.get_status_tabular_string()) + "\n"
            total_count_str = "Total Hits: " + str(self.stats.get_total_count()) + "\n"
            total_size_str = "Total Size: " + str(self.stats.get_total_size_human_readable())
            avg_hit_str = "Average Hit Size: " + str(self.stats.get_avg_hit_size()) 
            alerts_str = "\nAlerts:\n" + str(self.stats.get_alerts_string())

            self.__add_to_screen(args_str)
            self.__add_to_screen(section_count_str)
            self.__add_to_screen(overall_stats_header)
            self.__add_to_screen(verb_count_str)
            self.__add_to_screen(status_count_str)
            self.__add_to_screen(total_count_str)
            self.__add_to_screen(total_size_str)
            self.__add_to_screen(avg_hit_str)
            self.__add_to_screen(alerts_str)
            
            self.stdscr.refresh()
            time.sleep(2)

    def __add_to_screen(self, text):
        height, width = self.stdscr.getmaxyx()
        after_text_len = len(text) + self.current_number_of_lines
        if after_text_len >= height:
            self.stdscr.resize(after_text_len, width)
        self.stdscr.addstr(self.__current_number_of_lines(text), 0, text)

    def __current_number_of_lines(self, text):
        prev_number_of_lines = self.current_number_of_lines
        self.current_number_of_lines += self.__number_of_lines(text)
        return prev_number_of_lines

        
    def __number_of_lines(self, text):
        return len(text.split('\n'))