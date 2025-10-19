from ursina import *
from ursina.prefabs.input_field import InputField

class NumberInputField(InputField):
    def __init__(self, **kwargs):
        super().__init__(limit_content_to='0123456789.-',**kwargs)
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
        
        # Position labels and input fields
        y_offset = 0.25
        spacing = 0.08
        
        # X Position
        Text("X:", parent=self, position=(-0.4, y_offset, -0.1), scale=(1/0.3, 1), color=color.white, origin=(-0.5, 0.1))
        self.x_input = NumberInputField(
            default_value='0',
            parent=self,
            position=(-0.05, y_offset, -0.1),
            scale=(0.5, 0.05, 1),
            max_lines=1,
            scroll_callback=self.apply_changes
        )
        
        # Y Position
        y_offset -= spacing
        Text("Y:", parent=self, position=(-0.4, y_offset, -0.1), scale=(1/0.3, 1), color=color.white, origin=(-0.5, 0.1))
        self.y_input = NumberInputField(
            default_value='0',
            parent=self,
            position=(-0.05, y_offset, -0.1),
            scale=(0.5, 0.05, 1),
            max_lines=1,
            scroll_callback=self.apply_changes
        )
        
        # Z Position
        y_offset -= spacing
        Text("Z:", parent=self, position=(-0.4, y_offset, -0.1), scale=(1/0.3, 1), color=color.white, origin=(-0.5, 0.1))
        self.z_input = NumberInputField(
            default_value='0',
            parent=self,
            position=(-0.05, y_offset, -0.1),
            scale=(0.5, 0.05, 1),
            max_lines=1,
            scroll_callback=self.apply_changes
        )

        self.inputs = [self.x_input, self.y_input, self.z_input]
        
        # Apply button
        self.apply_button = Button(
            text='Apply',
            parent=self,
            position=(-0.08, y_offset - 0.1, -0.1),
            scale=Vec3(1/0.3, 0.6, 1) * 0.1,
            color=color.blue,
            on_click=self.apply_changes
        )
        
        # Set up TAB navigation chain
        self.x_input.next_field = self.y_input
        self.y_input.next_field = self.z_input
        self.z_input.next_field = self.x_input  # Loop back to first
    
    def show_for_entity(self, entity):
        """Show editor for a specific entity"""
        self.target_entity = entity
        if entity:
            # Update input fields with entity's current position
            self.x_input.text = str(round(entity.x, 3))
            self.y_input.text = str(round(entity.y, 3))
            self.z_input.text = str(round(entity.z, 3))
            self.title.text = f"Editing: {entity.name}"
        else:
            # Reset to defaults when no entity
            self.x_input.text = '0'
            self.y_input.text = '0' 
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
            x_val = float(self.x_input.text) if self.x_input.text else 0
            y_val = float(self.y_input.text) if self.y_input.text else 0
            z_val = float(self.z_input.text) if self.z_input.text else 0
            
            # Apply to entity
            self.target_entity.position = Vec3(x_val, y_val, z_val)
            
            print(f"Applied position ({x_val}, {y_val}, {z_val}) to {self.target_entity.name}")
            
        except ValueError:
            print("Invalid input values. Please enter numbers only.")
    
    def update(self):
        if any([x.active for x in self.inputs]) and held_keys['enter']:
            self.apply_changes()