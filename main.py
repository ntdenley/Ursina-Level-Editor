from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# Custom free camera
from freecam import FreeCam
from selector import Selector
from editor import EditorWindow

app = Ursina()

# simple scene to move around in
#ground = Entity(model='plane', scale=100, texture='white_cube', texture_scale=(100, 100), color=color.light_gray)
for x in range(-5, 6, 2):
    for z in range(-5, 6, 2):
        if x == 0 and z == 0:
            continue
        # Generate random color for each cube
        random_color = color.rgb(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        e = Entity(model='cube', color=random_color, scale=1.5, position=(x, 0.75, z), collider='box', render_queue=0)
        e.selectable = True  # Mark entity as selectable

# Add a teapot entity (using sphere as placeholder since Ursina doesn't have built-in teapot)
teapot = Entity(
    model='teapot.obj', 
    color=color.gold, 
    scale=1,
    origin_y=1,
    position=(0, 10, 0), 
    collider='teapot.obj',
    render_queue=0
)
teapot.selectable = True  # Mark teapot as selectable

selected_objects = []

# hook Ursina update/input to the camera
freecam = FreeCam()
selector = Selector()
selector.select_callback = lambda entity: editor_window.show_for_entity(entity)
editor_window = EditorWindow()

def update():
    selected_objects = [selector.selected_entity]



# helpful on-screen hint
Text(
    "Hold Right-Click: camera control  WASD: move  Space/Ctrl: up/down  Shift: speed  Scroll: FOV  Esc: release mouse",
    parent=camera.ui,
    position =(-0.85, 0.45),
    background=True, 
    scale=0.6)

Sky(color=color.azure)

app.run()