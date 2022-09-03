from __future__ import annotations
from pathlib import Path
from typing import Any, Dict
from utils.constants import TILES, TILE_SIZE, TILE_MAPS, WATCHTOWERS, \
    FRAMES, TRAFFIC_SIGNS, GROUND_TAGS, VEHICLES, CITIZENS
from mapStorage import MapStorage
from classes.layers import BasicLayer
from classes.basic.command import Command
from classes.MapDescription import MapDescription
from classes.Commands.GetLayerCommand import GetLayerCommand
from dt_maps.types.watchtowers import WatchtowerType
from dt_maps.types.tiles import TileType
from dt_maps.types.traffic_signs import TrafficSignType
from dt_maps.types.citizens import CitizenType
from dt_maps.types.vehicles import VehicleType, ColorType


class TilesLayerHandler(BasicLayer):
    def __init__(self) -> None:
        super(TilesLayerHandler, self).__init__(TILES)

    def handle(self, command: Command) -> Any:
        response = command.execute(self.dm, self.data, self.layer_name,
                                   self.default_conf(),
                                   check_config=self.check_config)
        if response:
            return response
        return super().handle(command)

    def default_conf(self) -> Dict[str, Any]:
        return {'i': 0, 'j': 0, 'k': 0, 'type': 'floor'}

    def check_config(self, config: Dict[str, Any]) -> bool:
        return super().check_config(config) and config.get("type") \
               in [t.value for t in TileType]


class WatchtowersLayerHandler(BasicLayer):
    def __init__(self) -> None:
        super(WatchtowersLayerHandler, self).__init__(WATCHTOWERS)

    def handle(self, command: Command) -> Any:
        response = command.execute(self.dm, self.data, self.layer_name,
                                   self.default_conf(),
                                   check_config=self.check_config)
        if response:
            return response
        return super().handle(command)

    def default_conf(self) -> Dict[str, str]:
        return {'configuration': 'WT18', 'id': ""}

    def check_config(self, config: Dict[str, Any]) -> bool:
        return super().check_config(config) and config.get("configuration") \
               in [t.value for t in WatchtowerType]


class FramesLayerHandler(BasicLayer):
    def __init__(self) -> None:
        super(FramesLayerHandler, self).__init__(FRAMES)

    def default_conf(self) -> Dict[str, Any]:
        return {'pose': {'x': 1.0, 'y': 1.0, 'z': 0.0, 'yaw': 0.0, 'roll': 0.0,
                         'pitch': 0.0}, 'relative_to': ""}

    def handle(self, command: Command) -> Any:
        response = command.execute(self.dm, self.data, self.layer_name,
                                   self.default_conf(),
                                   check_config=self.check_config)
        if response:
            return response
        return super().handle(command)


class TileMapsLayerHandler(BasicLayer):
    def __init__(self) -> None:
        super(TileMapsLayerHandler, self).__init__(TILE_MAPS)

    def default_conf(self) -> Dict[str, Any]:
        return {TILE_SIZE: {'x': 0.585, 'y': 0.585}}

    def handle(self, command: Command) -> Any:
        response = command.execute(self.dm, self.data, self.layer_name,
                                   self.default_conf())
        if response:
            return response
        return super().handle(command)


class TrafficSignsLayerHandler(BasicLayer):
    def __init__(self) -> None:
        super(TrafficSignsLayerHandler, self).__init__(TRAFFIC_SIGNS)

    def handle(self, command: Command) -> Any:
        response = command.execute(self.dm, self.data, self.layer_name,
                                   self.default_conf(),
                                   check_config=self.check_config)
        if response:
            return response
        return super().handle(command)

    def default_conf(self) -> Dict[str, Any]:
        return {"type": "stop", "id": 0, "family": "36h11"}

    def check_config(self, config: Dict[str, Any]) -> bool:
        return super().check_config(config) and \
               config.get("type") in [t.value for t in TrafficSignType]


class GroundTagsLayerHandler(BasicLayer):
    def __init__(self) -> None:
        super(GroundTagsLayerHandler, self).__init__(GROUND_TAGS)

    def default_conf(self) -> Dict[str, Any]:
        return {"size": 0.15, "id": 0, "family": "36h11"}

    def handle(self, command: Command) -> Any:
        response = command.execute(self.dm, self.data, self.layer_name,
                                   self.default_conf(),
                                   check_config=self.check_config)
        if response:
            return response
        return super().handle(command)


class CitizensLayerHandler(BasicLayer):
    def __init__(self) -> None:
        super(CitizensLayerHandler, self).__init__(CITIZENS)

    def handle(self, command: Command) -> Any:
        response = command.execute(self.dm, self.data, self.layer_name,
                                   self.default_conf(),
                                   check_config=self.check_config)
        if response:
            return response
        return super().handle(command)

    def default_conf(self) -> Dict[str, Any]:
        return {"color": "yellow"}

    def check_config(self, config: Dict[str, Any]) -> bool:
        return super().check_config(config) and \
               config.get("color") in [t.value for t in CitizenType]


'''class VehiclesHandler(BasicLayer):
    def __init__(self) -> None:
        super(VehiclesHandler, self).__init__(VEHICLES)

    def handle(self, command: Command) -> Any:
        response = command.execute(self.dm, self.data, self.layer_name,
                                   self.default_conf(),
                                   check_config=self.check_config)
        if response:
            return response
        return super().handle(command)

    def default_conf(self) -> Dict[str, Any]:
        return {"color": "blue", "configuration": "DB18", "id": 0}

    def check_config(self, config: Dict[str, Any]) -> bool:
        return super().check_config(config) and \
               config.get("configuration") in [t.value for t in VehicleType] and \
               config.get("color") in [t.value for t in ColorType]'''


if __name__ == '__main__':
    MapStorage(MapDescription(Path("./maps/tm1"), "test"))
    tile_layer = TilesLayerHandler()
    watchtower_layer = WatchtowersLayerHandler()
    tile_layer.set_next(watchtower_layer)
    layer = tile_layer

    # while layer:
    print(layer.handle(GetLayerCommand("watchtowers")))
