
import asyncio

from aiocoap import Context, Message, GET, POST


# Dia chi tai nguyen tren CoAP Server
SERVER_URI = "coap://127.0.0.1:5683/iot/lab/message"

# Thay bang thong tin cua ban
STUDENT_NAME = "Nguyen Thu Thảo"
STUDENT_ID = "B23DCCN776"


async def main():
    # Khoi tao CoAP Client
    protocol = await Context.create_client_context()

    print("========== CoAP Client ==========")

    try:
        # ===== GUI YEU CAU GET =====
        print("\nSending GET request...")
        print(f"URI: {SERVER_URI}")

        get_request = Message(
            code=GET,
            uri=SERVER_URI
        )

        get_response = await asyncio.wait_for(
            protocol.request(get_request).response,
            timeout=10
        )

        print("\nGET Response:")
        print(f"Code: {get_response.code}")
        print(
            f"Payload: {get_response.payload.decode('utf-8')}"
        )

        # ===== GUI YEU CAU POST =====
        message = (
            f"Xin chao tu CoAP Client - "
            f"{STUDENT_ID} - {STUDENT_NAME}"
        )

        print("\nSending POST request...")
        print(f"Payload: {message}")

        post_request = Message(
            code=POST,
            uri=SERVER_URI,
            payload=message.encode("utf-8")
        )

        post_response = await asyncio.wait_for(
            protocol.request(post_request).response,
            timeout=10
        )

        print("\nPOST Response:")
        print(f"Code: {post_response.code}")
        print(
            f"Payload: {post_response.payload.decode('utf-8')}"
        )

    except asyncio.TimeoutError:
        print("\nERROR: Server khong phan hoi (timeout).")

    except Exception as error:
        print(f"\nERROR: {error}")

    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
