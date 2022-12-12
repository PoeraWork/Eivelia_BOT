from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    mqtt_client_id: str
    mqtt_topic: str
    mqtt_user: str
    mqtt_password: str
    mqtt_host:str
    mqtt_port:int
    fire_repo_user_id:int
