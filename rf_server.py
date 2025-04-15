from rpi_rf import RFDevice
from webos import configure_tv_play_video
import time


# Your GPIO pin for receiver
RX_PIN = 27  
rfdevice = RFDevice(RX_PIN)
rfdevice.enable_rx()
timestamp = None

print("Listening for RF signals...")

try:
    while True:
        if rfdevice.rx_code_timestamp != timestamp:
            timestamp = rfdevice.rx_code_timestamp
            received_code = rfdevice.rx_code
            print(f"Received code: {received_code}")

            # Replace with your actual code value
            if received_code == 13739617:  
                try:
                    configure_tv_play_video()
                except Exception as e:
                    print(f"Couldn't configure tv and play video: {e}")

        time.sleep(0.01)

except KeyboardInterrupt:
    rfdevice.cleanup()
