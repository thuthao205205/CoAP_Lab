
import asyncio
import json
import random
from datetime import datetime

from aiocoap import resource, Message, Context
from aiocoap.numbers.codes import Code
from aiocoap.numbers.contentformat import ContentFormat


class SensorResource(resource.Resource):

    def __init__(self):
        super().__init__()

        self.device_id = "sensor01"
        self.temperature = 28.5
        self.humidity = 65.2

    # Tu dong cap nhat du lieu moi 3 giay
    async def update_sensor_data(self):
        while True:
            self.temperature = round(
                random.uniform(25.0, 40.0), 1
            )

            self.humidity = round(
                random.uniform(30.0, 80.0), 1
            )

            current_time = datetime.now().strftime("%H:%M:%S")

            print(f"\n[{current_time}] Sensor data updated")
            print(f"Device: {self.device_id}")
            print(f"Temperature: {self.temperature} C")
            print(f"Humidity: {self.humidity} %")

            await asyncio.sleep(3)

    # Xu ly GET tu Client
    async def render_get(self, request):
        sensor_data = {
            "device_id": self.device_id,
            "temperature": self.temperature,
            "humidity": self.humidity
        }

        json_data = json.dumps(sensor_data)

        current_time = datetime.now().strftime("%H:%M:%S")

        print(f"\n[{current_time}] GET request received")
        print(f"Response: {json_data}")

        return Message(
            code=Code.CONTENT,
            payload=json_data.encode("utf-8"),
            content_format=ContentFormat.JSON
        )


async def main():
    root = resource.Site()

    sensor = SensorResource()

    root.add_resource(
        ["iot", "lab", "sensor01", "data"],
        sensor
    )

    server = await Context.create_server_context(
        root,
        bind=("127.0.0.1", 5683)
    )

    print("========== Sensor CoAP Server ==========")
    print("Server started on UDP port 5683")
    print("Resource: /iot/lab/sensor01/data")
    print("Updating sensor data every 3 seconds...")
    print("Press Ctrl+C to stop.")

    update_task = asyncio.create_task(
        sensor.update_sensor_data()
    )

    try:
        await asyncio.Future()

    finally:
        update_task.cancel()

        try:
            await update_task
        except asyncio.CancelledError:
            pass

        await server.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSensor CoAP Server stopped.")
