# src/drag_logic.py

class DragManager:
    """Provides drag-and-drop functionality for the Library Game."""
    
    def __init__(self, game_instance):
        """
        Initialize DragManager with reference to the game instance.
        
        Args:
            game_instance: The LibraryGame instance that owns this manager
        """
        self.game = game_instance
        self.dragging = False
    
    def start_drag(self, event):
        self.dragging = True
    
    @staticmethod
    def rect_overlap(rect1, rect2):
        """Check if two rectangles overlap."""
        return not (rect1[2] < rect2[0] or 
                    rect1[0] > rect2[2] or 
                    rect1[3] < rect2[1] or 
                    rect1[1] > rect2[3])

    def on_drag(self, event):
        if not self.dragging:
            print("Not dragging")
            return
        
        bbox = self.game.main_canvas.bbox("draggable")
        print(f"Dragging - bbox: {bbox}")
        if not bbox:
            return
        
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2
        dx, dy = event.x - center_x, event.y - center_y
        self.game.main_canvas.move("draggable", dx, dy)
        
        for slot_idx, slot_rect, _ in self.game.slot_areas:
            coords = self.game.main_canvas.coords(slot_rect)
            if coords and self.rect_overlap(bbox, coords):
                self.on_slot_hover(slot_idx)
                return
        self.on_slot_leave()
    
    def end_drag(self, event):
        self.dragging = False
        
        bbox = self.game.main_canvas.bbox("draggable")
        if not bbox:
            self.game.main_canvas.delete("draggable")
            self.game.draw_book_to_place()
            self.on_slot_leave()
            return

        for slot_idx, slot_rect, _ in self.game.slot_areas:
            coords = self.game.main_canvas.coords(slot_rect)
            if coords and self.rect_overlap(bbox, coords):
                self.game.selected_slot = slot_idx
                self.game.check_answer()
                return
        
        self.game.main_canvas.delete("draggable")
        self.game.draw_book_to_place()
        self.on_slot_leave()
    
    def on_slot_hover(self, slot_idx):
        if not self.dragging:
            return
        if self.game.hovered_slot == slot_idx:
            return
        self.game.hovered_slot = slot_idx
        
        gap_size = self.game.drag_book_info.get('width', 268)

        for book in self.game.book_labels:
            if book['index'] >= slot_idx:
                book['current_x'] = book['original_x'] + gap_size
            else:
                book['current_x'] = book['original_x']
            self.redraw_book(book)
    
    def on_slot_leave(self):
        if self.game.selected_slot is not None:
            return
        self.game.hovered_slot = None
        for book in self.game.book_labels:
            book['current_x'] = book['original_x']
            self.redraw_book(book)
    
    def redraw_book(self, book):
        self.game.main_canvas.delete(f"book_{book['index']}")
        self.game.draw_book_spine(
            book['index'], book['current_x'], book['y'],
            book['width'], book['height'], book['color'],
            book['title'], book['author'], book['font_size']
        )