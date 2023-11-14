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

    dht11Device = adafruit_dht.DHT11(board.D4)

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        sensor = cls(config.name)
        sensor.reconfigure(config, dependencies)
        return sensor

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        
        dht11Device = config.attributes.fields["dht11Device"].number_value
        readings_map = config.attributes.fields["readings_map"].struct_value
        
        if readings_map =="":
            raise NameError("Sensor map must be defined ")
        
        if dht11Device == "":
            raise Exception("Device must be defined")
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        # Initialize the resource instance
        dht11Device = int(config.attributes.fields["dht11Device"].number_value)
        self.readings_map = dict(config.attributes.fields["readings_map"].struct_value)
        return

    # Implement the methods the Viam RDK defines for the Sensor API
    async def get_readings(
        self, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None, **kwargs
    ) -> Mapping[str, Any]:
        
        dht11Device = adafruit_dht.DHT22(board.D4)

        temperature_c = dht11Device.temperature
        humidity = dht11Device.humidity

        readings = {}

        for label, dhtreadings in self.readings_map.items():
            readings[label] = temperature_c, humidity


        while True:
            try:
                return readings
        
            except RuntimeError as error:
             # Errors happen fairly often
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                dht11Device.exit()
                raise error
            
    

        


