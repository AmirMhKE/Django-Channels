import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.renderers import JSONRenderer
from .serializers import MessageSerializer
from .models import Message

class ChatConsumer(WebsocketConsumer):
    def new_message(self, data):
        print("New message!")

    def fetch_message(self, data):
        qs = Message.last_message(self)
        message_json = self.message_serializer(qs)
        content = {
            "message": eval(message_json),
        }
        self.chat_message(content)

    def message_serializer(self, qs):
        serialized = MessageSerializer(qs, many=True)
        content = JSONRenderer().render(serialized.data)
        return content

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    commands = {
        "new_message": new_message,
        "fetch_message": fetch_message,
    }

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_dict = json.loads(text_data)
        message = text_data_dict.get("message")
        command = text_data_dict["command"]

        self.commands[command](self, message)

    def send_to_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )

    def chat_message(self, event):
        message = event["message"]

        self.send(json.dumps({
            "message": message
        }))