"""
This file registers the model with the Python SDK.
"""

from viam.components.sensor import Sensor
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .dht11 import dht11

Registry.register_resource_creator(Sensor.SUBTYPE, dht11.MODEL, ResourceCreatorRegistration(dht11.new, dht11.validate))
