from msgraph import GraphServiceClient
from msgraph.generated.teams.item.channels.get_all_messages.get_all_messages_request_builder import GetAllMessagesRequestBuilder
from msgraph.generated.models.chat_message import ChatMessage
from msgraph.generated.models.item_body import ItemBody

class TeamsChannelsFetcher:
    def __init__(self, client: GraphServiceClient, team_id: str):
        self.client = client
        self.team = client.teams.by_team_id(team_id)

    async def get_channels(self):
        response = await self.team.all_channels.get()
        return response.value
    
    async def get_all_channels_messages(self, params):
        response = await self.team.channels.get_all_messages.get()
        messages = response.value
        while response is not None and response.odata_next_link is not None:
            response = await self.team.channels.get_all_messages.with_url(response.odata_next_link).get()
            messages.extend(response.value)

        return messages
    
    async def get_channel_members(self, channel_id: str): 
        response = await self.team.channels.by_channel_id(channel_id).members.get()
        members = response.value
        while response is not None and response.odata_next_link is not None:
            response = await self.team.channels.get_all_messages.with_url(response.odata_next_link).get()
            members.extend(response.value)

        users = []
        if members and members.value:
            for member in members.value:
                user = await self.client.users.by_user_id(member.id).get()
                users.append(user)
        return users

    async def get_channel_messages(self, channel_id: str):
        response = await self.team.channels.by_channel_id(channel_id).messages.get()
        messages = response.value
        while response is not None and response.odata_next_link is not None:
            response = await self.team.channels.by_channel_id(channel_id).messages.with_url(response.odata_next_link).get()
            messages.extend(response.value)

        return messages
    
    async def get_message(self, channel_id: str, chat_message_id: str):
        return await self.team.channels.by_channel_id(channel_id).messages.by_chat_message_id(chat_message_id).get()

    async def send_message_to_channel(self, channel_id: str, content: str):
        request_body = ChatMessage(
            body = ItemBody(
                content = content,
            ),
        )
        result = await self.team.channels.by_channel_id(channel_id).messages.post(request_body)
        return result
    
    async def soft_delete_message_in_channel(self, channel_id: str, chat_message_id: str):
        await self.team.channels.by_channel_id(channel_id).messages.by_chat_message_id(chat_message_id).soft_delete.post()
