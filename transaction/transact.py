import json
from channels.generic.websocket import AsyncWebsocketConsumer

class Transaction(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(
            self.roomGroupName ,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self , close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName , 
            self.channel_layer 
        )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        code = text_data_json["code"]
        action = text_data_json["action"]
        transact_id = text_data_json["transact_id"]
        await self.channel_layer.group_send(
            self.roomGroupName,{
                "type" : "sendTransact" ,
                "code" : code , 
                "action" : action,
                "transact_id" : transact_id
            })
        
    async def sendTransact(self , event) : 
        code = event['code']
        action = event['action']
        transact_id = event['transact_id']
        await self.send(text_data=json.dumps({
            "code" : code,
            "action" : action,
            "transact_id" : transact_id
        }))