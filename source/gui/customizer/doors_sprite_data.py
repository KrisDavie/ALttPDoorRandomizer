from pathlib import Path
from tkinter import Canvas, Toplevel, NW
from PIL import ImageTk, Image
from source.gui.customizer import worlds_data

ITEM_SHEET_PATH = Path("resources") / "app" / "gui" / "plandomizer" / "Doors_Sheet.png"

BORDER_SIZE = 20
TILE_BORDER_SIZE = 3


def show_sprites(self, top, parent_event):
    def select_sprite(parent, self, event):
        item = self.canvas.find_closest(event.x, event.y)
        print(item)
        if item not in [(x,) for x in self.items.values()]:
            return
        item_name = get_sprite_by_button(self, item)

        sprite_window.selected_item = item_name
        self.destroy()

    def get_sprite_by_button(self, button):
        for name, loc in self.items.items():
            if loc == button[0]:
                return name

    sprite_window = Toplevel(self)
    w = top.winfo_x()
    h = top.winfo_y()
    x = max(0, min(w + parent_event.x - 544, self.winfo_screenwidth() - 544))
    y = max(0, min(h + parent_event.y - 288, self.winfo_screenheight() - 288))
    sprite_window.geometry(f"{544 + (BORDER_SIZE * 2)}x{288 + (BORDER_SIZE * 2)}+{int(x)}+{int(y)}")
    sprite_window.title("Sprites Window")
    sprite_window.focus_set()
    sprite_window.grab_set()

    sprite_window.canvas = Canvas(
        sprite_window, width=544 + (BORDER_SIZE * 2), height=288 + (BORDER_SIZE * 2), background="black"
    )
    sprite_window.canvas.pack()
    sprite_window.spritesheet = ImageTk.PhotoImage(Image.open(ITEM_SHEET_PATH).resize((544, 288)))
    sprite_window.image = sprite_window.canvas.create_image(
        0 + BORDER_SIZE, 0 + BORDER_SIZE, anchor=NW, image=sprite_window.spritesheet
    )
    sprite_window.items = {}
    for item, coords in item_table.items():
        disabled = False

        y, x = coords
        item_selector = sprite_window.canvas.create_rectangle(
            x * 32 + BORDER_SIZE,
            y * 32 + BORDER_SIZE,
            x * 32 + 33 + BORDER_SIZE,
            y * 32 + 33 + BORDER_SIZE,
            outline="",
            fill="#888" if disabled else "",
            stipple="gray12" if disabled else "",
            state="disabled" if disabled else "normal",
        )
        sprite_window.items[item] = item_selector
        sprite_window.canvas.tag_bind(
            item_selector,
            "<Button-1>",
            lambda event: select_sprite(self, sprite_window, event),
        )
    sprite_window.wait_window(sprite_window)
    sprite_window.grab_release()
    return sprite_window.selected_item


item_table = {
    "Bomb Door": (0, 0),
    "Slash Door": (0, 1),
    "Dash Door": (0, 2),
    "Key Door": (0, 3),
    "Big Key Door": (0, 4),
    "Trap Door": (0, 5),
    "Lobby Door": (0, 6),
}
