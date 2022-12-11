import asyncio,json
from nonebot import require,get_driver,get_bot
from nonebot.plugin import PluginMetadata

from eivelia_bot.plugins.mqtt.mqtt import get_client

driver = get_driver()
require('mqtt')

__plugin_meta__ = PluginMetadata(
    name="测试插件",
    description="测试插件元信息",
    usage='测试',
    extra={"author": "NoneBot"},
)








@driver.on_startup
async def bot_init():
    await asyncio.sleep(5)
    topic = "poera_out"
    try:
        self_id = get_bot().self_id
    except Exception:
        self_id = 'none'
    
    msg = json.dumps({'state':True,'self_id':f'{self_id}'})
    client = get_client(__plugin_meta__.name)
    client.publish(topic,msg)