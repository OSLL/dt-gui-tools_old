import logging
from abc import ABC
from dt_maps import MapLayer
from dt_maps.types.commons import EntityHelper
from classes.basic.command import Command
from utils.maps import DT_MAP_LAYERS, create_layer
from mapStorage import MapStorage
from typing import Dict, Any
from classes.basic.chain import AbstractHandler


class AbstractLayer(ABC):
    _data: MapLayer = None
    _layer_handler: EntityHelper = None
    _layer_name: str = ""

    def __init__(self, layer_name: str) -> None:
        self.dm = MapStorage().map
        self._layer_name = layer_name

        try:
            self.data = self.dm.layers[self.layer_name]
        except KeyError:
            logging.error(f"Empty layer {self.layer_name}")
            create_layer(self.dm, self.layer_name, self.default_conf())
            self.data = self.dm.layers[self.layer_name]
        self._layer_handler = DT_MAP_LAYERS[self.layer_name]

    @property
    def layer_name(self) -> str:
        return self._layer_name

    def render(self) -> None:
        pass

    def default_conf(self) -> Dict[str, Any]:
        return {}

    def check_config(self, config: Dict[str, Any]) -> bool:
        for field in config:
            map_layer_type = self._layer_handler._get_property_types(self._layer_handler, field)
            if not isinstance(config[field], map_layer_type):
                return False
        return True

    def set_layer_handler(self, handler: EntityHelper) -> None:
        self._layer_handler = handler


class BasicLayer(AbstractLayer, AbstractHandler):
    def __init__(self, layer_name: str):
        super(BasicLayer, self).__init__(layer_name)

    def handle(self, command: Command) -> Any:
        response = command.execute(self.dm, self.data, self.layer_name,
                                   self.default_conf(),
                                   check_config=self.check_config)
        if response:
            return response
        return super().handle(command)
