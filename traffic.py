# -*- coding: utf-8 -*-

"""
Module to display your AG DSN traffic

Show how much of your AG DSN traffic you used today in your
statusbar

Configuration parameters:
    - cache_timeout : refresh intervall in seconds
    - traffic_url : where to get the traffic data (expects json)

@author Matthes Lipke matthes.lipke@gmail.com
@license BSD
"""

import time
import requests

class Py3status:
    # available configuration parameters
    cache_timeout = 120
    traffic_url = "https://atlantis.wh2.tu-dresden.de/traffic/getMyTraffic.php"

    def __init__(self):
        pass

    def kill(self, i3s_output_list, i3s_config):
        pass

    def on_click(self, i3s_output_list, i3s_config, event):
        return self.traffic(i3s_output_list, i3s_config)

    def traffic(self, i3s_output_list, i3s_config):
        t = Traffic(self.traffic_url)

        try:
            t.get()
        except Exception as e:
            t = "0.000 MiB"

        output = {
                "cached_until": time.time() + self.cache_timeout,
                "full_text": str(t)
                }
        return output

class Traffic:
    def __init__(self, url):
        self.TRAFFIC_URL = url
    
    def get(self):
        response = requests.get(self.TRAFFIC_URL).json()

        if response.get("version") == 2:
            upload = response.get("traffic").get("out")
            download = response.get("traffic").get("in")
            
            self.traffic = upload + download
        elif response.get("version") == 0:
            raise ResponseError("Not connected to an AG DSN network")
        else:
            raise ResponseError("Check your internet connection")

    def __str__(self):
        num, dec = str(self.traffic).split(".")
        return num + "." + dec[0:3] + " MiB"

class ResponseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

if __name__ == "__main__":
    status = Py3status()

    config = {
        "color_bad": "#FF0000",
        "color_degraded": "#FFFF00",
        "color_good": "#00FF00"
    }

    while True:
        print(status.traffic([], config))
        time.sleep(1)
