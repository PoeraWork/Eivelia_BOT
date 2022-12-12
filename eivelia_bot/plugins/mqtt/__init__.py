# -*- coding: utf-8 -*-
import nonebot

from eivelia_bot.config import Config
from nonebot.log import logger
from gmqtt import Client as MQTTClient

driver = nonebot.get_driver()
config = Config.parse_obj(driver.config)
client: MQTTClient = MQTTClient(config.mqtt_client_id)

def on_connect(client, flags, rc, properties):
    client.subscribe(config.mqtt_topic, qos=0)
    logger.info("connected")


def on_message(client, topic, payload, qos, properties):
    logger.info('RECV MSG:'+str(payload))


def on_disconnect(client, packet, exc=None):
    logger.info('Disconnected')


def on_subscribe(client, mid, qos, properties):
    logger.info('SUBSCRIBED')


@driver.on_startup
async def client_init() -> MQTTClient:
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    if config.mqtt_user:
        client.set_auth_credentials(config.mqtt_user, str(config.mqtt_password))
    await client.connect(config.mqtt_host, config.mqtt_port)
    logger.debug('conect '+str(config.mqtt_host)+' '+str(config.mqtt_port))
    return client

@driver.on_shutdown
async def disconnect():
    await client.disconnect()
