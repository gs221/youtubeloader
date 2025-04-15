import os
import time
import pickle

from yoututbe_channel import YoutubeChannel48Hours
from pywebostv.connection import WebOSClient
from pywebostv.controls import ApplicationControl, InputControl, SystemControl, MediaControl
from wakeonlan import send_magic_packet
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def configure_tv_play_video(): 
    if not tv_online():
        turn_on_tv()

        # Wait for the TV to appear on the network, try up to 10 times. 
        for _ in range(10):
            if tv_online():
                break
            else:
                time.sleep(3)

    # Establish Connection With LG WebOS TV
    client =connect_to_tv()

    # Set volume to something low 
    media = MediaControl(client)
    media.set_volume(8)

    # System control allows notifications to be sent to TV
    system = SystemControl(client)
    system.notify("Connected to the TV. Youtube will launch shortly.")  

    # Get a youtube video to watch 
    video = get_youtube_video()

    # Launch YouTube on the TV with the selected video. 
    app = ApplicationControl(client)
    apps = app.list_apps()
    yt = [x for x in apps if "youtube" in x["title"].lower()][0]
    app.launch(yt, content_id=video)

    # Wait for the app to launch
    system.notify("Waiting 15 seconds for Youtube to launch...")  
    time.sleep(15)

    # Select YouTube guest mode 
    inp = InputControl(client)
    inp.connect_input()
    inp.down()
    time.sleep(1)
    inp.ok()
    inp.disconnect_input()

    system.notify("Video should now be playing. Enjoy!")  


def turn_on_tv():
    tv_mac = os.getenv('TV_MAC')

    # Turn on the TV through wake on LAN
    send_magic_packet(tv_mac)
    send_magic_packet(tv_mac)

def tv_online():
    tv_addr = os.getenv('TV_ADDR')

    # Check if the TV is online by pinging it 
    response = os.system(f"ping -c 1 -t 1 {tv_addr}")
    if response == 0:
        print(f"{tv_addr} is online")
        return True
    else:
        print(f"{tv_addr} is offline")
        return False

def connect_to_tv(max_tries=10):
    # tv_key = {}
    tv_key = {'client_key': os.getenv('WEBOS_KEY')}
    tv_addr = os.getenv('TV_ADDR')

    for i in range(max_tries):
        try:
            # Establish Connection With LG WebOS TV
            client = WebOSClient(tv_addr)
            client.connect()
            for status in client.register(tv_key, timeout=10):
                if status == WebOSClient.PROMPTED:
                    print("Please accept the connect on the TV!")
                elif status == WebOSClient.REGISTERED:
                    print("Registration successful!")
                    print(f"Store this as the environment variable WEBOS_KEY: {tv_key}")
                    return client
        except Exception as e:
            print(f"Connection attempt {i+1} failed: {e}")
            time.sleep(5)

def get_youtube_video():
    # Get a youtube video to watch 
    if os.path.exists('ytc_48_hours.pickle'):
        with open('ytc_48_hours.pickle', 'rb') as f:
            ytc_48_hours = pickle.load(f)
    else:
        ytc_48_hours = YoutubeChannel48Hours()
        ytc_48_hours.scrape_video_urls()

    video = ytc_48_hours.get_unwatched_video_url()

    # Pickle youtube channel object(s) to file
    with open('ytc_48_hours.pickle', 'wb') as f:
        pickle.dump(ytc_48_hours, f)

    return video


if __name__ == "__main__":
    configure_tv_play_video()
