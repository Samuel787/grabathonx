from pydantic import BaseModel

class SlackRequest(BaseModel):
    team_id: str
    team_domain: str
    enterprise_id: str
    enterprise_name: str
    channel_id: str
    channel_name: str
    user_id: str
    user_name: str
    command: str
    text: str
    response_url: str
    trigger_id: str
    api_app_id: str