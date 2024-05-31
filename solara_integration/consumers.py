import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging

logger = logging.getLogger("solara.server.django")

class KernelConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.kernel_id = self.scope['url_route']['kwargs']['kernel_id']
        self.name = self.scope['url_route']['kwargs']['name']
        await self.accept()
        logger.info(f"Solara kernel requested for kernel_id={self.kernel_id}")

    async def disconnect(self, close_code):
        logger.info(f"Disconnected kernel_id={self.kernel_id}")

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            await self.send(text_data=text_data)
        if bytes_data:
            await self.send(bytes_data=bytes_data)
