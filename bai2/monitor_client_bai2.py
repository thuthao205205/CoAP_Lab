
import asyncio
import json
from datetime import datetime

from aiocoap import Context, Message, GET


SERVER_URI = (
    "coap://127.0.0.1:5683/iot/lab/sensor01/data"
)

TEMPERATURE_THRESHOLD = 35.0
HUMIDITY_THRESHOLD = 40.0


async def main():
    protocol = await Context.create_client_context()

    print("========== CoAP Monitoring Client ==========")
    print(f"Monitoring: {SERVER_URI}")
    print("Polling every 3 seconds...")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            try:
                request = Message(
                    code=GET,
                    uri=SERVER_URI
                )

                response = await asyncio.wait_for(
                    protocol.request(request).response,
                    timeout=5
                )

                if not response.code.is_successful():
                    print(f"\nServer error: {response.code}")

                else:
                    sensor_data = json.loads(
                        response.payload.decode("utf-8")
                    )

                    device_id = sensor_data["device_id"]
                    temperature = sensor_data["temperature"]
                    humidity = sensor_data["humidity"]

                    current_time = datetime.now().strftime(
                        "%H:%M:%S"
                    )

                    print(
                        f"\n[{current_time}] Received sensor data"
                    )
                    print(f"Device: {device_id}")
                    print(f"Temperature: {temperature} C")
                    print(f"Humidity: {humidity} %")

                    has_alert = False

                    if temperature > TEMPERATURE_THRESHOLD:
                        print("CANH BAO: Nhiet do cao")
                        has_alert = True

                    if humidity < HUMIDITY_THRESHOLD:
                        print("CANH BAO: Do am thap")
                        has_alert = True

                    if not has_alert:
                        print("Trang thai: Binh thuong")

                    print("-" * 35)

            except asyncio.TimeoutError:
                print(
                    "\nLOI: Server khong phan hoi "
                    "trong thoi gian cho."
                )

            except (json.JSONDecodeError, KeyError, TypeError) as error:
                print(f"\nLOI: Du lieu JSON khong hop le: {error}")

            except Exception as error:
                print(f"\nLOI: Khong the lay du lieu: {error}")

            await asyncio.sleep(3)

    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitoring Client stopped.")
