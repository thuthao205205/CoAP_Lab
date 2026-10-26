
import asyncio
from datetime import datetime

from aiocoap import resource, Message, Context
from aiocoap.numbers.codes import Code


# Tai nguyen /iot/lab/message
class MessageResource(resource.Resource):

    # Xu ly yeu cau GET
    async def render_get(self, request):
        print("\nGET request received: /iot/lab/message")

        message = "Xin chao tu CoAP Server"

        return Message(
            code=Code.CONTENT,
            payload=message.encode("utf-8")
        )

    # Xu ly yeu cau POST
    async def render_post(self, request):
        message = request.payload.decode("utf-8")
        receive_time = datetime.now().strftime("%H:%M:%S")

        print("\nPOST request received:")
        print(f"Payload: {message}")
        print(f"Time: {receive_time}")

        response = "Server da nhan thong diep"

        return Message(
            code=Code.CHANGED,
            payload=response.encode("utf-8")
        )


async def main():
    # Khoi tao cay tai nguyen
    root = resource.Site()

    # Dang ky URI /iot/lab/message
    root.add_resource(
        ["iot", "lab", "message"],
        MessageResource()
    )

    # Khoi tao CoAP Server tai cong UDP 5683
    server = await Context.create_server_context(
        root,
        bind=("127.0.0.1", 5683)
    )

    print("CoAP Server started on port 5683")
    print("Resource: coap://localhost:5683/iot/lab/message")
    print("Waiting for requests...")
    print("Press Ctrl+C to stop.")

    try:
        await asyncio.Future()
    finally:
        await server.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCoAP Server stopped.")
