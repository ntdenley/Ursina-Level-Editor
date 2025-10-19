from ursina import Entity, mouse, camera, Vec3, clamp, held_keys, time

# Free camera implementation
class FreeCam(Entity):
    def __init__(self, position=(0, 2, -10), speed=10, sensitivity=40):
        super().__init__()
        self.position = Vec3(position)
        self.speed = speed
        self.sensitivity = sensitivity
        self.yaw = 0.0
        self.pitch = 0.0
        self.fov = 90  # Default field of view
        self.stored_mouse_pos = None  # Store mouse position when right-click starts
        mouse.locked = False  # Start with mouse unlocked
        camera.position = self.position
        camera.rotation = (0, 0, 0)
        camera.fov = self.fov

    def update(self):
        # Only allow camera control when right mouse button is held
        if held_keys['right mouse']:
            # mouse look
            self.yaw += mouse.velocity.x * self.sensitivity
            self.pitch -= mouse.velocity.y * self.sensitivity
            self.pitch = clamp(self.pitch, -89, 89)
            if mouse.velocity != Vec3(0,0,0):         
                camera.rotation = (self.pitch, self.yaw, 0)

            # movement input
            forward = held_keys['w'] - held_keys['s']
            right = held_keys['d'] - held_keys['a']
            up = held_keys['space'] - held_keys['left control']

            move_dir = (camera.forward * forward) + (camera.right * right) + (Vec3(0,1,0) * up)
            if move_dir != Vec3(0,0,0):
                move_dir = move_dir.normalized()

            cur_speed = self.speed * (3 if held_keys['shift'] else 1)
            self.position += move_dir * cur_speed * time.dt
            camera.position = self.position

    def input(self, key):
        # toggle mouse capture when right mouse is pressed/released
        if key == 'right mouse down':
            self.stored_mouse_pos = (mouse.x, mouse.y)  # Store current mouse position
            mouse.locked = True
            mouse.position = (0,0)  # Center mouse to prevent jump
        if key == 'right mouse up':
            mouse.locked = False
            if self.stored_mouse_pos:
                # Restore mouse to original position
                mouse.position = self.stored_mouse_pos
                self.stored_mouse_pos = None
        if key == 'escape':
            mouse.locked = False
            if self.stored_mouse_pos:
                # Restore mouse to original position
                mouse.position = self.stored_mouse_pos
                self.stored_mouse_pos = None
        
        # FOV control with scroll wheel when holding right click
        if held_keys['right mouse']:
            if key == 'scroll up':
                self.fov = max(10, self.fov - 1)  # Minimum FOV of 10
                camera.fov = self.fov
            elif key == 'scroll down':
                self.fov = min(150, self.fov + 1)  # Maximum FOV of 150
                camera.fov = self.fov