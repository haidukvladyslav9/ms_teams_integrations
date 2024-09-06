from msgraph import GraphServiceClient
from msgraph.generated.models.chat_message import ChatMessage
from msgraph.generated.models.item_body import ItemBody

class TeamsChatFetcher:
    def __init__(self, client: GraphServiceClient):
        self.client = client

    async def get_chat_messages(self, chat_id: str):
        response = await self.client.chats.by_chat_id(chat_id).messages.get()
        messages = response.value
        while response is not None and response.odata_next_link is not None:
            response = await self.client.chats.by_chat_id(chat_id).messages.with_url(response.odata_next_link).get()
            messages.extend(response.value)

        return messages

    async def send_message_to_chat(self, chat_id: str, content: str):
        request_body = ChatMessage(
            body = ItemBody(
                content = content,
            ),
        )
        response = await self.client.chats.by_chat_id(chat_id).messages.post(request_body)
        return response
    
    async def soft_delete_chat_message(self, user_id: str, chat_id: str, chat_message_id: str):
        await self.client.users.by_user_id(user_id).chats.by_chat_id(chat_id).messages.by_chat_message_id(chat_message_id).soft_delete.post()
