
from ..zhimi.entity import ZhiMIoTEntity, ZHI_MIOT_SCHEMA
from .mrbond_airer_m1pro import *
from homeassistant.components.light import LightEntity, PLATFORM_SCHEMA

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(ZHI_MIOT_SCHEMA)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([ZhiMrBondLight(config)], True)


class ZhiMrBondLight(ZhiMIoTEntity, LightEntity):

    def __init__(self, conf):
        super().__init__({SRV_Light: [PROP_Switch_Status]}, conf)

    @property
    def is_on(self):
        return self.data[PROP_Switch_Status]

    async def async_turn_on(self, **kwargs):
        await self.async_control(SRV_Light, PROP_Switch_Status, True)

    async def async_turn_off(self, **kwargs):
        await self.async_control(SRV_Light, PROP_Switch_Status, False)
