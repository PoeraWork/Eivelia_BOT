import asyncio,json
from nonebot import require,get_driver,get_bot
from nonebot.log import logger
from nonebot.plugin import PluginMetadata

from eivelia_bot.plugins.mqtt.mqtt import get_client

driver = get_driver()
require('mqtt')

__plugin_meta__ = PluginMetadata(
    name="火灾报警",
    description="基于mqtt协议的火灾报警插件",
    usage='火警状态',
    extra={"author": "Poera and Eivelia"},
)


def on_message(client, topic, payload, qos, properties):
    logger.info(f'{topic} RECV MSG:'+str(json.loads(payload)))

@driver.on_startup
async def live():
    await asyncio.sleep(3)
    client = get_client(__plugin_meta__.name)
    client.subscribe('poera_out',qos=1)
    client.on_message = on_message