from teams_api import TeamsApiHelper
from teams_chat import TeamsChatFetcher
from teams_channels import TeamsChannelsFetcher
from teams_groups import TeamsGroupFetcher
from teams_teams import TeamsTeamFetcher
from typing import Optional

team_id = 'aba'
conversation_id = 'aba'
chat_id = 'aba'

client = TeamsApiHelper.create_graph_client()
channelsFetcher = TeamsChannelsFetcher(client=client, team_id=team_id)
chatFetcher = TeamsChatFetcher(client=client)
groupFetcher = TeamsGroupFetcher(client=client)
teamFetcher = TeamsTeamFetcher(client=client)

async def fetch_all_teams():
    return await teamFetcher.get_teams()

async def fetch_all_groups():
    return await groupFetcher.get_groups()

async def fetch_all_channels():
    teams = await fetch_all_teams()
    channels = []
    if teams is None:
        return []
    
    for team in teams:
        if team:
            teamChannelsFetcher = TeamsChannelsFetcher(client=client, team_id=team.id)
            _channels = teamChannelsFetcher.get_channels()
            channels.extend(_channels)
    return channels

async def fetch_group_chat_messages(group_id: str):
    conversations = await groupFetcher.get_group_conversations(group_id)
    all_threads = []

    if conversations == None:
        return all_threads

    for conversation in conversations:
        if conversation.threads:
            all_threads.extend(conversation.threads)  

    return all_threads

async def fetch_private_chat_messages(chat_id: str):
    return await chatFetcher.get_chat_messages(chat_id)

async def fetch_channel_messages(channel_id: str):
    return await channelsFetcher.get_channel_messages(channel_id)

async def fetch_post(group_id: str, conversation_id: str, conversation_thread_id: str, post_id: str):
    return await groupFetcher.get_group_conversation_thread_post(group_id, conversation_id, conversation_thread_id, post_id)

async def send_message(content: str, chat_id: Optional[str] = None, channel_id: Optional[str] = None, team_id: Optional[str] = None):
    if chat_id is None:
        if channel_id is None or team_id is None:
            raise Exception("Could not find TeamsAppConfig for the provided organization ID")
        await TeamsChannelsFetcher(client=client, team_id=team_id).send_message_to_channel(channel_id, content)

    await chatFetcher.send_message_to_chat(chat_id, content)

async def delete_message(chat_message_id: str, user_id: Optional[str], chat_id: Optional[str] = None, channel_id: Optional[str] = None, team_id: Optional[str] = None):
    if chat_id is None:
        if channel_id is None or team_id is None:
            raise Exception("Could not find team_id & channel_id")
        await TeamsChannelsFetcher(client=client, team_id=team_id).soft_delete_message_in_channel(channel_id, chat_message_id)
    if user_id is None:
        raise Exception("Could not find user_id")
    await chatFetcher.soft_delete_chat_message(user_id, chat_id, chat_message_id)