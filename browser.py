from tkinter import *
from handle_request import URL, lex

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18 # Horizonal Step, Vertical Step for text display
SCROLL_STEP = 100

def layout(text: str) -> list[str]:
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        display_list.append((cursor_x, cursor_y, c))
        cursor_x += HSTEP
        if cursor_x >= WIDTH - HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
    return display_list
        
class Browser:
    def __init__(self):
        self.window = Tk()
        self.window.bind("<Down>", self.scroll_down)
        self.window.bind("<Up>", self.scroll_up)
        self.scroll = 0
        self.canvas = Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT  
            )
        self.canvas.pack()

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
        text = lex(body)
        self.display_list = layout(text)
        self.draw()


if __name__ == "__main__":
    import sys
    from handle_request import URL
    Browser().load(URL(sys.argv[1]))
    mainloop()