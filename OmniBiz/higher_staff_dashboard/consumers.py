from channels.generic.websocket import AsyncWebsocketConsumer
import json


class BusinessGraphConsumerForHigherStaff(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user'].user_id
        self.room_group_name = f'higher_staff_{self.user_id}'

        # Join the room group for this owner
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def graph_update_staff(self, event):
        graph_data = event['graph_data']

        # Send updated graph data to WebSocket
        await self.send(text_data=json.dumps({
            'graph_data': graph_data
        }))
