import copy
from ursina import Entity, mouse, color, Text, destroy

class Selector(Entity):
    def __init__(self):
        super().__init__()
        self.hovered_entity = None
        self.highlight_border = None  # Solid border entity

        self.selected_entity = None
        self.selection_border = None  # Border for selected entity

        self.select_callback = None  # Function to call on selection change

    def update(self):
        # Only handle highlighting when mouse is unlocked
        if not mouse.locked:
            self.handle_hover()

    def input(self, key):
        if key == "right mouse down":
            self.clear_highlight()
        if key == "left mouse down":
            if self.hovered_entity:
                if self.hovered_entity != self.selected_entity:
                    self.select_callback and self.select_callback(self.hovered_entity)
                    # if something is already selected, remove its highlight
                    if self.selection_border:
                        destroy(self.selection_border)

                    # highlight the newly selected entity
                    self.selected_entity = self.hovered_entity
                    self.selection_border = self.highlight_border
                    self.selection_border.color = color.rgba(255, 255, 0, 255)  # Change to yellow for selection
                    self.highlight_border = None  # Clear hover highlight after selection
                
    
    def handle_hover(self):
        # Get the entity under the mouse cursor
        entity_under_mouse = mouse.hovered_entity
        
        # If we're hovering over a different entity
        if entity_under_mouse != self.hovered_entity:
            # Remove previous highlight
            self.clear_highlight()
            
            # Highlight new entity
            if entity_under_mouse and hasattr(entity_under_mouse, 'model'):
                # Skip UI elements and entities we don't want to highlight
                if not isinstance(entity_under_mouse, Text) and self.should_highlight(entity_under_mouse):
                    self.create_border_highlight(entity_under_mouse)
                    self.hovered_entity = entity_under_mouse
                else:
                    self.hovered_entity = None
            else:
                self.hovered_entity = None
    
    def create_border_highlight(self, entity):
        # Create a wireframe border around the entity
        if entity.model:

            # Solid wireframe border that renders on top
            self.highlight_border = Entity(
                parent=entity,
                model=copy.deepcopy(entity.model),
                color=color.rgba(255, 255, 255, 255),
                mode='wireframe',
                unlit=True,
                scale=1.05,
                origin=entity.origin,
                render_queue=-3,  # Render on top of everything
            )

            # Create a transparent mask that matches the entity exactly
            self.highlight_mask =Entity(
                parent=self.highlight_border,
                model=copy.deepcopy(entity.model),
                color=entity.color,  # Fully transparent
                mode='wireframe',
                unlit=True,
                scale = 1/1.05,
                origin=entity.origin,
                render_queue=-2,  # Render on top of everything
                always_on_top=True
            )

    def create_selection_highlight(self, entity):
        # Create a wireframe border around the selected entity
        self.selected_entity = entity
        if entity.model:

            # Solid wireframe border that renders on top
            self.selection_border = Entity(
                model=copy.deepcopy(entity.model),
                color=color.rgba(255, 255, 0, 255),  # Yellow for selection
                position=entity.position,
                rotation=entity.rotation,
                scale=entity.scale * 1.05,
                mode='wireframe',
                unlit=True,
                render_queue=-1,  # Render on top of everything
                always_on_top=True
            )
    
    def should_highlight(self, entity):
        # Add logic here to determine which entities should be highlighted
        # For now, highlight everything except specific types
        return hasattr(entity, 'selectable') and entity.selectable == True
    
    def clear_highlight(self):
        # Clear any current highlighting
        if self.highlight_border:
            destroy(self.highlight_border)
            self.highlight_border = None
        # Don't modify entity render properties - just clear the reference
        self.hovered_entity = None
