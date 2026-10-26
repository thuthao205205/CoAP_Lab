
import asyncio
import json

from aiocoap import Context, Message, GET, PUT
from aiocoap.numbers.contentformat import ContentFormat


SERVER_URI = (
    "coap://127.0.0.1:5683/iot/lab/light01/status"
)

DEVICE_ID = "light01"


async def send_get(protocol):
    print("\nSending GET request...")

    request = Message(
        code=GET,
        uri=SERVER_URI
    )

    response = await asyncio.wait_for(
        protocol.request(request).response,
        timeout=10
    )

    print(f"Response Code: {response.code}")
    print(f"Response: {response.payload.decode('utf-8')}")


async def send_put(protocol, command):
    print("\nSending PUT request...")

    data = {
        "device_id": DEVICE_ID,
        "command": command
    }

    request = Message(
        code=PUT,
        uri=SERVER_URI,
        payload=json.dumps(data).encode("utf-8"),
        content_format=ContentFormat.JSON
    )

    response = await asyncio.wait_for(
        protocol.request(request).response,
        timeout=10
    )

    print(f"Response Code: {response.code}")

    if response.code.is_successful():
        result = json.loads(
            response.payload.decode("utf-8")
        )

        print(f"Device: {result['device_id']}")
        print(f"Current status: {result['status']}")

        if result["status"] == "ON":
            print("Da bat den light01")
        else:
            print("Da tat den light01")

    else:
        print(
            f"Server error: "
            f"{response.payload.decode('utf-8')}"
        )


async def main():
    protocol = await Context.create_client_context()

    print("========== Light Controller Client ==========")
    print("Available commands: ON, OFF, STATUS, EXIT")

    try:
        while True:
            # Chay input trong thread rieng de khong
            # chan cac tac vu bat dong bo
            command = await asyncio.to_thread(
                input,
                "\nNhap lenh (ON/OFF/STATUS/EXIT): "
            )

            command = command.strip().upper()

            if command == "EXIT":
                print("Controller stopped.")
                break

            try:
                if command == "STATUS":
                    await send_get(protocol)

                elif command in ["ON", "OFF"]:
                    await send_put(protocol, command)

                else:
                    print(
                        "Lenh khong hop le. "
                        "Vui long nhap ON, OFF, STATUS hoac EXIT."
                    )

            except asyncio.TimeoutError:
                print("LOI: Server khong phan hoi.")

            except Exception as error:
                print(f"LOI: {error}")

    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nController stopped.")
