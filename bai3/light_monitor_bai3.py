
import asyncio
import json
from datetime import datetime

from aiocoap import Context, Message, GET


SERVER_URI = (
    "coap://127.0.0.1:5683/iot/lab/light01/status"
)


def display_status(response, initial=False):
    data = json.loads(
        response.payload.decode("utf-8")
    )

    current_time = datetime.now().strftime("%H:%M:%S")

    if initial:
        print(f"\n[{current_time}] Initial State")
    else:
        print(f"\n[{current_time}] State Updated")

    print(f"Device: {data['device_id']}")
    print(f"Status: {data['status']}")
    print("-" * 35)


async def main():
    protocol = await Context.create_client_context()
    observation = None

    print("========== Light Monitoring Client ==========")
    print(f"Resource: {SERVER_URI}")
    print("Registering CoAP Observe...")
    print("Press Ctrl+C to stop.")

    try:
        # Dang ky Observe
        request = Message(
            code=GET,
            uri=SERVER_URI,
            observe=0
        )

        requester = protocol.request(request)

        # Nhan trang thai ban dau
        response = await asyncio.wait_for(
            requester.response,
            timeout=10
        )

        if not response.code.is_successful():
            print(f"Observe failed: {response.code}")
            return

        if response.opt.observe is None:
            print("Server does not support Observe.")
            return

        observation = requester.observation

        if observation is None:
            print("Observation is not available.")
            return

        print("Observe registration successful")
        display_status(response, initial=True)

        # Nhan thong bao tu Server khi trang thai thay doi
        # Khong gui GET dinh ky
        async for notification in observation:
            display_status(notification)

    except asyncio.TimeoutError:
        print("LOI: Server khong phan hoi.")

    except Exception as error:
        print(f"LOI: {error}")

    finally:
        if observation is not None:
            observation.cancel()

        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitoring Client stopped.")
