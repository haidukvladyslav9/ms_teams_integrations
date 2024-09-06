from msgraph import GraphServiceClient
from msgraph.generated.models.user import User
from typing import List, Optional

class TeamsTeamFetcher:
    def __init__(self, access_token: str):
        self.client = GraphServiceClient(credential={"access_token": access_token})

    async def get_teams(self):
        response = await self.client.teams.get()
        return response.value