import time
from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
from typing_extensions import Self

from typing import Any, Mapping, Optional

import adafruit_dht
import board


from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.components.sensor import Sensor
from viam.logging import getLogger

from board import D4


LOGGER = getLogger(__name__)

class dht11(Sensor, Reconfigurable):

    # Defines new model's triplet 
    MODEL: ClassVar[Model] = Model(ModelFamily("arielle", "sensor"), "dht11")
    
    # Class parameters

    dhtDevice = adafruit_dht.DHT11(board.D4)

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        sensor = cls(config.name)
        sensor.reconfigure(config, dependencies)
        return sensor

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        
        dhtDevice = config.attributes.fields["dhtDevice"].number_value

        if dhtDevice == "":
            raise Exception("A some_pin must be defined")
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        # Initialize the resource instance
        dhtDevice = int(config.attributes.fields["dhtDevice"].number_value)
        return

    # Implement the methods the Viam RDK defines for the Sensor API
    async def get_readings(
        self, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None, **kwargs
    ) -> Mapping[str, Any]:
        
        dhtDevice = adafruit_dht.DHT11(board.D4)

        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity

        while True:
            try:
                return  temperature_c, temperature_f, humidity
        
            except RuntimeError as error:
             # Errors happen fairly often
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                dhtDevice.exit()
                raise error
    
        


