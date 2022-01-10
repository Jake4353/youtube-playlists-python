#DOES NOT DOWNLOAD ANYTHING YET STILL WORK IN PROGRESS

import os
#os.system('pip install inquirer')
#os.system('pip install clipboard')
#os.system('pip install colorama')
#os.system('pip install youtube-search-python')
#os.system('pip install pytube')
import shutil
import inquirer
import clipboard
from colorama import Fore, Style
from youtubesearchpython import *
from pick import *
import urllib.request
import json
import urllib
from pytube import Playlist
playlist_url = ''

#test URLS

#playlist_url = 'https://www.youtube.com/playlist?list=PLoWcMTAJfJaqqLqUGE3wkOzVuXs4Fpmib'
#playlist_url= 'https://www.youtube.com/'

#todo
'''
FIX SEARCH SELECTION ON URL_INPUT()
almost done - TRY TO ADD WINDOWS SUPPORT IN THE FUTURE
CLEAN CODE - VERY EARLY VERSION (0.1)
MAKE STORAGE PROTECTION TO PREVENT VERY LARGE PLAYLISTS FROM TAKING UP TONS OF STORAGE
FILE FORMAT SELECTION (for music playlists)

------------------
WORKING ON FINAL APP WITH ALL OTHER MEDIA FEATURES
'''

#Info
'''
For managed downloading of youtube playlists within a terminal with a search function built in and 
with good error management built in
using the pytube package for downloading videos and receiving data about them
and using youtube-search-python for the search function that is built into the URL input function.
'''


#CLASS FOR MAIN APP
class playlist():

    #FOR PRINTING TO CENTER OF SCREEN
    def print_centre(c):
        print(c.center(shutil.get_terminal_size().columns))


    def url_input():
        os.system('clear')
        global playlist_url
        input_selections = []

        #CHECKING IF URL IS VALID
        if playlist_url.startswith('https://www.youtube.com/playlist?') == True or playlist_url.startswith('https://youtube.com/playlist?') == True:
            print(f'Current URL Status: {Fore.GREEN}VALID{Fore.RESET}')
            try:  input_selections.remove('Fix URL')
            except: pass
            try: input_selections.remove('Add URL')
            except: pass
            input_selections.append('Change URL')
        elif playlist_url == '':
            print(f'Current URL Status: {Fore.RED}NO URL{Fore.RESET}')
            try: input_selections.remove('Change URL')
            except: pass
            try: input_selections.remove('Fix URL')
            except: pass
            input_selections.append('Add URL')
        else:
            print(f'URL Status: {Fore.YELLOW}INVALID{Fore.RESET}')
            try: input_selections.remove('Change URL')
            except: pass
            try: input_selections.remove('Add URL')
            except: pass
            input_selections.append('Fix URL')
        input_selections.append("Back")
        #DEFINING URL INPUT METHODS
        url_input_method = [
        inquirer.List('method-input',
            message='What would you like to input your URL with',
            choices=[input_selections[0], input_selections[1]])
        ]

        #ASKING QUESTION IN TERMINAL AND RUNNING COMMANDS FOR SPECIFIC OUTPUTS
        url_input_output = inquirer.prompt(url_input_method)
        print(url_input_output['method-input'])
        if url_input_output['method-input'] == 'Back': playlist.main_screen()
        elif url_input_output['method-input'] == input_selections[0]:
            if playlist_url.startswith('https://www.youtube.com/playlist?') == True or playlist_url.startswith('https://youtube.com/playlist?') == True:
                print(f'{Fore.GREEN}Clipboard Data: \n"{clipboard.paste()}"{Fore.RESET}')
            elif playlist_url.startswith('https://') == True:
                print(f'{Fore.RED}Clipboard Data: \n"{clipboard.paste()}"{Fore.RESET}')
            else:
                print(f'{Fore.YELLOW}Clipboard Data: \n"{clipboard.paste()}"{Fore.RESET}')

            if playlist_url.startswith('https://www.youtube.com/playlist?') == True or playlist_url.startswith('https://youtube.com/playlist?') == True:
                selection_colour = Fore.GREEN
            else:
                selection_colour = Fore.RED
            url_input_method1 = [
                inquirer.List('input1',
                              message='Select Method of inputting a URL or Search Key',
                              choices=['Type Search Key', 'Use Search Key On Clipboard', f'{selection_colour}Use URL On Clipboard{Fore.RESET}'])
            ]
            url_input_output1 = inquirer.prompt(url_input_method1)
            if url_input_output1['input1'] == 'Type Search Key':
                video_search_key_input = input(f'{Fore.BLUE}What Would You Like To Search? {Fore.MAGENTA}')
                print(f'{Fore.RESET}')
                playlist_search_out = PlaylistsSearch(video_search_key_input, region='US', limit=5)
                i=0
                len_result = len(playlist_search_out.result()['result'])
                playlist_search_urls = []
                playlist_search_names=[]
                print(f'{Fore.GREEN}Loading {len_result} playlists.{Fore.RESET}')
                for i in range(len_result):
                    playlist_search_urls.append(playlist_search_out.result()['result'][i]['link'])
                    i += 1
                for i in range(len(playlist_search_urls)):
                    yt = Playlist(playlist_search_urls[int(i)])
                    playlist_search_names.append(yt.title)
                    i+=1
                playlist_search_inquire = [
                inquirer.List('list search',
                              message='Please Select A Playlist Result',
                              choices=playlist_search_names)
                ]
                playlist_search_output = inquirer.prompt(playlist_search_inquire)
                try:
                    if playlist_search_output['list search'] == playlist_search_names[0]:
                        print(playlist_search_names[0])
                        print(playlist_search_urls[0])
                        playlist_url = playlist_search_urls[0]
                    elif playlist_search_output['list search'] == playlist_search_names[1]:
                        print(playlist_search_names[1])
                        print(playlist_search_urls[1])
                        playlist_url = playlist_search_urls[1]
                    elif playlist_search_output['list search'] == playlist_search_names[2]:
                        print(playlist_search_names[2])
                        print(playlist_search_urls[2])
                        playlist_url = playlist_search_urls[2]
                    elif playlist_search_output['list search'] == playlist_search_names[3]:
                        print(playlist_search_names[3])
                        print(playlist_search_urls[3])
                        playlist_url = playlist_search_urls[3]
                    elif playlist_search_output['list search'] == playlist_search_names[4]:
                        print(playlist_search_names[4])
                        print(playlist_search_urls[4])
                        playlist_url = playlist_search_urls[4]
                except: print(f'{Fore.RED}Error Within PLAYLIST SELECTION\nPossibly with integers and the playlist search len result.{Fore.RESET}')
                playlist.url_input()

            elif url_input_output1['input1'] == 'Use Search Key On Clipboard':
                input(f'{Fore.GREEN}Press Enter If you would like to Search with this: "{clipboard.paste()}" ')
                print(f'Searching with "{clipboard.paste()}"!')
                print(f'{Fore.RESET}')
                playlist_search_out = PlaylistsSearch(clipboard.paste(), region='US', limit=5)
                i=0
                len_result = len(playlist_search_out.result()['result'])
                playlist_search_urls = []
                playlist_search_names=[]
                print(f'{Fore.GREEN}Loading {len_result} playlists.{Fore.RESET}')
                for i in range(len_result):
                    playlist_search_urls.append(playlist_search_out.result()['result'][i]['link'])
                    i += 1
                for i in range(len(playlist_search_urls)):
                    yt = Playlist(playlist_search_urls[int(i)])
                    playlist_search_names.append(yt.title)
                    i+=1
                playlist_search_inquire = [
                inquirer.List('list search',
                              message='Please Select A Playlist Result',
                              choices=playlist_search_names)
                ]
                playlist_search_output = inquirer.prompt(playlist_search_inquire)

                '''
                
                NEED TO FIX
                
                '''

                try:
                    if playlist_search_output['list search'] == playlist_search_names[0]:
                        print(playlist_search_names[0])
                        print(playlist_search_urls[0])
                        playlist_url = playlist_search_urls[0]
                    elif playlist_search_output['list search'] == playlist_search_names[1]:
                        print(playlist_search_names[1])
                        print(playlist_search_urls[1])
                        playlist_url = playlist_search_urls[1]
                    elif playlist_search_output['list search'] == playlist_search_names[2]:
                        print(playlist_search_names[2])
                        print(playlist_search_urls[2])
                        playlist_url = playlist_search_urls[2]
                    elif playlist_search_output['list search'] == playlist_search_names[3]:
                        print(playlist_search_names[3])
                        print(playlist_search_urls[3])
                        playlist_url = playlist_search_urls[3]
                    elif playlist_search_output['list search'] == playlist_search_names[4]:
                        print(playlist_search_names[4])
                        print(playlist_search_urls[4])
                        playlist_url = playlist_search_urls[4]
                except: print(f'{Fore.RED}Error Within PLAYLIST SELECTION\nPossibly with integers and the playlist search len result. THIS IS SOMETHING THAT WILL BE FIXED SOON{Fore.RESET}')
                playlist.url_input()


            elif url_input_output1['input1'] == f'{selection_colour}Use URL On Clipboard{Fore.RESET}':
                if playlist_url.startswith('https://www.youtube.com/playlist?') == True or playlist_url.startswith('https://youtube.com/playlist?') == True:
                    url_link_from_clipboard = Playlist(clipboard.paste())
                    url_sring_from_clipboard = clipboard.paste()
                else:
                    while True:
                        print("URL isn't valid")
                        if input('Press Enter When ready with URL, Type "E" To Exit') == 'E': exit()
                        else:
                            break
                    url_link_from_clipboard = Playlist(clipboard.paste())
                    url_sring_from_clipboard = clipboard.paste()
                print(f'NAME: {url_link_from_clipboard.title}')
                print(f'URL: {url_sring_from_clipboard}')
                playlist_url = url_sring_from_clipboard

            playlist.main_screen()



    def download_playlist():
        os.system('clear')

        #CHECKING IF URL IS CORRECT AGAIN
        if playlist_url.startswith('https://www.youtube.com/playlist?') == True or playlist_url.startswith('https://youtube.com/playlist?') == True or playlist_url.startswith('www.youtube.com/playlist?') == True or playlist_url.startswith(('youtube.com/playlist?')) == True:
            #CHECKING TO SEE IF USER WOULD LIKE TO CONTINUE
            input(f'{Fore.GREEN}Press enter if ready to download all, Press ctrl C to exit : {Fore.RESET}')


            print(f'Playlist DATA\nVideo Amount: {len(youtube_playlist)}\nPlaylist Owner: {youtube_playlist.owner}')
            print(f'\n\n{Fore.GREEN}Loading {len(youtube_playlist)} Videos{Fore.RESET}')

            #DEFINING LISTS AND VARIABLES FOR SELECTION
            i = 0
            noedit = [' @ Select', " @ Back"]
            canedit_names = [" @ Select", ' @ Back']
            noedit_names = ["Select", 'Back']
            index = 0
            selected_index = []

            #FAST WAY OF GETTING YOUTUBE VIDEO NAME FROM URL AND PUTTING IT IN A LIST
            for i in range(len(youtube_playlist)):
                params = {"format": "json", "url": youtube_playlist[i]}

                url = "https://www.youtube.com/oembed"

                query_string = urllib.parse.urlencode(params)

                url = url + "?" + query_string
                with urllib.request.urlopen(url) as response:
                    response_text = response.read()

                    data = json.loads(response_text.decode())

                noedit_names.append(f"{data['title']}")
                canedit_names.append(f" [ ] {data['title']}")
                noedit.append(youtube_playlist[i])


            #LIST OF ALL VIDEOS IN PLAYLIST (ASKS WHAT ONES TO REMOVE FROM DOWNLOAD)
            while True:
                option, index = pick(canedit_names,
                                     'Press Select when finished\nPress Back to cancel\nSelect songs to remove from playlist download:\n',
                                     indicator='-', default_index=index)
                if option == ' @ Select':
                    print('Exit\n')
                    print(selected_index)
                    exit()
                elif option == ' @ Back':
                    print('exiting')
                    exit()
                elif canedit_names[int(index)].startswith(' [#] ') == False:
                    canedit_names[int(index)] = f' [#] {noedit_names[int(index)]}'
                elif canedit_names[int(index)].startswith(' [#] ') == True:
                    canedit_names[int(index)] = f' [ ] {noedit_names[int(index)]}'
                selected_index.append(index)

            os.system('clear')




    def main_screen():
        os.system('clear')
        global youtube_playlist
        youtube_playlist = Playlist(playlist_url)
        #CHECKING IF URL IS CORRECT AGAIN
        if playlist_url.startswith('https://www.youtube.com/playlist?') == True or playlist_url.startswith('https://youtube.com/playlist?') == True or playlist_url.startswith('www.youtube.com/playlist?') == True or playlist_url.startswith(('youtube.com/playlist?')) == True:

            #SOME RANDOM STUFF ABOUT THE INPUTTED URL
            playlist.print_centre(c='URL:')
            playlist.print_centre(c=playlist_url)
            playlist.print_centre(c='Playlist Title:')
            playlist.print_centre(c=youtube_playlist.title)
        else: playlist.print_centre(c='No playlist inputted, cannot load DATA')

        #DEFINING WHAT ANSWERS TO GIVE ON INQUIRER QUESTIOPNS (I KNOW ITS MESSY AND IMPRACTICAL BUT IT WORKS FOR NOW)
        if playlist_url == None:
            playlist.print_centre(c=f'Playlist URL Is Not Valid, Use The URL Input Func.')
            playlist_input_selection = ['URL Input', 'Download all', 'Back']
        else:
            if playlist_url.startswith('https://www.youtube.com/playlist?')==True or playlist_url.startswith('https://youtube.com/playlist?')==True:
                playlist.print_centre(c=f'Playlist URL Is Valid')
                playlist_input_selection = ['URL Change', 'Download all', 'Back']
            else:
                playlist.print_centre(c=f'Playlist URL Is Not A Valid Youtube Url')
                playlist_input_selection = ['URL Change', 'Download all', 'Back']


        #inquirer question
        main_screen_selection = [
            inquirer.List('main menu', message='Please select an action below',
                          choices=[playlist_input_selection[0], playlist_input_selection[1], playlist_input_selection[2]])]
        main_screen_output = inquirer.prompt(main_screen_selection)

        if main_screen_output['main menu'] == 'Back':
            print(f'{Fore.GREEN}Exiting Application{Fore.RESET}')
            exit()
        elif main_screen_output['main menu'] == 'URL Change' or main_screen_output['main menu'] == 'URL Input':
            playlist.url_input()
        elif main_screen_output['main menu'] == playlist_input_selection[1]:
            playlist.download_playlist()



print('Alive!')
if __name__ == '__main__':
    playlist.main_screen()
    print('Good Bye!')
