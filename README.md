# One-Button YouTube for LG WebOS TV

A Python-based system that lets an elderly or non-technical user launch a new YouTube video with a single button press.

This project uses a Raspberry Pi, an RF button, and the LG WebOS API to:
- Power on the TV (if it’s off)
- Launch YouTube in guest mode
- Play a random, full-length unwatched video from a preferred channel

---

## 🛠 Features

- Wake-on-LAN support to power on the TV
- Connects via WebOS API using Python
- Launches YouTube and automatically selects guest mode
- Plays a full-length unwatched video from a YouTube channel
- Persistent storage of watched/unwatched videos
- RF button triggers the whole process

---

## 📦 Requirements

- Raspberry Pi (any model with GPIO support)
- 433 MHz RF receiver + button
- LG TV with WebOS and Wake-on-LAN enabled
- Python 3.x
- YouTube channel of your choice (default: [48 Hours](https://www.youtube.com/@48hours))

---
