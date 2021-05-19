from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ChatSerializer
from Chat.models import Chat

class ChatList(ViewSet):
    permission_classes = [IsAuthenticated]

    def chat_lists(self, request):
        filter_contains = request.GET.get("contains")
        if not filter_contains:
            queryset = Chat.objects.all().order_by("-id")
        else:
            queryset = Chat.objects.filter(room_name__icontains=filter_contains).order_by("-id")

        serializer = ChatSerializer(queryset, many=True)
        return Response(serializer.data)