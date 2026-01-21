# src/drag_logic.py

class DragManager:
    """Provides drag-and-drop functionality for the Library Game."""
    
    def start_drag(self, event):
        self.dragging = True
    
    @staticmethod
    def rect_overlap(rect1, rect2):
        return not (rect1[2] < rect2[0] or 
                    rect1[0] > rect2[2] or 
                    rect1[3] < rect2[1] or 
                    rect1[1] > rect2[3])

    def on_drag(self, event):
        if not hasattr(self, 'dragging') or not self.dragging:
            return
        
        bbox = self.main_canvas.bbox("draggable")
        if not bbox: return
        
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2
        dx, dy = event.x - center_x, event.y - center_y
        self.main_canvas.move("draggable", dx, dy)
        
        for slot_idx, slot_rect, _ in self.slot_areas:
            coords = self.main_canvas.coords(slot_rect)
            if coords and self.rect_overlap(bbox, coords):
                self.on_slot_hover(slot_idx)
                return
        self.on_slot_leave()
    
    def end_drag(self, event):
        self.dragging = False
        bbox = self.main_canvas.bbox("draggable")
        if not bbox:
            self.main_canvas.delete("draggable")
            self.draw_book_to_place()
            self.on_slot_leave()
            return

        for slot_idx, slot_rect, _ in self.slot_areas:
            coords = self.main_canvas.coords(slot_rect)
            if coords and self.rect_overlap(bbox, coords):
                self.selected_slot = slot_idx
                self.check_answer()
                return
        
        self.main_canvas.delete("draggable")
        self.draw_book_to_place()
        self.on_slot_leave()
    
    def on_slot_hover(self, slot_idx):
        if not self.dragging: return
        if self.hovered_slot == slot_idx: return
        self.hovered_slot = slot_idx
        gap_size = self.drag_book_info.get('width', 268)

        for book in self.book_labels:
            if book['index'] >= slot_idx:
                book['current_x'] = book['original_x'] + gap_size
            else:
                book['current_x'] = book['original_x']
            self.redraw_book(book)
    
    def on_slot_leave(self):
        if self.selected_slot is not None: return
        self.hovered_slot = None
        for book in self.book_labels:
            book['current_x'] = book['original_x']
            self.redraw_book(book)
    
    def redraw_book(self, book):
        self.main_canvas.delete(f"book_{book['index']}")
        self.draw_book_spine(book['index'], book['current_x'], book['y'],
                            book['width'], book['height'], book['color'],
                            book['title'], book['author'], book['font_size'])