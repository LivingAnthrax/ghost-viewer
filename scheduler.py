# Used to generate schedules based on dates published in forums and websites
from dataclasses import dataclass, field
from typing import Dict, List
from time import sleep
import datetime as dt
from pprint import pprint
import json

from browser import webdriver, init_browser, profile_path, profile_name
# from browser import *

@dataclass(order = True)
class Stream:
    '''
    Define individual stream objects
    '''
    index : str = field(init = False, repr = False)
    starts: dt.datetime = dt.datetime.now()
    ends: dt.datetime = dt.datetime.now() + dt.timedelta(minutes=2)
    duration : int = 2
    url : str = 'https://www.google.com'
    title : str = 'Default'
    drops : str = 'No drops'
    browser : webdriver = 'chrome'
    # def __init__(
    #         self,
    #         starts: dt.datetime,
    #         ends: dt.datetime,
    #         duration : int,
    #         url : str,
    #         title : str,
    #         drops : str,
    #         browser : webdriver):
    #     self.starts = starts
    #     self.ends = ends
    #     self.duration = duration
    #     self.url = url
    #     self.title = title,
    #     self.drops = drops,
    #     self.browser = browser
    
    def __post_init__(self):
        # Set the index for sorting and comparing stream objects
        self.index = self.starts.strftime('%Y-%m-%d %H:%M_') + self.title

    def play_stream(self) -> None :
        '''
        Call at relevant time to start viewing the stream. Closes the stream at specified time as well.
        '''
        # TODO : make this function asynchronous
        browser = init_browser(self.browser, profile_path, profile_name)
        browser.get(url = self.url)
        timeLeft = (self.ends - dt.datetime.now()).seconds
        print(f'Starting {self.title} @ {self.starts} for {timeLeft//60} mins')
        sleep(timeLeft)
        print(f'Closing {self.title} @ {self.ends}')
        browser.close()
    
    def to_dict(self) -> Dict:
        '''
        Converts a stream object into a dictionary to be saved as a json later.
        '''
        stream_info = dict(starts = self.starts.strftime('%Y-%m-%d %H:%M'),
                       ends = self.ends.strftime('%Y-%m-%d %H:%M'),
                       duration = self.duration,
                       url = self.url,
                       title = self.title,
                       drops = self.drops,
                       browser = self.browser
                       )
        return stream_info
    
    def from_dict(self, stream_info : dict):
        '''
        TODO : Implement default values for Stream properties
        
        Parses a json string dict into a Stream object.

        json format for proper parsing:
        
        {\n
            'starts' : 'YYYY-MM-DD HH:MM',\n
            'ends' : 'YYYY-MM-DD HH:MM',\n
            'duration' : int,\n
            'url' : str,\n
            'title' : str,\n
            'drops' : str,\n
            'browser' : str\n
        }
        '''
        self.starts = dt.datetime.strptime(stream_info['starts'],'%Y-%m-%d %H:%M')
        self.ends = dt.datetime.strptime(stream_info['ends'],'%Y-%m-%d %H:%M')
        self.duration = stream_info['duration']
        self.url = stream_info['url']
        self.title = stream_info['title']
        self.drops = stream_info['drops']
        self.browser = stream_info['browser']
        self.index = self.starts.strftime('%Y-%m-%d %H:%M_') + self.title
        return self

    def time_left(self, max_depth: int = 2) -> str:
        """
        Get time left for the stream to start.\n
        `max_depth` controls the resolution of time units to display.
        """
        diff = self.starts - dt.datetime.now()
        diff_dict = {
            'd': diff.days,
            'h': diff.seconds//3600,
            'm': (diff.seconds%3600)//60,
            's': diff.seconds%60
        }

        message = str()
        depth = 0
        for key,val in diff_dict.items():
            if val == 0 or depth >= max_depth :
                continue
            else:
                message += (f"{val.__str__()} {key} ")
                depth += 1

        return message


class Schedule(dict):
    '''
    A collection of Streams for each week stored in a dictionary format for easy recall.\n
    Key format : stream.starts_stream.title
    '''
    # How to create stream:
    # 1. If you pass the current week number, then it will check for existing schedule or generate a fresh schedule
    # 2. DONE : if you run schedule.add_stream(Stream), it should add the stream to the current schedule
    # 3. DONE : if you don't pass anything, it will create and empty dict which you can repopulate later
    # 4. if you import a schedule from a json file, it will add the streams into the current schedule object
    
    # Currently the below __init__ function is redundant. Use it for function overloading later if needed
    # def __init__(self):
    #     # try to get the week number from dt.datetime.now() and check if schedule json exists in schedule folder
    #     # or not. If yes then import it and return else
    #     # self = dict(stream_dict.starts + stream_dict.title)
    #     self = dict()
    def __init__(self):
        # for saving variable name as an attribute to stream object. Needed for json dump
        # self.name = uuid.uuid4()
        # self.name = 'week' + str(dt.datetime.today().isocalendar()[1])
        # self.name = str(dt.datetime.today().isocalendar()[0]) + '_' + str(dt.datetime.today().isocalendar()[1])
        self.name = str(dt.datetime.today().strftime('%Y')) + '_' + str(dt.datetime.today().strftime('%V'))
    
    def add_stream(self : dict, stream : Stream) -> Dict:
        '''
        Utility to manually add stream object into the schedule 
        with the key : stream.starts_stream.title
        '''
        # self[stream.starts.strftime('%Y-%m-%d %H:%M_') + stream.title] = stream
        self[stream.index] = stream
        return self
        
    def update():
        # This function will use the current week number (if nothing is passed into it, else, it will use the
        # passed argument) to scrape the info present in forums and create a weekly schdule
        # For now it will just look for a json file with the week number and import it
        return NotImplemented
    
    # def import_json(filename : str) -> Dict:
    #     # get the current week from datetime
    #     # look for a jsonc file with the same week name
    #     # read the contents, convert them into appropriate format and return schedule
    #     with open('json/'+ filename + '.json', 'r', encoding='utf-8') as file_handle:
    #         json_sched = json.load(file_handle)
    #     for key, value in json_sched.items():
    #         json_sched[key] = Stream().from_dict(value)
    #     print('JSON imported...')
    #     return json_sched

    def import_json(self, jsonPath : str) -> Dict:
        
        # get the current week from datetime
        # look for a jsonc file with the same week name
        # read the contents, convert them into appropriate format and return schedule
        with open(jsonPath + self.name + '.json', 'r', encoding='utf-8') as file_handle:
            self = json.load(file_handle)
        for key, value in self.items():
            self[key] = Stream().from_dict(value)
        print('json imported...')
        return self
    
    def export_json(self) -> None:
        # export the schedule as json with filename as current-week_variable-name.jsonc
        with open('json/' + str(self.name) + '.json', 'w', encoding='utf-8') as file_handle:
            json.dump(self, file_handle, indent= 4)
        print(f'JSON exported...{self.name}.json')
    
    # def __repr__(self) -> str :
    #     """
    #     Prints a summary of all the streams in the current week on startup
    #     """
    #     # Uses:
    #     # 1. Get the number of streams for this week
    #     # 2. Print the summary in the following format
    #     #   Total streams this week : X
    #     #   Stream 1 : 'Stream.title' @ DD MMM, YYYY for XX mins drops {Stream.drops}
    #     #   Stream 2 : 'Stream.title' @ DD MMM, YYYY for XX mins drops {Stream.drops} #
    #     return NotImplemented