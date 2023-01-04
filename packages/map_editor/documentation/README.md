# Autolab map {#autolab-map-editor status=draft}


<div class='requirements' markdown="1">

Requires: Knowledge about what a Autolab is [](#part:autolab-definition)

Results: generated map for duckietown
</div>

## Map editor

You can launch the map editor, using command:

    laptop $ dts map editor

You will see:

<div figure-id="fig:editor1" figure-caption="Map editor">
  <img src="images/start.png" style='width: 25em; height:auto'/>
</div>

## How to create a new map?

You should specify sizes(width, height) of the map, the size of tiles(width, height), map name and folder for saving map.  
Default map size: (**5**, **5**)  
Default tile size: (**0.585**, **0.585**)  
Default map name: **map_1**  
Default folder: **./maps/map1**

<div figure-id="fig:editor2" figure-caption="How to create new map">
  <img src="images/create_map_form.png" style='width: 25em; height:auto'/>
</div>

Then the map generation process should be initialized. Sample editor window:

<div figure-id="fig:editor3" figure-caption="new map">
  <img src="images/create.png" style='width: 25em; height:auto'/>
</div>

## How to add an object to the map
 
You can add any object(s) from the left menu except the first two blocks, "Road tiles" and "Fill tiles", which describe the types of tiles.
For adding an object, you should double click the object in the left menu.
<div figure-id="fig:editor3" figure-caption="add object to map">
  <img src="images/add_obj.png" style='width: 25em; height:auto'/>
</div>

For editing attributes of an object you should do right click on the object and edit its attributes in the opened window. The window should look like:
<div figure-id="fig:editor4" figure-caption="change attribute of obj">
  <img src="images/edit_obj.png" style='width: 25em; height:auto'/>
</div>

For editing tiles, you should activate the brush mode (see Fig.5). After that, you should choose the type of tiles in the left menu. Then, one could select/brush the grids to apply the selected tile type. See Fig. 6 for the illustrated outcome.
<div figure-id="fig:editor5" figure-caption="brush button">
  <img src="images/brush.png" style='width: 25em; height:auto'/>
</div>

<div figure-id="fig:editor6" figure-caption="brush tiles">
  <img src="images/after_brush.png" style='width: 25em; height:auto'/>
</div>

## Select objects

For selecting objects you should click on them. See Fig. 7 for the illustrated outcome.

<div figure-id="fig:editor7" figure-caption="select objects">
  <img src="images/select_obj.png" style='width: 25em; height:auto'/>
</div>

## Rotate tiles and objects

For rotation you should select required tiles and objects and click the rotation button in the toolbar (see Fig. 8). See Fig. 9 for the illustrated outcome.

<div figure-id="fig:editor8" figure-caption="rotate tiles button">
  <img src="images/rotate.png" style='width: 25em; height:auto'/>
</div>

<div figure-id="fig:editor9" figure-caption="rotate tiles">
  <img src="images/after_rotate.png" style='width: 25em; height:auto'/>
</div>

## Delete tiles and objects

For deletion you should select required tiles and objects and click the delete button in the toolbar (see Fig. 10).

<div figure-id="fig:editor10" figure-caption="delete button">
  <img src="images/delete.png" style='width: 25em; height:auto'/>
</div>

## Copy tiles and objects

For copy you should select required tiles and objects and click the copy button in the toolbar (see Fig. 11).

<div figure-id="fig:editor11" figure-caption="copy button">
  <img src="images/copy.png" style='width: 25em; height:auto'/>
</div>

<div figure-id="fig:editor12" figure-caption="after copy">
  <img src="images/copy_obj.png" style='width: 25em; height:auto'/>
</div>

## Paste objects

For paste you should copy tiles and objects, click on tile on map and then click the paste button in the toolbar (see Fig. 13). See Fig. 14 for the illustrated outcome.

<div figure-id="fig:editor13" figure-caption="paste button">
  <img src="images/paste.png" style='width: 25em; height:auto'/>
</div>

<div figure-id="fig:editor14" figure-caption="after copy">
  <img src="images/paste_obj.png" style='width: 25em; height:auto'/>
</div>

## Cut objects

For cut you should select required tiles and objects and click the cut button in the toolbar (see Fig. 15). See Fig. 16 for the illustrated outcome. Tiles will replace on type *asphalt*,  objects will be deleted. Cutted tiles and objects will copy.

<div figure-id="fig:editor15" figure-caption="cut button">
  <img src="images/cut.png" style='width: 25em; height:auto'/>
</div>

<div figure-id="fig:editor16" figure-caption="after cut">
  <img src="images/cut_obj.png" style='width: 25em; height:auto'/>
</div>

## Save map to png

For save map to image you should click the save to png button in the toolbar (see Fig. 17). See Fig. 18 for the illustrated outcome.

<div figure-id="fig:editor17" figure-caption="png button">
  <img src="images/save_map_as_png.png" style='width: 25em; height:auto'/>
</div>

<div figure-id="fig:editor18" figure-caption="png image">
  <img src="images/after_save_to_png.png" style='width: 25em; height:auto'/>
</div>

## Save map

For the save map you should click the save button in the toolbar (see Fig. 19). If you want to select a folder to save the map you should click the save map as button in the toolbar (see Fig. 20) and select the folder on the filesystem which will save the map(see Fig. 21).

<div figure-id="fig:editor19" figure-caption="save button">
  <img src="images/save_map.png" style='width: 25em; height:auto'/>
</div>

<div figure-id="fig:editor20" figure-caption="save as button">
  <img src="images/save_map_as.png" style='width: 25em; height:auto'/>
</div>

<div figure-id="fig:editor21" figure-caption="fs on saving">
  <img src="images/save_map_filesystem.png" style='width: 25em; height:auto'/>
</div>

## Open map

For opening map you should click the open button in the toolbar (see Fig. 22) and select the folder on the filesystem which will open map (see Fig. 23).

<div figure-id="fig:editor22" figure-caption="open button">
  <img src="images/open_map.png" style='width: 25em; height:auto'/>
</div>

<div figure-id="fig:editor23" figure-caption="fs on open">
  <img src="images/open_map_filesystem.png" style='width: 25em; height:auto'/>
</div>

## Moving map

For moving map you should click the middle button on mouse and drag map (see Fig. 24). See Fig. 25 for the illustrated outcome.

<div figure-id="fig:editor24" figure-caption="before to the corner">
  <img src="images/cut_obj.png" style='width: 25em; height:auto'/>
</div>

<div figure-id="fig:editor25" figure-caption="after moving">
  <img src="images/move_map.png" style='width: 25em; height:auto'/>
</div>

 For move the map to the left high corner of the window you should click the corner button in the toolbar (see Fig. 26). See Fig. 27 for the illustrated outcome.

<div figure-id="fig:editor26" figure-caption="to the corner button">
  <img src="images/corner.png" style='width: 25em; height:auto'/>
</div>

<div figure-id="fig:editor27" figure-caption="after to the corner">
  <img src="images/after_to_the_corner.png" style='width: 25em; height:auto'/>
</div>


## Scale map

For the scale map on the window you should roll the ring on the mouse.

## Undo

For move through the history of changes, you need to click on the undo button (see Fig. 28) or the undo shift button (see Fig. 29).

<div figure-id="fig:editor28" figure-caption="undo button">
  <img src="images/undo.png" style='width: 25em; height:auto'/>
</div>

<div figure-id="fig:editor29" figure-caption="shift undo button">
  <img src="images/shift_undo.png" style='width: 25em; height:auto'/>
</div>

## Debug line

On the bottom of the editor you will see a debug line with Qt coordinates and map-translated coordinates (see Fig. 30).

<div figure-id="fig:editor30" figure-caption="debug line">
  <img src="images/debug_line.png" style='width: 25em; height:auto'/>
</div>

## Hotkeys

Exit: Ctrl+Q  
Create map: Ctrl+N  
Open map: Ctrl+O  
Save map: Ctrl+S  
Save map as: Ctrl+Alt+S  
Save to png: Ctrl+P  
Delete: Ctrl+D  
Undo: Ctrl+Z  
Shift undo: Ctrl+Shift+Z  
Rotate: Ctrl+R  
To the corner: Ctrl+M  
Copy: Ctrl+C  
Cut: Ctrl+X  
Paste: Ctrl+V  
Brush mode: Ctrl+B  


