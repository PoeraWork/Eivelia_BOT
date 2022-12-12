import asyncio
import json

from gmqtt import Client
from eivelia_bot.config import Config

from nonebot import require, get_driver, get_bot
from nonebot.log import logger
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Bot

driver = get_driver()
config = Config.parse_obj(driver.config)

try:
    client:Client = require('mqtt').client
    if isinstance(client,Client):
        logger.debug('client加载完成')
except RuntimeError:
    logger.error('插件加载失败')

__plugin_meta__ = PluginMetadata(
    name="火灾报警",
    description="基于mqtt协议的火灾报警插件",
    usage='火警状态',
    extra={"author": "Poera and Eivelia"},
)


async def on_message(client, topic, payload, qos, properties):
    if json.loads(payload)['state'] == "fire":
        try:
            bot = get_bot()
            if isinstance(bot, Bot):
                await bot.send_private_msg(user_id=config.fire_repo_user_id, message="fire!warning!")
        except KeyError:
            logger.info('no bot')
    logger.warning(f'{topic} RECV MSG:'+str(json.loads(payload)))

async def on_connect(client, flags, rc, properties):
    try:
        bot = get_bot()
        if isinstance(bot, Bot):
            await bot.send_private_msg(user_id=config.fire_repo_user_id, message="火灾报警系统连接成功")
    except KeyError:
        logger.warning('no bot')
    logger.info("connected")

async def on_disconnect(client, packet, exc=None):
    try:
        bot = get_bot()
        if isinstance(bot, Bot):
            await bot.send_private_msg(user_id=config.fire_repo_user_id, message="warning!火灾报警系统失联，请迅速前往查看")
    except KeyError:
        logger.warning('no bot')
    logger.info("connected")
    logger.info('Disconnected')

@driver.on_startup
async def live():
    await asyncio.sleep(3)
    client.subscribe('poera_out', qos=1)
    client.on_message = on_message
    client.on_connect = on_connect
