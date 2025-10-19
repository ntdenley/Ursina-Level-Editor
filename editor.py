from ursina import *
from ursina.prefabs.input_field import InputField

class NumberInputField(InputField):
    def __init__(self, **kwargs):
        super().__init__(
            limit_content_to='0123456789.-', 
            default_value="0.0",
            scale=Vec3(0.5, 0.05, 1) * 0.4, 
            **kwargs)
        self.text_field.scale *= 0.4
        self.dragging = False
        self.scroll_callback = kwargs.get('scroll_callback', None)
    
    def input(self, key):
        if key == "left mouse down" and self.hovered:
            self.dragging = True
            self.start_x = mouse.x
            self.start_value = float(self.text) if self.text else 0
        if key == "left mouse up":
            self.dragging = False
    
    def update(self):
        if self.dragging:
            delta_x = mouse.x - self.start_x
            sensitivity = 10  # Adjust sensitivity as needed
            new_value = self.start_value + delta_x * sensitivity
            self.text = str(round(new_value, 3))

            if(mouse.x >= 1.1):
                mouse.x = -1.1  # Wrap around to the left side
                self.start_x = -mouse.x
                self.start_value = float(self.text)
            elif(mouse.x <= -1.1):
                mouse.x = 1.1  # Wrap around to the right side
                self.start_x = -mouse.x
                self.start_value = float(self.text)

            if self.scroll_callback:
                self.scroll_callback()

class EditorWindow(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='cube',
            color=color.dark_gray,
            scale=(0.3, 1, 1),
            position=(0.7, 0, -1),
            alpha=0.8
        )
        
        self.visible = False
        self.target_entity = None
        self.pos_inputs = [None]*3
        self.rot_inputs = [None]*3
        self.scale_inputs = [None]*3

        # Create UI elements
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        self.title = Text(
            "Editor",
            parent=self,
            position=(-0.12, 0.4, -0.1),
            scale=(1/0.3, 1),
            color=color.white
        )

        y_offset = 0.3
        y_spacing = 0.1
        
        # Position labels and input fields
        x_offset = 0.3
        x_spacing = 0.3

        previous_input = None
        labels = ['X', 'Y', 'Z']
        colors = [color.red, color.green, color.blue]

        Text("Position:", parent=self, position=(0, y_offset, -0.1), scale=Vec2(1/0.3, 1) * 0.8, color=color.white, origin=(0, -1.1))

        # Labels and input fields
        for i in range(2, -1, -1):  
            # Position
            pos = NumberInputField(
                parent=self,
                position=(x_offset, y_offset, -0.1),
                max_lines=1,
                scroll_callback=self.apply_changes,
                next_field=previous_input,
            )
            Text(f"{labels[i]}:", parent=pos, position=(-(pos.scale.x/self.scale.x), 0, 0), scale=(Vec3(0.5)/pos.scale)/self.scale, color=colors[i], origin=(0.5, 0))
            x_offset -= x_spacing
            previous_input = pos
            self.pos_inputs[i] = pos

        y_offset -= y_spacing
        x_offset = 0.3

        Text("Rotation:", parent=self, position=(0, y_offset, -0.1), scale=Vec2(1/0.3, 1) * 0.8, color=color.white, origin=(0, -1.1))

        # Labels and input fields
        for i in range(2, -1, -1):  
            # Position
            rot = NumberInputField(
                parent=self,
                position=(x_offset, y_offset, -0.1),
                max_lines=1,
                scroll_callback=self.apply_changes,
                next_field=previous_input,
            )
            Text(f"{labels[i]}:", parent=rot, position=(-(rot.scale.x/self.scale.x), 0, 0), scale=(Vec3(0.5)/rot.scale)/self.scale, color=colors[i], origin=(0.5, 0))
            x_offset -= x_spacing
            previous_input = rot
            self.rot_inputs[i] = rot

        y_offset -= y_spacing
        x_offset = 0.3

        Text("Scale:", parent=self, position=(0, y_offset, -0.1), scale=Vec2(1/0.3, 1) * 0.8, color=color.white, origin=(0, -1.1))

        # Labels and input fields
        for i in range(2, -1, -1):  
            # Position
            scale = NumberInputField(
                parent=self,
                position=(x_offset, y_offset, -0.1),
                max_lines=1,
                scroll_callback=self.apply_changes,
                next_field=previous_input,
            )
            Text(f"{labels[i]}:", parent=scale, position=(-(scale.scale.x/self.scale.x), 0, 0), scale=(Vec3(0.5)/scale.scale)/self.scale, color=colors[i], origin=(0.5, 0))
            x_offset -= x_spacing
            previous_input = scale
            self.scale_inputs[i] = scale

    def show_for_entity(self, entity):
        """Show editor for a specific entity"""
        self.target_entity = entity
        if entity:
            # Update input fields with entity's current position
            for i in range(3):
                self.pos_inputs[i].text = str(round(entity.position[i], 3))
                self.rot_inputs[i].text = str(round(entity.rotation[i], 3))
                self.scale_inputs[i].text = str(round(entity.scale[i], 3))
            self.title.text = f"Editing: {entity.name}"
        else:
            # Reset to defaults when no entity
            for i in range(3):
                self.pos_inputs[i].text = '0'
            self.z_input.text = '0'
            self.title.text = "Editor"
        
        self.visible = True
    
    def hide(self):
        """Hide the editor window"""
        self.visible = False
        self.target_entity = None
    
    def apply_changes(self):
        """Apply the changes from input fields to the target entity"""
        if not self.target_entity:
            return
            
        try:
            # Parse input values
            x_val, y_val, z_val = [float(self.pos_inputs[i].text) for i in range(3)]
            rx_val, ry_val, rz_val = [float(self.rot_inputs[i].text) for i in range(3)]
            sx_val, sy_val, sz_val = [float(self.scale_inputs[i].text) for i in range(3)]

            # Apply to entity
            self.target_entity.position = Vec3(x_val, y_val, z_val)
            self.target_entity.rotation = Vec3(rx_val, ry_val, rz_val)
            self.target_entity.scale = Vec3(sx_val, sy_val, sz_val)

        except ValueError:
            print("Invalid input values. Please enter numbers only.")