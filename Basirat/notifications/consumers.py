# import json
# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
# from main.models import Group, Student
# from .models import Message
# from django.utils import timezone
#
#
# class NotificationConsumer(WebsocketConsumer):
#     def connect(self):
#         self.user = self.scope["user"]
#         if self.user.is_authenticated:
#             self.accept()
#             self.subscribe_to_notifications()
#             self.send_existing_messages()
#         else:
#             self.close()
#
#     def disconnect(self, close_code):
#         self.unsubscribe_from_notifications()
#
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         group_id = text_data_json.get('group')
#         message_text = text_data_json.get('message')
#
#         if group_id and message_text:
#             try:
#                 group = Group.objects.get(pk=group_id)
#                 sender = self.user
#                 message = Message.objects.create(group=group, sender=sender, message=message_text)
#                 self.send_message(message)
#             except Group.DoesNotExist:
#                 pass
#
#     def subscribe_to_notifications(self):
#         if not self.user.is_staff:
#             student = Student.objects.get(user=self.user)
#             self.room_group_name = f"notifications_{student.user.username}"
#
#             async_to_sync(self.channel_layer.group_add)(
#                 self.room_group_name,
#                 self.channel_name
#             )
#
#     def unsubscribe_from_notifications(self):
#         if hasattr(self, 'room_group_name'):
#             async_to_sync(self.channel_layer.group_discard)(
#                 self.room_group_name,
#                 self.channel_name
#             )
#
#     def send_message(self, message):
#         self.send(text_data=json.dumps({
#             'type': 'notification',
#             'message': message.message,
#             'sender': message.sender.username,
#             'timestamp': message.created_at.timestamp()  # Unix timestamp
#         }))
#
#     def send_existing_messages(self):
#         if not self.user.is_staff:
#             student = Student.objects.get(user=self.user)
#             group_messages = Message.objects.filter(group=student.group,
#                                                     created_at__gte=timezone.now() - timezone.timedelta(days=5))
#             for message in group_messages:
#                 self.send_message(message)
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Subquery, CharField, Q, OuterRef
from main.models import Group, Student
from .models import Message
from django.utils import timezone


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.accept()
            await self.subscribe_to_notifications()
            await self.send_existing_messages()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.unsubscribe_from_notifications()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        group_id = text_data_json.get('group')
        message_text = text_data_json.get('message')

        if group_id and message_text:
            try:
                group = await self.get_group(group_id)
                sender = self.user
                message = await self.create_message(group, sender, message_text)
                await self.send_message(message)
            except Group.DoesNotExist:
                pass

    async def subscribe_to_notifications(self):
        if not self.user.is_staff:
            self.room_group_name = f"notifications_{self.user.username}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def unsubscribe_from_notifications(self):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_message(self, message):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message.message,
            'sender': message.sender.username,
            'timestamp': message.created_at.timestamp()  # Unix timestamp-
        }))

    async def send_existing_messages(self):
        if not self.user.is_staff:
            # student = await self.get_student()
            group = await self.get_student_group()
            group_messages = await self.get_group_messages(group)
            for message in group_messages:
                print(f"###########################{message.message}")
                await self.send_message(message)

    # Helper functions for asynchronous database access
    async def get_group(self, group_id):
        return await database_sync_to_async(Group.objects.get)(pk=group_id)

    async def get_student(self):
        return await database_sync_to_async(Student.objects.get)(user=self.user)

    async def get_student_username(self):
        student = await database_sync_to_async(Student.objects.get)(user=self.user)
        return await database_sync_to_async(student.user.username)()

    async def create_message(self, group, sender, message_text):
        return await database_sync_to_async(Message.objects.create)(group=group, sender=sender, message=message_text)

    async def get_group_messages(self, group):
        return await database_sync_to_async(Message.objects.filter)(group=group,
                                                                    created_at__gte=timezone.now() - timezone.timedelta(
                                                                        days=5))

    async def get_student_group(self):
        return await database_sync_to_async(Group.objects.get)(student__user=self.user)
