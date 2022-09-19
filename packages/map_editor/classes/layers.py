import logging
from abc import ABC
from dt_maps import MapLayer
from dt_maps.types.commons import EntityHelper
from dt_maps.Map import REGISTER
from classes.basic.command import Command
from utils.maps import create_layer
from mapStorage import MapStorage
from typing import Dict, Any, Type
from classes.basic.chain import AbstractHandler


class AbstractLayer(ABC):
    _data: MapLayer = None
    _layer_handler: EntityHelper = None
    _layer_name: str = ""
    _default_conf: Dict[str, Any] = {}

    def __init__(self, layer_name: str) -> None:
        self.dm = MapStorage().map
        self._layer_name = layer_name
        print(layer_name)

        try:
            self.data = self.dm.layers[self.layer_name]
        except KeyError:
            print("create layer", layer_name)
            logging.error(f"Empty layer {self.layer_name}")
            create_layer(self.dm, self.layer_name, {})
            self.data = self.dm.layers[self.layer_name]
        #print(REGISTER)
        self._layer_handler = REGISTER[self.layer_name]

    @property
    def layer_name(self) -> str:
        return self._layer_name

    def render(self) -> None:
        pass

    def default_conf(self) -> Dict[str, Any]:
        return self._default_conf

    def check_config(self, config: Dict[str, Any]) -> bool:
        if not config:
            return True
        for field in config:
            try:
                map_layer_type = self._layer_handler._get_property_types(
                    self._layer_handler, field)
            except TypeError:
                map_layer_type = self._layer_handler._get_property_types(
                    field)
            if not isinstance(config[field], map_layer_type):
                return False
        return True

    def set_layer_handler(self, handler: EntityHelper) -> None:
        self._layer_handler = handler


class BasicLayerHandler(AbstractLayer, AbstractHandler):
    def __init__(self, layer_name: str, fields: list = None):
        super(BasicLayerHandler, self).__init__(layer_name)
        if fields and len(fields) != 0:
            conf = {}
            for field in fields:
                conf[field] = ""
            self._default_conf = conf

    def handle(self, command: Command) -> Any:
        response = command.execute(self.dm, self.data, self.layer_name,
                                   self.default_conf(),
                                   check_config=self.check_config)
        if response:
            return response
        return super().handle(command)


class DynamicLayer(EntityHelper):
    _fields: Dict[str, str] = {}
    _layer_name: str = ""
    _map = None

    def __init__(self, fields: list, layer_name: str, map):
        super(DynamicLayer, self).__init__(map, layer_name)
        self._layer_name = layer_name
        for field_type in fields:
            self._fields[field_type] = ""
            setattr(self, field_type, "")

    def _get_property_values(self, name: str) -> str:
        return self._fields[name]

    def _get_property_types(self, name: str) -> Type[str]:
        return str

    def _get_layer_name(self) -> str:
        return self._layer_name
