import logging
from abc import ABC, abstractmethod
from dt_maps import MapLayer
from dt_maps.types.commons import EntityHelper

from classes.basic.chain import AbstractHandler
from classes.basic.command import Command
from utils.maps import REGISTER
from mapStorage import MapStorage
from utils.maps import create_layer
from typing import Dict, Any


class AbstractLayer(ABC):
    _data: MapLayer = None
    _layer_handler: EntityHelper = None
    #_layer_name: str = ""

    def __init__(self, **kwargs) -> None:
        self.dm = MapStorage().map
        #self._layer_name = kwargs["layer_name"]
        try:
            self.data = self.dm.layers[self.layer_name()]
        except KeyError:
            logging.error(f"Empty layer {self.layer_name()}")
            create_layer(self.dm, self.layer_name(), {})
            self.data = self.dm.layers[self.layer_name()]
        self._layer_handler = REGISTER[self.layer_name()]

    def layer_name(self) -> str:
        pass
    #    return self._layer_name

    def render(self) -> None:
        pass

    @abstractmethod
    def default_conf(self) -> Dict[str, Any]:
        pass

    def check_config(self, config: Dict[str, Any]) -> bool:
        for field in config:
            map_layer_type = self._layer_handler._get_property_types(self._layer_handler, field)
            if not isinstance(config[field], map_layer_type):
                return False
        return True

    def set_layer_handler(self, handler: EntityHelper) -> None:
        self._layer_handler = handler


class BasicLayerHandler(AbstractHandler, AbstractLayer):
    def __init__(self, **kwargs) -> None:
        super(BasicLayerHandler, self).__init__(**kwargs)

    def handle(self, command: Command) -> Any:
        response = command.execute(self.data, self.layer_name(),
                                   self.default_conf(),
                                   check_config=self.check_config)
        if response:
            return response
        return super().handle(command)

    def layer_name(self) -> str:
        pass

    def default_conf(self) -> Dict[str, Any]:
        pass
