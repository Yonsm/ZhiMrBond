"""Support for MrBond Airer's Light."""
from . import MiioEntity, DOMAIN
from homeassistant.components.light import LightEntity

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the light from config."""
    async_add_entities([MrBondLight(hass, discovery_info + '灯', hass.data[DOMAIN])])


class MrBondLight(MiioEntity, LightEntity):
    """Representation of MrBond Airer Light."""

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._device.status.get('led') == '1'

    def turn_on(self, **kwargs):
        """Turn the light on."""
        if self._device.control('set_led', 1):
            self._device.status['led'] = '1'

    def turn_off(self, **kwargs):
        """Turn the light off."""
        if self._device.control('set_led', 0):
            self._device.status['led'] = '0'
