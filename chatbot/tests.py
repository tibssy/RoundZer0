import os
from django.test import TestCase
from asgiref.testing import ApplicationCommunicator
from chatbot.consumers import VoiceConsumer


class VoiceConsumerTest(TestCase):
    async def test_websocket_connect_disconnect(self):
        """Test WebSocket connection and disconnection."""
        consumer = VoiceConsumer(scope={"type": "websocket"})
        communicator = ApplicationCommunicator(consumer, {"type": "websocket.connect"})

        # Simulate connection
        await communicator.send_input({"type": "websocket.connect"})
        response = await communicator.receive_output()
        self.assertEqual(response["type"], "websocket.accept")

        # Simulate disconnection
        await communicator.send_input({"type": "websocket.disconnect"})
        self.assertFalse(communicator.future.done())

    async def test_receive_audio_data(self):
        """Test if audio data is processed and converted to text correctly."""
        consumer = VoiceConsumer(scope={"type": "websocket"})
        communicator = ApplicationCommunicator(consumer, {"type": "websocket.connect"})

        # Simulate connection
        await communicator.send_input({"type": "websocket.connect"})
        await communicator.receive_output()

        # Simulate receiving audio data
        audio_file_path = os.path.join(os.path.dirname(__file__), "test.ogg")
        with open(audio_file_path, "rb") as audio_file:
            test_data = audio_file.read()

            await communicator.send_input({"type": "websocket.receive", "bytes": test_data})
            response = await communicator.receive_output()

            self.assertEqual(response["type"], "websocket.send")
            self.assertIn("Data received", response["text"])
