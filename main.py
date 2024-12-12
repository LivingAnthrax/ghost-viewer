from time import sleep
from pprint import pprint
from os import scandir
import datetime as dt
# from datetime import datetime as dt, timedelta as delta

from scheduler import Stream, Schedule
# import browser
# import json
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
    # 2. Clean the schedule and remove old streams#
    return NotImplemented

def main() -> None:
    '''
    Steps in the main funtion run
    1. Get current date and time and extract week from it - DONE
    2. Check the json folder if a schedule json exists for current week or not
    3. If yes, then create schedule object and import the file - DONE
    4. If not then call schedule.update to fetch a new schedule from the web. Export schedule to json - NOT IMPLEMENTED
    5. Schedule is read but streams are just dictionaries. - DEPRECATED: import_json() now returns correct dict with Stream
    6. for each item/stream in schedule,
        convert the dictionary to stream object inside schedule - DEPRECATED: import_json() now returns correct dict with Stream
        if timenow > stream.ends, remove the stream from schedule
        remove - TODO : Currently skips the Stream in while loop instead of removing. Move to sanity_checks()
    7. for each stream in schedule - DONE
        inside while loop
            get current datetime.
            if time.now > stream.ends
                break
            elif stream.starts > time now > stream.ends
                set current stream = schedule.stream
                stream.play
                break
            else
                print Stream hasn't started yet. Next stream in x mins
                sleep for 5 mins
                continue
    '''
    
    # ### Archaic code - Clean this later
    # # starts = dt.datetime.now()
    # # duration = 5
    # # ends = dt.datetime.now() + dt.timedelta(minutes=duration)
    
    # #starts = dt.datetime.strftime('2024-11-22 04:30 IST')
    # # TODO: Currently can't compare naive dt (dt.now) with aware dt (the one below)
    # # starts = dt.datetime.strptime('2024-11-21 00:10 +0530', '%Y-%m-%d %H:%M %z')
    # # starts = dt.datetime.now()
    # starts = dt.datetime.strptime('2024-12-06 04:30', '%Y-%m-%d %H:%M')
    # duration = 180
    # ends = starts + dt.timedelta(minutes=duration)
    # # try:
    # #     chrome = browser.init_browser(browser= browser.app, path= browser.profile_path, profile= browser.profile_name)
    # # except Exception as e:
    # #     print(e)
    # # chrome = init_browser(browser= app, path= profile_path, profile= profile_name)
    # current = Stream(starts= starts,
    #                  ends= ends,
    #                  duration= duration,
    #                  url='https://twitch.tv/gaz_ttv',
    #                  title='Prime Time #417',
    #                  drops= 'Tennobaum Gift',
    #                  browser= 'chrome')
    # pprint(current)
    # # current.play_stream()

    # # print(f'Time now : {dt.datetime.now()}')
    # # print(f'Stream starts : {current.starts}')
    # # print(f'{dt.datetime.now() > current.starts}')
    # this_week = Schedule().add_stream(current)

    # while True:
    #     now = dt.datetime.now()
    #     if now >= current.starts:
    #         current.play_stream()
    #         break
    #     else:
    #         print(f"{now} : Stream hasn't started yet. {(current.starts - now).seconds//60} min(s) left.")
    #         sleep(300)
    #         continue
    # ### Archaic code ends here
    # Get current week number and set it as an empty schdule variable
    now = dt.datetime.now()
    weekNow = Schedule()
    
    # Get json files in the respective directory
    jsonPath = './json/'
    jsonFiles = [file.name for file in scandir(jsonPath)]

    if weekNow.name + '.json' in jsonFiles:
        print(f'json found for {weekNow.name}')
        # print(weekNow.name)
        weekNow = weekNow.import_json(jsonPath)
    else:
        pprint('json NOT found for weekNow')
        # weekNow.update()
        # weekNow = weekNow.import_json(weekNow.name)
    
    # pprint(weekNow)

    for index, stream in weekNow.items():
        # print(f'i in for loop : {i}')'
        print(f"{now.strftime('%Y-%m-%d %H:%M :: ')}Upcoming stream - {stream.title} @ {stream.starts.strftime('%Y-%m-%d %H:%M')} drops {stream.drops}")
        while True:
            now = dt.datetime.now()
            if now >= stream.ends:
                print(f"{now.strftime('%Y-%m-%d %H:%M :: ')}{stream.title} is over @ {stream.ends.strftime('%Y-%m-%d %H:%M')}")
                break
            elif stream.starts > now >stream.ends:
                print(f"{now.strftime('%Y-%m-%d %H:%M :: ')}Starting {stream.title} and waiting till {stream.ends.strftime('%Y-%m-%d %H:%M')}")
                stream.play_stream()
                print(f"{now.strftime('%Y-%m-%d %H:%M :: ')}{stream.title} has ended")
                break
            else:
                print(f"{now.strftime('%Y-%m-%d %H:%M :: ')}{stream.title} is yet to start. {(stream.starts - now).seconds//60} min(s) left")
                sleep(300)
                continue
        print(f'All caught up! No more streams this week..')
    print('End of main')

if __name__ == '__main__':
    main()