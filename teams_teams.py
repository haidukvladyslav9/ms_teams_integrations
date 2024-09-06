from msgraph import GraphServiceClient
from msgraph.generated.models.user import User
from typing import List, Optional

class TeamsTeamFetcher:
    def __init__(self, client: GraphServiceClient):
        self.client = client

    async def get_teams(self):
        response = await self.client.teams.get()
        return response.value