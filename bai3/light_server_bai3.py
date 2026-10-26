
import asyncio
import json
from datetime import datetime

from aiocoap import Context, Message, resource
from aiocoap.numbers.codes import Code
from aiocoap.numbers.contentformat import ContentFormat


class SmartLightResource(resource.ObservableResource):

    def __init__(self):
        super().__init__()
        self.device_id = "light01"
        self.status = "OFF"

    def get_status_payload(self):
        data = {
            "device_id": self.device_id,
            "status": self.status
        }
        return json.dumps(data).encode("utf-8")

    # GET: Lay trang thai hien tai
    async def render_get(self, request):
        print("\nGET request received")

        return Message(
            code=Code.CONTENT,
            payload=self.get_status_payload(),
            content_format=ContentFormat.JSON
        )

    # PUT: Dieu khien den
    async def render_put(self, request):
        print("\nPUT request received")

        try:
            data = json.loads(request.payload.decode("utf-8"))

            device_id = data.get("device_id")
            command = data.get("command")

            print(f"Device: {device_id}")
            print(f"Command: {command}")

            if device_id != self.device_id:
                return Message(
                    code=Code.BAD_REQUEST,
                    payload=b"Invalid device_id"
                )

            if command not in ["ON", "OFF"]:
                return Message(
                    code=Code.BAD_REQUEST,
                    payload=b"Invalid command. Use ON or OFF"
                )

            old_status = self.status

            # Cap nhat trang thai
            self.status = command

            if old_status != self.status:
                print(
                    f"Light state changed: "
                    f"{old_status} -> {self.status}"
                )

                # Thong bao cho cac Observe Client
                self.updated_state()

                print(f"Notify observers: {self.status}")

            else:
                print("Light state unchanged")

            return Message(
                code=Code.CHANGED,
                payload=self.get_status_payload(),
                content_format=ContentFormat.JSON
            )

        except (json.JSONDecodeError, UnicodeDecodeError):
            return Message(
                code=Code.BAD_REQUEST,
                payload=b"Invalid JSON payload"
            )


async def main():
    root = resource.Site()

    light = SmartLightResource()

    root.add_resource(
        ["iot", "lab", "light01", "status"],
        light
    )

    server = await Context.create_server_context(
        root,
        bind=("127.0.0.1", 5683)
    )

    print("========== CoAP Smart Light Server ==========")
    print("Server started on UDP port 5683")
    print("Resource: /iot/lab/light01/status")
    print("Initial light status: OFF")
    print("Press Ctrl+C to stop.")

    try:
        await asyncio.Future()
    finally:
        await server.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSmart Light Server stopped.")
