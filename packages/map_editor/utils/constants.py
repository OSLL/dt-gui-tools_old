OBJECTS_TYPES = ["watchtowers", "citizens", "vehicles", "ground_tags"]
NOT_DRAGGABLE = ["tiles"]
LAYERS_WITH_TYPES = ["traffic_signs", "tiles"]
KNOWN_LAYERS = ["frames", "tiles", "tile_maps", "watchtowers", "citizens",
                "traffic_signs", "ground_tags", "vehicles"]
REQUIRED_LAYERS = ["tiles.yaml", "frames.yaml", "tile_maps.yaml"]
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
    "tiles": {"type": TILE_TYPES},
    "traffic_signs": {"type": TRAFFIC_SIGNS_TYPES},
    "citizens": {"color": CITIZENS_COLORS},
    "vehicles": {"color": VEHICLES_COLORS, "configuration": VEHICLES_CONFIGURATION},
    "watchtowers": {"configuration": WATCHTOWERS_CONFIGURATION}
}
CTRL = 16777249
