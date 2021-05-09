import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model
from .serializers import MessageSerializer
from .models import Message, Chat

user = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def new_message(self, data):
        message = data["message"]
        author = data["username"]
        room_name = data["room_name"]
        user_model = user.objects.filter(username=author)[0]
        chat_model = Chat.objects.get(room_name=room_name)
        message_model = Message.objects.create(message_type="txt", author=user_model, content=message, related_chat=chat_model)
        result = eval(self.message_serializer(message_model))
        self.send_to_chat_message(result)

    def fetch_message(self, data):
        room_name = data["room_name"]
        qs = Message.last_message(self, room_name)
        message_json = self.message_serializer(qs)
        content = {
            "message": eval(message_json),
            "command": "fetch_message"
        }
        self.chat_message(content)

    def new_image(self, data):
        author = data["__str__"]
        room_name = data["room_name"]
        user_model = user.objects.filter(username=author)[0]
        chat_model = Chat.objects.get(room_name=room_name)
        message_model = Message.objects.create(message_type="img", author=user_model, 
        content=data["content"], related_chat=chat_model)
        self.send_to_chat_message(data)

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
        "img": new_image
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
        command = message.get("command")

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "content": message["content"],
                "command": (lambda command: "img" if command == "img" else "new_message")(command),
                "__str__": message["__str__"]
            }
        )

    def chat_message(self, event):
        self.send(json.dumps(event))