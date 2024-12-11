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
        print(f'Starting {self.title} @ {self.starts} for {self.duration} mins')
        sleep(self.duration*60)
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
        return self

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
    
    def import_json(filename : str) -> Dict:
        # get the current week from datetime
        # look for a jsonc file with the same week name
        # read the contents, convert them into appropriate format and return schedule
        return NotImplemented
    
    def export_json(self) -> None:
        # export the schedule as json with filename as current-week_variable-name.jsonc
        return NotImplemented
    