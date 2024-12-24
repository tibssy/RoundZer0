from channels.generic.websocket import AsyncWebsocketConsumer
import json


class VoiceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            # Process the voice data received from WebRTC
            with open('test.ogg', 'wb') as file:
                file.write(bytes_data)

            print(f"Received voice data: {len(bytes_data)} bytes")
        await self.send(text_data=json.dumps({"message": "Data received"}))
