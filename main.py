# by krutmaster
import os
import datetime
import configparser
from youtube_dl import YoutubeDL
from youtube_dl.utils import DateRange


def createConfig():
    """Create config file for save program settings"""
    config = configparser.ConfigParser()
    config.add_section('Settings')
    config.set('Settings', 'date_last', str(datetime.datetime.now().date()).replace('-', ''))
    config.add_section('List channels')
    channels = {}
    config.set('List channels', 'names', str(channels))

    with open('config.ini', 'w') as config_file:
        config.write(config_file)


def date_range():
    """Interval date for downloading"""
    global config

    start_date = config.get('Settings', 'date_last')
    end_date = datetime.datetime.now().date()
    days = (end_date - datetime.date(int(start_date[:4]), int(start_date[4:6]), int(start_date[6:]))).days + 1
    return start_date, str(end_date).replace('-', ''), days


def str_in_dict():
    """Turn string type from config in dictionary type"""
    global config

    return eval(config.get('List channels', 'names'))


def add_channel(link, name):
    """Add channel in list for downloading"""
    global config, channels

    channels[name] = link
    config.set('List channels', 'names', str(channels))

    with open('config.ini', 'w') as config_file:
        config.write(config_file)

    print(f'Channel with name {name} was added successfully')


def del_channel(name):
    """Delete channel from list for downloading"""
    global config, channels

    channels.pop(name)
    config.set('List channels', 'names', str(channels))

    with open('config.ini', 'w') as config_file:
        config.write(config_file)

    print(f'Channels with name {name} was deleted successfully')


def list_channels():
    """Print list channel for downloading"""
    global config, channels

    print('List channels:')

    for i, channel in enumerate(channels):
        print(f'{i + 1}. {channel} : {channels[channel]}')

    print('The end')


def download(channel):
    """Download video"""
    start_date, end_date, days = date_range()
    path = os.getcwd() + '\Download'

    ydl_opts = {
        'daterange': DateRange(start=start_date, end=end_date),  # rewrite
        'download_archive': 'archive.txt',
        'ignoreerrors': True,
        'playlistend': days * 5,
        'outtmpl': path + '\%(title)s.%(ext)s',
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([channel])


if __name__ == '__main__':
    if not os.path.exists('config.ini'):
        createConfig()

    config = configparser.ConfigParser()
    config.read('config.ini')
    channels = str_in_dict()
    ans = ' '

    while ans[0] != 'exit':
        ans = input().split()
        if ans[0] == 'add':
            name, link = ans[1], ans[2]
            add_channel(link, name)
        elif ans[0] == 'del':
            name = ans[1]
            del_channel(name)
        elif ans[0] == 'list':
            if len(channels) == 0:
                print('Error - your list channels is empty. Add channel for downloading')
            else:
                list_channels()
        elif ans[0] == 'download':
            if len(channels) == 0:
                print('Error - your list channels is empty. Add channel for downloading')
            else:
                for name in channels:
                    link = channels[name]
                    download(link)

                print('Download successfully')
                config.set('Settings', 'date_last', str(datetime.datetime.now().date()).replace('-', ''))

                with open('config.ini', 'w') as config_file:
                    config.write(config_file)
        else:
            if ans[0] != 'exit':
                print('Incorrect command, try again')
