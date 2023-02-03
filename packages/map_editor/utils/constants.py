TILES = "tiles"
FRAMES = "frames"
FRAME = "frame"
TILE_MAPS = "tile_maps"
TILE_SIZE = "tile_size"
WATCHTOWERS = "watchtowers"
TRAFFIC_SIGNS = "traffic_signs"
GROUND_TAGS = "ground_tags"
VEHICLES = "vehicles"
CITIZENS = "citizens"
NEW_CONFIG = "new_config"
RELATIVE_TO = "relative_to"
LAYER_NAME = "layer_name"
OBJECTS_TYPES = [WATCHTOWERS, CITIZENS, VEHICLES, GROUND_TAGS]
NOT_DRAGGABLE = [TILES]
LAYERS_WITH_TYPES = [TRAFFIC_SIGNS, TILES]
KNOWN_LAYERS = [FRAMES, TILES, TILE_MAPS, WATCHTOWERS, CITIZENS,
                TRAFFIC_SIGNS, GROUND_TAGS, VEHICLES]
REQUIRED_LAYERS = [f"{TILES}.yaml", f"{FRAMES}.yaml", f"{TILE_MAPS}.yaml"]
TILE_KIND = ('block', 'road')
TILE_TYPES = ("straight", "curve", "3way", "4way", "asphalt", "grass", "floor")
TRAFFIC_SIGNS_TYPES = ("stop", "yield", "no_right_turn", "no_left_turn",
                       "do_not_enter", "oneway_right", "oneway_left",
                        "four_way_intersect", "right_t_intersect",
                        "left_t_intersect", "t_intersection", "pedestrian",
                        "t_light_ahead", "duck_crossing", "parking")
WATCHTOWERS_CONFIGURATION = ("WT18", "WT19")
VEHICLES_CONFIGURATION = ("DB18", "DB19", "DB20", "DB21M", "DB21J", "DB21R", "DD18", "DD21")
CITIZENS_COLORS = ("yellow", "red", "green", "grey")
VEHICLES_COLORS = ("blue", "red", "green", "grey")
FORM_DICT = {
    TILES: {"type": TILE_TYPES},
    TRAFFIC_SIGNS: {"type": TRAFFIC_SIGNS_TYPES},
    CITIZENS: {"color": CITIZENS_COLORS},
    VEHICLES: {"color": VEHICLES_COLORS, "configuration": VEHICLES_CONFIGURATION},
    WATCHTOWERS: {"configuration": WATCHTOWERS_CONFIGURATION}
}
CTRL = 16777249