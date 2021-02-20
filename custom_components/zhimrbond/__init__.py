import logging
from miio import Device

_LOGGER = logging.getLogger(__name__)

DOMAIN = "zhimrbond"

AIRER_PROPS = [
            "dry",
            "led",
            "motor",
            # "drytime",
            # "airer_location",
]


class MiioDevice(Device):
    """Representation of MrBond Airer Light."""

    def __init__(self, host, token):
        """Initialize the light device."""
        super().__init__(host, token)
        self.status = {}
        self.available = False
        self.update_entities = []
        self._skip_update = False
        self._retry = 0

    def update(self):
        """Fetch state from the device."""
        if self._skip_update:
            self._skip_update = False
            return

        try:
            for prop in AIRER_PROPS:
                self.status[prop] = self.send('get_prop', [prop])[0]
            _LOGGER.debug("MiioDevice update: %s", self.status)
            self.available = True
            self._retry = 0
        except Exception as exc:
            _LOGGER.error("Error on update: %s", exc)
            self._retry += 1
            if self._retry > 3:
                self.available = False

        for entity in self.update_entities:
            entity.async_schedule_update_ha_state()

    def control(self, name, value):
        try:
            result = self.send(name, [value])
            _LOGGER.debug("Response from miio control: %s", result)
            self._skip_update = True
            return result == ['ok']
        except Exception as exc:
            #import traceback
            # _LOGGER.error(traceback.format_exc())
            _LOGGER.error("Error on miio control: %s", exc)
            #self.available = False
            return None


class MiioEntity():
    """Representation of MrBond Airer Light."""

    def __init__(self, hass, name, device, should_poll=False):
        """Initialize the light device."""
        self.hass = hass
        self._name = name
        self._device = device
        self._should_poll = should_poll
        if not should_poll:
            self._device.update_entities.append(self)

    @property
    def name(self):
        """Return the name of the device if any."""
        return self._name

    @property
    def available(self):
        """Return true when state is known."""
        return self._device.available

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        return self._device.status

    @property
    def should_poll(self):
        """Return True if entity has to be polled for state.

        False if entity pushes its state to HA.
        """
        return self._should_poll

    def update(self):
        """Fetch state from the device."""
        _LOGGER.debug("%s update", self.__class__.__name__)
        if self._should_poll:
            self._device.update()


import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.const import CONF_HOST, CONF_TOKEN, CONF_NAME
from homeassistant.helpers.discovery import async_load_platform

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_HOST): cv.string,
                vol.Required(CONF_TOKEN): vol.All(cv.string, vol.Length(min=32, max=32)),
                vol.Optional(CONF_NAME): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    """Set up the MrBond Airer component."""

    conf = config[DOMAIN]
    host = conf[CONF_HOST]
    token = conf[CONF_TOKEN]
    name = conf.get(CONF_NAME) or host

    hass.data[DOMAIN] = MiioDevice(host, token)

    for component in ['light', 'cover']:
        hass.async_create_task(async_load_platform(hass, component, DOMAIN, name, config))

    return True
