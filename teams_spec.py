
## WHAT WE CURRENTLY HAVE ##
- client_id
- client_secret
- oauth flow
-- stores msal.ConfidentialClientApplication.acquire_token_by_authorization_code details

## WHAT WE ARE LOOKING FOR ##
- implementation of teams functions for the bot


## FOUNDATIONAL ##
def fetch_group_chat_messages(...):
    all_messages = ...
    return all_messages

def fetch_private_chat_messages(...):
    all_messages = ...
    return all_messages

def fetch_channel_messages(...):
    all_posts = ...
    all_messages = []
    for post in all_posts:
        post_messages = ...
        all_messages.extend(post_messages)
    return all_messages

def fetch_post(...): ## Fetch a single post from a channel using an ID
    ...

## BONUS ##
def get_all_group_chats(...):
    ...

def get_all_private_chats(...):
    ...

def get_all_channels(...):
    ...

def send_message(...):
    ...

def delete_message(...):
    ...

def edit_message(...):
    ...

def download_file(...): ## Files from messages - specifically images
    ...

def get_bot_user_id(...):
    ...

def get_channel_users(...):
    ...

def get_permalink(...): ## Get the permalink of a message in a channel, group chat, or private chat
    ...