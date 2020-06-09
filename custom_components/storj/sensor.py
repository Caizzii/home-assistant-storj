"""Platform for sensor integration."""
import logging
from datetime import datetime

import requests
import json
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)
DEFAULT_NAME = "Storj"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PROTO = "http"
DEFAULT_PORT = "14002"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.string,
    vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
    vol.Optional(CONF_PROTOCOL, default=DEFAULT_PROTO): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([StorjSensor(config)])


class StorjSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, config):
        self._state = None
        self._name = config.get(CONF_NAME)
        self.host = config.get(CONF_HOST)
        self.protocol = config.get(CONF_PROTOCOL)
        self.port = config.get(CONF_PORT)
        self.data = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self.data

    def update(self):
        attributes = {}
        card_json = []

        stats = self.get_infos(self.protocol, self.host, self.port, self.token)

        init = {}
        """Initialized JSON Object"""
        init['node_id'] = stats['nodeID']
        init['wallet'] = stats['wallet']
        init['disk_space'] = stats['diskSpace']
        init['satellites'] = stats['satellites']
        init['icon'] = 'mdi:eye-off'
        card_json.append(init)

        attributes['data'] = json.dumps(card_json)
        if stats["success"].__eq__("True"):
            self._state = "Success"
        else:
            self._state = "Failure"
        self.data = attributes

    def get_infos(self, proto, host, port, token):
        url = "{0}://{1}:{2}/api/sno".format(
            proto,
            host, port)
        stats = requests.get(url).json()
        return stats
