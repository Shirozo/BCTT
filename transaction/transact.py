import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TransactionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "transaction_updates"
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        code = text_data_json.get("code", "")
        action = text_data_json.get("action", "")
        transact_id = text_data_json.get("transact_id", "")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_transact",
                "code": code,
                "action": action,
                "transact_id": transact_id
            }
        )

    async def send_transact(self, event):
        code = event['code']
        action = event['action']
        transact_id = event['transact_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "code": code,
            "action": action,
            "transact_id": transact_id
        }))
