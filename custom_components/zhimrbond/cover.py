from ..zhi.cover import ZhiTravelCover
from ..zhi.entity import ZhiEntity
from ..zhimi import miio_service
from ..zhimi.entity import CONF_DID, ZHI_MIOT_SCHEMA
from .mrbond_airer_m1pro import SRV_Airer, PROP_Motor_Control, VALUE_Motor_Control
from homeassistant.components.cover import PLATFORM_SCHEMA

AIRER_TRAVEL_TIME = 28

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(ZHI_MIOT_SCHEMA)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([ZhiMrBondAirer(config)])


class ZhiMrBondAirer(ZhiEntity, ZhiTravelCover):

    def __init__(self, conf):
        ZhiEntity.__init__(self, conf, 'mdi:hanger')
        ZhiTravelCover.__init__(self, AIRER_TRAVEL_TIME)
        self.did = conf[CONF_DID]

    async def async_control_cover(self, op):
        values = [VALUE_Motor_Control.Up, VALUE_Motor_Control.Down, VALUE_Motor_Control.Pause]
        return await miio_service.miot_control(self.did, SRV_Airer, PROP_Motor_Control, values[op]) == 0
