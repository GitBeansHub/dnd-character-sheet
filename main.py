import imgui, glfw, OpenGL.GL, sys
import imgui.integrations.glfw

# Function to read a file
def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

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

# Initialize ImGui context and GLFW renderer
def init_imgui(window):
    imgui.create_context()
    impl = imgui.integrations.glfw.GlfwRenderer(window)
    return impl

window=init_window()
impl=init_imgui(window)
md_text = read_file("sheetroot/text.md")
min_left_w=0
min_nav_w=0
min_top_h=0
left_w=.2
nav_w=.1
top_h=.15

# Function to clear the screen
def clear_screen():
    OpenGL.GL.glClearColor(0.1, 0.1, 1.1, 1)
    OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT)

#text zone
def draw_tz(left_w, nav_w, top_h, w, h, md_text):
    width = w*(1 - left_w - nav_w)
    height = h*(1 - top_h)
    imgui.set_next_window_position(w-width, h-height)
    imgui.set_next_window_size(width, height)

    imgui.begin(
        "Text.md (raw)",
        False,
        imgui.WINDOW_NO_TITLE_BAR |
        imgui.WINDOW_NO_RESIZE |
        imgui.WINDOW_NO_MOVE |
        imgui.WINDOW_NO_COLLAPSE
    )

    imgui.begin_child("scroll", 0, 0, True)
    imgui.push_text_wrap_pos(0.0)
    imgui.text_unformatted(md_text)
    imgui.pop_text_wrap_pos()
    imgui.end_child()
    imgui.end()
    
#counter zone
def draw_cz(left_w, nav_w, top_h, w, h, md_text):
    width = w*left_w
    height=h
    imgui.set_next_window_position(0, 0)
    imgui.set_next_window_size(width, height)

    imgui.begin(
        "Counter Area (raw)",
        False,
        imgui.WINDOW_NO_TITLE_BAR |
        imgui.WINDOW_NO_RESIZE |
        imgui.WINDOW_NO_MOVE |
        imgui.WINDOW_NO_COLLAPSE
    )

    imgui.begin_child("scroll", 0, 0, True)
    imgui.push_text_wrap_pos(0.0)
    imgui.text_unformatted(md_text)
    imgui.pop_text_wrap_pos()
    imgui.end_child()
    imgui.end()
    
#top inventory selector
def draw_top(left_w, nav_w, top_h, w, h, md_text):
    width = w*(1-left_w)
    height=h*top_h
    imgui.set_next_window_position(w*left_w, 0)
    imgui.set_next_window_size(width, height)

    imgui.begin(
        "Top Inventory Selector (raw)",
        False,
        imgui.WINDOW_NO_TITLE_BAR |
        imgui.WINDOW_NO_RESIZE |
        imgui.WINDOW_NO_MOVE |
        imgui.WINDOW_NO_COLLAPSE
    )

    imgui.begin_child("scroll", 0, 0, True)
    imgui.push_text_wrap_pos(0.0)
    imgui.text_unformatted(md_text)
    imgui.pop_text_wrap_pos()
    imgui.end_child()
    imgui.end()
#side inventory selector
def draw_nav(left_w, nav_w, top_h, w, h, md_text):
    width = w*(nav_w)
    height=h*(1-top_h)
    imgui.set_next_window_position(w*left_w, h*top_h)
    imgui.set_next_window_size(width, height)

    imgui.begin(
        "Side Inventory Selector (raw)",
        False,
        imgui.WINDOW_NO_TITLE_BAR |
        imgui.WINDOW_NO_RESIZE |
        imgui.WINDOW_NO_MOVE |
        imgui.WINDOW_NO_COLLAPSE
    )

    imgui.begin_child("scroll", 0, 0, True)
    imgui.push_text_wrap_pos(0.0)
    imgui.text_unformatted(md_text)
    imgui.pop_text_wrap_pos()
    imgui.end_child()
    imgui.end()

# Function to draw the UI
def draw_ui(md_text):
    io = imgui.get_io()
    w = io.display_size.x
    h = io.display_size.y

    #pull TZ text
    draw_tz(left_w, nav_w, top_h, w, h, md_text)

    #pull CZ text
    draw_cz(left_w, nav_w, top_h, w, h, md_text)

    #pull top text
    draw_top(left_w, nav_w, top_h, w, h, md_text)

    #pull nav text
    draw_nav(left_w, nav_w, top_h, w, h, md_text)


# Frame function to handle rendering and input
def frame(window, impl):
    glfw.poll_events()
    impl.process_inputs()
    imgui.new_frame()
    clear_screen()
    draw_ui(md_text)
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