# 2D-Grid-Raycaster
https://user-images.githubusercontent.com/69489271/174675018-d1cc91a9-eeb4-4bd0-9520-fa83ce8cfeb5.mp4

Will write more ... soon.
## Game Settings
Game runtime settings can be changing by modifying src/constants.py. A list of setting anems and descriptions are written below.

| Name | Description |
|----- | ----------- |
| SIZE										| Controls resolution of game window. |
| FPS											| Controls max FPS of game. |
| STEP										| Controls base rendering quality for all textures. Larger results in worse rendering quality. |
| SLOW										| A visual setting to visualize the rendering process. |
| RANDOM									| Controls if map should be ranomly generated. |
| EMPTY_CHANCE						| Controls ratio of empty tiles to filled tiles of randomly generated map. |
| DIM											| Controls size of randomly generated map. |
| INT_TO_COLOR						| Maps grid element value to color. |
| INT_TO_INDEX						| Maps grid element value to texture. |
| FLOOR										| Controls color of floor. |
| CEILING									| Controls color of ceiling. |
| STEPSIZE								| Controls speed of camera movement. |
| DEG_STEP								| Controls speed of camera turning. |
| SCALE										| Controls scale of the minimap. |
| TEX_WIDTH, TEX_HEIGHT 	| Controls the dimensions of the textures provided. Textures should be square. |
| INTERVAL 								| Controls the quality of textures as a function of distance. |

## Reading
1. [Super Fast Ray Casting in Tiled Worlds using DDA](https://www.youtube.com/watch?v=NbSee-XM7WA)
2. [Lode's Computer Graphics Tutorial](https://lodev.org/cgtutor/raycasting.html#The_Basic_Idea_)
3. [Rendering Raycasting](https://www.youtube.com/watch?v=Vij_obgv9h4)
