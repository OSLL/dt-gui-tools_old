import logging
from abc import ABC
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
    _layer_name: str = ""
    _default_conf: Dict[str, Any] = {}

    def __init__(self, **kwargs) -> None:
        self.dm = MapStorage().map
        self._layer_name = kwargs["layer_name"]
        self._default_conf = kwargs["default_conf"]
        try:
            self.data = self.dm.layers[self._layer_name]
        except KeyError:
            logging.error(f"Empty layer {self._layer_name}")
            create_layer(self.dm, self._layer_name, {})
            self.data = self.dm.layers[self._layer_name]
        self._layer_handler = REGISTER[self._layer_name]

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
        response = command.execute(self.data, self._layer_name,
                                   self._default_conf.copy(),
                                   check_config=self.check_config)
        if response:
            return response
        return super().handle(command)
