from msgraph import GraphServiceClient
from msgraph.generated.models.user import User
from typing import List

class TeamsGroupFetcher:
    def __init__(self, client: GraphServiceClient):
        self.client = client

    async def get_groups(self):
        response = await self.client.groups.get()
        return response.value
    
    async def get_group(self, group_id: str):
        group = await self.client.groups.by_group_id(group_id).get()
        return group
    
    async def get_group_members(self, group_id: str) -> List[User]: 
        members = await self.client.groups.by_group_id(group_id).members.get()
        users = []
        if members and members.value:
            for member in members.value:
                user = await self.client.users.by_user_id(member.id).get()
                users.append(user)
        return users
    
    async def get_group_conversations(self, group_id: str): 
        response = await self.client.groups.by_group_id(group_id).conversations.get()
        return response.value
    
    async def get_group_conversation_threads(self, group_id: str, conversation_id: str):
        response = await self.client.groups.by_group_id(group_id).conversations.by_conversation_id(conversation_id).get()
        return response.threads

    async def get_group_conversation_thread(self, group_id: str, conversation_id: str, conversation_thread_id: str):
        thread = await self.client.groups.by_group_id(group_id).conversations.by_conversation_id(conversation_id).threads.by_conversation_thread_id(conversation_thread_id=conversation_thread_id).get()
        return thread
                
    async def get_group_conversation_thread_post(self, group_id: str, conversation_id: str, conversation_thread_id: str, post_id: str):
        post = await self.client.groups.by_group_id(group_id).conversations.by_conversation_id(conversation_id).threads.by_conversation_thread_id(conversation_thread_id=conversation_thread_id).posts.by_post_id(post_id).get()
        return post

