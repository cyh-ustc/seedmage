import asyncio
import datetime
import signal
import os
import requests
import torrent
import utils

TORRENTS_DIR = 'TORRENTS'

alltasks = []


def print_wip(text):
  print(text + "...", end='', flush=True)


def print_info(text):
  print("\033[33m" + text + "\033[0m")

def print_success(text):
  print("\033[32m" + text + "\033[0m")

def print_error(text):
  print("\033[31m" + text + "\033[0m")


def handler(signum, frame):
    print("Ctrl-c was pressed. Exiting")
    for task in alltasks:
        task.cancel()
    exit(1)


signal.signal(signal.SIGINT, handler)


async def seed(torrent_file_name):
    # Torrent general information
    torrent_file = torrent.File(os.path.join(TORRENTS_DIR, torrent_file_name))
    print_info("Torrent:")
    print(torrent_file)

    # Requesting seeder information to the tracker
    seeder = torrent.Seeder(torrent_file)
    while True:
        print_wip("Requesting seeder information")
        try:
            seeder.load_peers()
            print_success("done")
            break
        except requests.exceptions.Timeout:
            print_error("timeout")

    print_info("Seeder:")
    print(seeder)

    # Calculate a few parameters
    seed_per_second = 0
    update_interval = seeder.update_interval

    # Seeding
    print_info("\nStarting seeding at %s/s" %
               utils.sizeof_fmt(seed_per_second))
    while True:
        print_wip("Waiting %d seconds" % update_interval)
        await asyncio.sleep(update_interval)
        print_success("done")

        while True:
            try:
                seeder.upload(0)
                print_success("uploaded")
                break
            except requests.exceptions.Timeout:
                print_error("timeout")


async def display_date(looptime):
    while True:
        print(str(datetime.datetime.now()), flush=True)
        await asyncio.sleep(looptime)


async def main():
    torrents_list = os.listdir(TORRENTS_DIR)

    async with asyncio.TaskGroup() as tg:
        bg_task = tg.create_task(display_date(30))
        alltasks.append(bg_task)

        for torrent_file_name in torrents_list:
            print(torrent_file_name)
            task = tg.create_task(seed(torrent_file_name))
            alltasks.append(task)

asyncio.run(main())
