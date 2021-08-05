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
                # return a time series
                data = ""
                timestamp = datetime.now() + timedelta(days=1)
                for i in range(0, 144):
                    timestamp = timestamp + timedelta(minutes=10)
                    SensorHandler.temperature = SensorHandler.temperature + random.randint(-10, 10) / 10
                    data = data + str(timestamp) + "," + str(round(SensorHandler.temperature, 1)) + "\n"
            self.contents = StringIO(data)
            if SensorHandler.temperature < 0:
                SensorHandler.temperature += 10
            return True
        except:
            self.setStatus(404)
            return False
