from tkinter import *
from handle_request import URL, lex

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18 # Horizonal Step, Vertical Step for text display
SCROLL_STEP = 100

def layout(text: str, width, height) -> list[str]:
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        if c == "\n":
            cursor_x = HSTEP
            cursor_y += VSTEP+5
        display_list.append((cursor_x, cursor_y, c))
        cursor_x += HSTEP
        if cursor_x >= width - HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
    return display_list
        
class Browser:
    def __init__(self):
        self.window = Tk()
        self.window.bind("<Down>", self.scroll_down)
        self.window.bind("<Up>", self.scroll_up)
        self.window.bind("<MouseWheel>", self.scroll_wheel)
        self.window.bind("<Configure>", self.reshape_window)
        self.scroll = 0
        self.canvas = Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT  
            )
        self.canvas.pack(fill=BOTH, expand=1)
    
    def reshape_window(self, e):
        width, height = e.width, e.height
        self.display_list = layout(self.text, width, height)
        self.draw()
        
    def scroll_wheel(self, e):
        if e.delta == 1:
            return self.scroll_up(e)
        return self.scroll_down(e)
    
    def scroll_down(self, e):
        self.scroll += SCROLL_STEP
        self.draw()
    
    def scroll_up(self, e):
        self.scroll -= SCROLL_STEP
        if self.scroll < 0:
            self.scroll = 0
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            # To speed-up scrolling
            # Don't render texts that are off screen
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue

            self.canvas.create_text(x, y-self.scroll, text=c)

    def load(self, url):
        body = url.request()
        self.text = lex(body)
        self.display_list = layout(self.text, WIDTH, HEIGHT)
        self.draw()


if __name__ == "__main__":
    import sys
    from handle_request import URL
    Browser().load(URL(sys.argv[1]))
    mainloop()