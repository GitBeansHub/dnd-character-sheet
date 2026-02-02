import imgui, glfw, OpenGL.GL, sys, os
import imgui.integrations.glfw
from dataclasses import dataclass, field

# Default Variables
left_w = 0.2
nav_w = 0.25
top_h = 0.1
sheetroot = "sheetroot"
fonts = None
top_text_size = 0.1 # Top Text Size (as fraction of height)
top_padding_size = 0.2 # Top Padding Size (as fraction of height)
TZ_text_size = 12 # TZ Text Size (Raw Text Size)
nav_text_size = 0.05 # Nav Text Size (as fraction of width)
nav_padding_size = 0.02 # Nav Padding Size (as fraction of width)
CZ_text_size = 0.09 # CZ Text Size (as fraction of width)
CZ_padding_size = 0.02 # CZ Padding Size (as fraction of width)

# Function to read a file
def read_file(path):
    with open(path, "a+", encoding="utf-8") as f:
        f.seek(0)  # move pointer to beginning
        return f.read()
# Node dataclass
@dataclass
class Node:
    name_disk: str
    path: str
    content: str
    parent: "Node | None" = None
    children: list["Node"] = field(default_factory=list)

    @property
    def name_ui(self) -> str:
        return self.name_disk[0:]  # hides the prefix character
# Function to create a directory tree
def make_dir_tree(base_path, parent=None):
    node = Node(
        name_disk=os.path.basename(base_path),
        path=base_path,
        content=read_file(os.path.join(base_path, "text.md")),
        parent=parent,
    )

    for name in os.listdir(base_path):
        full_path = os.path.join(base_path, name)
        if os.path.isdir(full_path):
            child = make_dir_tree(full_path, parent=node)
            node.children.append(child)

    return node
# Initialize GLFW and create a window
def init_window():
    if not glfw.init():
        print("Failed to initialize GLFW")
        sys.exit(1)

    window = glfw.create_window(800, 600, "DND Sheet", None, None)
    if not window:
        glfw.terminate()
        print("Failed to create GLFW window")
        sys.exit(1)

    glfw.make_context_current(window)
    glfw.swap_interval(1)
    return window
def init_imgui(window):
    imgui.create_context()
    global fonts
    io = imgui.get_io()
    fonts = [
        io.fonts.add_font_from_file_ttf("C:/Windows/Fonts/segoeui.ttf", s)
        for s in range(2, 83, 2)
    ]

    impl = imgui.integrations.glfw.GlfwRenderer(window)
    impl.refresh_font_texture()
    return impl

# Setup basic variables
window = init_window()
impl = init_imgui(window)
tree = make_dir_tree(sheetroot)  
# Bandaid to read files for CZ and TZ
cz_text = read_file("sheetroot/counters.csv")
nav_selected: "Node | None" = None
text_selected: "str | None" = read_file("sheetroot/text.md")
# Font size
def set_font_size(size):
    size = max(0, min(40, int(size)))
    if fonts:
        imgui.push_font(fonts[size])
def pop_font():
    if fonts:
        imgui.pop_font()
# Draw functions for different UI sections
def draw_tz(left_w, nav_w, top_h, w, h):
    global text_selected
    width = w * (1 - left_w - nav_w)
    height = h * (1 - top_h)
    imgui.set_next_window_position(w - width, h - height)
    imgui.set_next_window_size(width, height)

    imgui.begin(
        "Text.md (raw)",
        False,
        imgui.WINDOW_NO_TITLE_BAR
        | imgui.WINDOW_NO_RESIZE
        | imgui.WINDOW_NO_MOVE
        | imgui.WINDOW_NO_COLLAPSE,
    )
    set_font_size(TZ_text_size)
    imgui.begin_child("scroll", 0, 0, True)
    imgui.push_text_wrap_pos(0.0)
    imgui.text_unformatted(text_selected)
    imgui.pop_text_wrap_pos()
    imgui.end_child()
    pop_font()
    imgui.end()
def draw_cz(left_w, nav_w, top_h, w, h, content):
    width = w * left_w
    height = h
    imgui.set_next_window_position(0, 0)
    imgui.set_next_window_size(width, height)

    imgui.begin(
        "Counter Area (raw)",
        False,
        imgui.WINDOW_NO_TITLE_BAR
        | imgui.WINDOW_NO_RESIZE
        | imgui.WINDOW_NO_MOVE
        | imgui.WINDOW_NO_COLLAPSE,
    )

    imgui.begin_child("scroll", 0, 0, True)
    imgui.push_text_wrap_pos(0.0)
    imgui.text_unformatted(content)
    imgui.pop_text_wrap_pos()
    imgui.end_child()
    imgui.end()
def draw_top(left_w, nav_w, top_h, w, h):
    global nav_selected
    global text_selected
    width = w * (1 - left_w)
    height = h * top_h
    imgui.set_next_window_position(w * left_w, 0)
    imgui.set_next_window_size(width, height)
    imgui.begin(
        "Top",
        False,
        imgui.WINDOW_NO_TITLE_BAR
        | imgui.WINDOW_NO_RESIZE
        | imgui.WINDOW_NO_MOVE
        | imgui.WINDOW_NO_COLLAPSE
        | imgui.WINDOW_ALWAYS_HORIZONTAL_SCROLLBAR,
    )
    io = imgui.get_io()
    if imgui.is_window_hovered() and io.mouse_wheel != 0.0:
        imgui.set_scroll_x(imgui.get_scroll_x() - io.mouse_wheel * 30.0)

    set_font_size(height * top_text_size)  # Set font size based on window height
    imgui.push_style_var(imgui.STYLE_FRAME_PADDING, (12, height * top_padding_size))
    for i, child in enumerate(tree.children):
        if i > 0:
            imgui.same_line()
        if imgui.button(f"{child.name_ui}##top_{child.name_disk}"):
            print("clicked top:", child.path)
            nav_selected = child
            text_selected = child.content
            print(nav_selected.name_disk)
    pop_font()
    imgui.pop_style_var()

    imgui.end()
def draw_nav(left_w, nav_w, top_h, w, h):
    global nav_selected
    global text_selected
    width = w * (nav_w)
    height = h * (1 - top_h)
    imgui.set_next_window_position(w * left_w, h * top_h)
    imgui.set_next_window_size(width, height)
    
    imgui.begin(
        "Side Inventory Selector (raw)",
        False,
        imgui.WINDOW_NO_TITLE_BAR
        | imgui.WINDOW_NO_RESIZE
        | imgui.WINDOW_NO_MOVE
        | imgui.WINDOW_NO_COLLAPSE,
    )
    set_font_size(nav_text_size * width)  # Set font size based on window width
    imgui.begin_child("scroll", 0, 0, True)
    for i, child in enumerate(nav_selected.children if nav_selected else []):
        if imgui.button(f"O##open{i}"):
            print("clicked nav open:", child.path)
            nav_selected = child
        imgui.same_line()
        if imgui.button(f"{child.name_ui}##{child.name_disk}"): #navigate deeper
            print("clicked nav:", child.path)
            text_selected = child.content
        imgui.separator()
    if nav_selected and nav_selected.parent:
        if imgui.button("Back"):
            nav_selected = nav_selected.parent
            print("navigated back to:", nav_selected.path)
            if nav_selected.parent is None:
                nav_selected = None
    imgui.end_child()
    pop_font()
    imgui.end()
def clear_screen():
    OpenGL.GL.glClearColor(0.1, 0.1, 1.1, 1)
    OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT)
def draw_ui():
    io = imgui.get_io()
    w = io.display_size.x
    h = io.display_size.y

    # pull TZ text
    draw_tz(left_w, nav_w, top_h, w, h)

    # pull CZ text
    draw_cz(left_w, nav_w, top_h, w, h, cz_text)

    # pull top text
    draw_top(left_w, nav_w, top_h, w, h)

    # pull nav text
    draw_nav(left_w, nav_w, top_h, w, h)
# Frame function to handle rendering and input
def frame(window, impl):
    glfw.poll_events()
    impl.process_inputs()
    imgui.new_frame()
    clear_screen()
    draw_ui()
    imgui.render()
    impl.render(imgui.get_draw_data())
    glfw.swap_buffers(window)

# Run the application
while not glfw.window_should_close(window):
    frame(window, impl)

# Cleanup and exit
impl.shutdown()
glfw.terminate()
print("GLFW terminated")
