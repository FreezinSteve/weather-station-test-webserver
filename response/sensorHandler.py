import datetime

from response.requestHandler import RequestHandler
from io import StringIO
import random
from datetime import datetime
from datetime import timedelta

class SensorHandler(RequestHandler):
    temperature = random.randint(0, 300) / 10

    def __init__(self):
        super().__init__()
        self.contentType = "text/plain"

    def get_data(self, parameters):

        id = None
        day = None
        if "id" in parameters:
            id = parameters["id"][0]
        if "day" in parameters:
            day = parameters["day"][0]
        if id is None:
            self.setStatus(404)
            return False

        try:
            self.setStatus(200)
            if day is None:
                # sensor value only
                SensorHandler.temperature = SensorHandler.temperature + random.randint(-10, 10) / 10
                data = str(round(SensorHandler.temperature, 1))
            else:
                val = 0
                min = -10
                max = 10
                floor = 0
                ceil = 0
                if id == "te":
                    val = random.randint(-100, 200) / 10
                    min = -5
                    max = 5
                    floor = -10
                    ceil = 40
                elif id == "ws":
                    val = random.randint(0, 200) / 10
                    min = -15
                    max = 15
                    floor = 0
                    ceil = 20
                elif id == "gs":
                    val = random.randint(0, 500) / 10
                    min = -15
                    max = 15
                    floor = 0
                    ceil = 50
                elif id == "wd":
                    val = random.randint(0, 3590) / 10
                    min = -100
                    max = 100
                    floor = 0
                    ceil = 359
                elif id == "rh":
                    val = random.randint(50, 1000) / 10
                    min = -3
                    max = 3
                    floor = 0
                    ceil = 100
                elif id == "bp":
                    val = random.randint(9950, 10500) / 10
                    min = -1
                    max = 1
                    floor = 990
                    ceil = 1050
                # return a time series
                data = ""
                timestamp = datetime.now() + timedelta(days=1)
                for i in range(0, 144):
                    timestamp = timestamp + timedelta(minutes=10)
                    val = val + random.randint(min, max) / 10
                    if val < floor:
                        val = floor
                    if val > ceil:
                        val = ceil
                    #if id == "wd":
                    #    val = 350
                    data = data + timestamp.replace(microsecond=0).isoformat() + "," + str(round(val, 1)) + "\n"
            self.contents = StringIO(data)
            if SensorHandler.temperature < 0:
                SensorHandler.temperature += 10
            return True
        except:
            self.setStatus(404)
            return False
