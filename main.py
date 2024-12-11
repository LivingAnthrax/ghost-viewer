from time import sleep
from pprint import pprint
import datetime as dt
# from datetime import datetime as dt, timedelta as delta

from scheduler import Stream, Schedule
import browser
import json
#from browser import init_browser, app, profile_path, profile_name

def first_run() -> bool:
    # Run this function to check if the first run has been done on the current system or not
    # (create a user_preference file for the same)
    # If yes, then continue to regular runs
    # If no, then implement the following steps
    # 1. Check the browsers which are available on the system
    # 2. Ask the user to select the browsers they want to use and the default one as well
    # 3. Duplicate the profile for the selected browser
    # 4. Open each browser, ask the user to login to twitch and install & setup relevant plug-ins as well
    return NotImplemented

def sanity_check() -> None:
    '''
    All sanity checks to be done before proceeding with the main loop will be done here
    '''
    # #### Browser checks
    # 1. Streaming sites are currently logged in
    # 2. Site is connecting + network connectivity
    # 3. Plugins are installed, enabled and updated 
    # 4. Check for open browser windows
    # #### Schedule checks
    # 1. Check if there are any schedule overlaps and handle them
    # #
    return NotImplemented

def main() -> None:
    '''
    Steps in the main funtion run
    1. Get current date and time and extract week from it
    2. Check the json folder if a schedule json exists for current week or not
    3. If yes, then create schedule object and import the file
    4. If not then call schedule.update to fetch a new schedule from the web. Export schedule to json
    5. Schedule is read but streams are just dictionaries.
    6. for each item/stream in schedule,
        convert the dictionary to stream object inside schedule
        if timenow > stream.ends, remove the stream from schedule
        remove
    7. inside while loop
        1. get current datetime.
        2. for each stream in schedule
            if stream.starts > time now > stream.ends
                set current stream = schedule.stream
                stream.play
            
    '''


    # starts = dt.datetime.now()
    # duration = 5
    # ends = dt.datetime.now() + dt.timedelta(minutes=duration)
    
    #starts = dt.datetime.strftime('2024-11-22 04:30 IST')
    # TODO: Currently can't compare naive dt (dt.now) with aware dt (the one below)
    # starts = dt.datetime.strptime('2024-11-21 00:10 +0530', '%Y-%m-%d %H:%M %z')
    # starts = dt.datetime.now()
    starts = dt.datetime.strptime('2024-12-06 04:30', '%Y-%m-%d %H:%M')
    duration = 180
    ends = starts + dt.timedelta(minutes=duration)
    # try:
    #     chrome = browser.init_browser(browser= browser.app, path= browser.profile_path, profile= browser.profile_name)
    # except Exception as e:
    #     print(e)
    # chrome = init_browser(browser= app, path= profile_path, profile= profile_name)
    current = Stream(starts= starts,
                     ends= ends,
                     duration= duration,
                     url='https://twitch.tv/gaz_ttv',
                     title='Prime Time #417',
                     drops= 'Tennobaum Gift',
                     browser= 'chrome')
    pprint(current)
    # current.play_stream()

    # print(f'Time now : {dt.datetime.now()}')
    # print(f'Stream starts : {current.starts}')
    # print(f'{dt.datetime.now() > current.starts}')
    this_week = Schedule().add_stream(current)
    
    # with open('json/this_week.json', 'w', encoding='utf-8') as file_handle:
    #     json.dump(this_week, file_handle, indent= 4)

    while True:
        now = dt.datetime.now()
        if now >= current.starts:
            current.play_stream()
            break
        else:
            print(f"{now} : Stream hasn't started yet. {(current.starts - now).seconds//60} min(s) left.")
            sleep(300)
            continue

if __name__ == '__main__':
    main()