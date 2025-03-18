import asyncio
import click
import websockets
from aioconsole import ainput

async def receive_messages(websocket):
    try:
        async for message in websocket:
            print(f"\nReceived from server: {message}")
    except websockets.ConnectionClosed:
        print("Connection to server closed.")

async def send_messages(websocket):
    try:
        while True:
            # 异步获取用户输入
            message = await ainput("Enter your message: ")
            await websocket.send(message)
    except websockets.ConnectionClosed:
        print("Connection to server closed.")

async def main(host):
    url = "ws://" + host
    async with websockets.connect(url) as websocket:
        print("Connected to WebSocket server!")

        receive_task = asyncio.create_task(receive_messages(websocket))
        send_task = asyncio.create_task(send_messages(websocket))

        await asyncio.gather(receive_task, send_task)


@click.command()
@click.argument('host')
def ws(host):
    """ ws is a command client for websocket,
    you can use it like:  
    
    ws localhost:8088/ws

    and into a loop to send msg and recevie msg
    """
    asyncio.run(main(host))


if __name__ == "__main__":
    ws()
