import os
import time
import msal
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient

from src.config.app_config_types import TeamsAppAuth, TeamsAppConfig

load_dotenv()

class TeamsApiHelper:
    @staticmethod
    def exchange_code_for_teams_token(code, user_id):
        client_id = os.getenv("MICROSOFT_TEAMS_CLIENT_ID")
        client_secret = os.getenv("MICROSOFT_TEAMS_CLIENT_SECRET")
        tenant_id = os.getenv("MICROSOFT_TEAMS_TENANT_ID")
        redirect_uri = "https://localhost:3001/client/teams/callback"
        
        app = msal.ConfidentialClientApplication(
            client_id,
            authority=f"https://login.microsoftonline.com/{tenant_id}",
            client_credential=client_secret,
        )
        
        result = app.acquire_token_by_authorization_code(
            code,
            scopes=["api://2beae4a8-427e-438d-b8e6-5ffb67c064ce/test2"],
            redirect_uri=redirect_uri
        )

        if "access_token" in result:
            token_type = result["token_type"]
            scope = result["scope"]
            expires_in = result["expires_in"]
            expires_at = result["expires_in"] + int(time.time())
            access_token = result["access_token"]
            refresh_token = result["refresh_token"]
            tenant_id = result["id_token_claims"]["tid"]
            
            TeamsAppConfig(
                organization_id=user_id,
                teams_tenant_id=tenant_id,
            ).upsert()
            TeamsAppAuth(
                teams_tenant_id=tenant_id,
                access_token=access_token,
                token_type=token_type,
                scope=scope,
                expires_in=expires_in,
                expires_at=expires_at,
                refresh_token=refresh_token
            ).upsert()
        else:
            raise Exception("Could not obtain access token from Microsoft Graph API")
        
    @staticmethod
    def refresh_token(auth: TeamsAppAuth=None, org_id=None):
        if auth is None:
            config = TeamsAppConfig(organization_id=org_id).get()
            if config is None:
                raise Exception("Could not find TeamsAppConfig for the provided organization ID")
            auth = TeamsAppAuth(teams_tenant_id=config.teams_tenant_id).get()
            if auth is None:
                raise Exception("Could not find TeamsAppAuth for the provided organization ID")

        # Check if token is expired
        if auth.expires_at > int(time.time()):
            return auth.access_token  # Token is still valid

        client_id = os.getenv("MICROSOFT_TEAMS_CLIENT_ID")
        client_secret = os.getenv("MICROSOFT_TEAMS_CLIENT_SECRET")
        tenant_id = os.getenv("MICROSOFT_TEAMS_TENANT_ID")
        
        app = msal.ConfidentialClientApplication(
            client_id,
            authority=f"https://login.microsoftonline.com/{tenant_id}",
            client_credential=client_secret,
        )
        
        result = app.acquire_token_by_refresh_token(
            auth.refresh_token,
            scopes=["api://2beae4a8-427e-438d-b8e6-5ffb67c064ce/test2"]
        )
        if "access_token" in result:
            token_type = result["token_type"]
            scope = result["scope"]
            expires_in = result["expires_in"]
            expires_at = result["expires_in"] + int(time.time())
            access_token = result["access_token"]
            refresh_token = result["refresh_token"]
            
            TeamsAppAuth(
                teams_tenant_id=auth.teams_tenant_id,
                access_token=access_token,
                token_type=token_type,
                scope=scope,
                expires_in=expires_in,
                expires_at=expires_at,
                refresh_token=refresh_token
            ).upsert()
            return access_token
        else:
            raise Exception("Could not obtain access token from Microsoft Graph API")

    @staticmethod
    def create_graph_client():
        credential = ClientSecretCredential(
            tenant_id='TENANT_ID',
            client_id='CLIENT_ID',
            client_secret='CLIENT_SECRET',
        )
        scopes = ['https://graph.microsoft.com/.default']

        # Create an API client with the credentials and scopes
        client = GraphServiceClient(credentials=credential, scopes=scopes)
        return client