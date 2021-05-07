import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model
from .serializers import MessageSerializer
from .models import Message

user = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def new_message(self, data):
        message = data["message"]
        author = data["username"]
        user_model = user.objects.filter(username=author)[0]
        message_model = Message.objects.create(author=user_model, content=message)
        result = self.message_serializer(message_model)
        result = eval(result)["content"]
        self.send_to_chat_message(result)

    def fetch_message(self, data):
        qs = Message.last_message(self)
        message_json = self.message_serializer(qs)
        content = {
            "message": eval(message_json),
            "command": "fetch_message"
        }
        self.chat_message(content)

    def message_serializer(self, qs):
        qs_func = lambda qs: True if qs.__class__.__name__ == "QuerySet" else False
        serialized = MessageSerializer(qs, many=qs_func(qs))
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
        command = text_data_dict["command"]

        self.commands[command](self, text_data_dict)

    def send_to_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "command": "new_message"
            }
        )

    def chat_message(self, event):
        self.send(json.dumps(event))