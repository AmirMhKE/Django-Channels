from rest_framework.serializers import ModelSerializer
from Chat.models import Chat

class ChatSerializer(ModelSerializer):
    def to_representation(self, instance):
        return {
            "id": instance.id, 
            "group_name": instance.room_name, 
            "members_count": instance.members.count()
        }

    class Meta:
        model = Chat
        fields = ("id", "group_name", "members_count")