"""Support for MrBond Airer."""
import logging
from . import MiioEntity, DOMAIN

from homeassistant.components.cover import CoverEntity, ATTR_POSITION
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.event import async_call_later

_LOGGER = logging.getLogger(__name__)

AIRER_DURATION = 10


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the light from config."""
    async_add_entities([MrBondAirer(hass, discovery_info, hass.data[DOMAIN])], True)


class MrBondAirer(MiioEntity, CoverEntity, RestoreEntity):
    """Representation of a cover."""

    def __init__(self, hass, name, device):
        """Initialize the light device."""
        super().__init__(hass, name ,device, True)
        self._device.status['airer_location'] = '1'

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        _LOGGER.debug("async_added_to_hass: %s", last_state)
        if last_state:
            location = last_state.attributes.get('airer_location')
            if location is not None:
                self._device.status['airer_location'] = location
                _LOGGER.debug("Restore location: %s", location)

    @property
    def icon(self):
        """Return the name of the device if any."""
        return 'mdi:hanger'

    @property
    def current_cover_position(self):
        """Return current position of cover.

        None is unknown, 0 is closed, 100 is fully open.
        """
        location = self._device.status.get('airer_location')
        return 0 if location == '2' else (50 if location == '0' else 100)

    @property
    def is_opening(self):
        """Return if the cover is opening or not."""
        return self._device.status.get('motor') == '1'

    @property
    def is_closing(self):
        """Return if the cover is closing or not."""
        return self._device.status.get('motor') == '2'

    @property
    def is_closed(self):
        """Return if the cover is closed or not."""
        return self._device.status.get('airer_location') == '2'

    def open_cover(self, **kwargs):
        """Open the cover."""
        _LOGGER.debug("open_cover: %s", kwargs)
        if self._device.control('set_motor', 1):
            self._device.status['airer_location'] = '1'
            _LOGGER.debug("open_cover success: %s", self._device.status)

    def close_cover(self, **kwargs):
        """Close cover."""
        _LOGGER.debug("close_cover: %s", kwargs)
        if self._device.control('set_motor', 2):
            self._device.status['airer_location'] = '2'

    def stop_cover(self, **kwargs):
        """Stop the cover."""
        _LOGGER.debug("stop_cover: %s", kwargs)
        self.pause_cover()

    def pause_cover(self):
        """Stop the cover."""
        if self._device.control('set_motor', 0):
            self._device.status['motor'] == '0'
            self._device.status['airer_location'] = '0'

    def set_cover_position(self, **kwargs):
        """Move the cover to a specific position."""
        _LOGGER.debug("set_cover_position: %s", kwargs)
        position = kwargs.get(ATTR_POSITION)
        if position <= 0:
            self.close_cover()
        elif position >= 100:
            self.open_cover()
        else:
            location = self._device.status.get('airer_location')
            if location == '1':
                self.close_cover()
                self._device.status['motor'] == '2'
            elif location == '2':
                self.open_cover()
                self._device.status['motor'] == '1'
            else:
                return
            async_call_later(self.hass, AIRER_DURATION/2, self.pause_cover)
