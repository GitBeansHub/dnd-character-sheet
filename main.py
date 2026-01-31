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

# Function to clear the screen
def clear_screen():
    OpenGL.GL.glClearColor(0.1, 0.1, 1.1, 1)
    OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT)

# Function to draw the UI
def draw_ui(md_text):
    imgui.begin("Text.md (raw)")
    imgui.begin_child("scroll", 0, 0, True)
    imgui.push_text_wrap_pos(0.0)
    imgui.text_unformatted(md_text)
    imgui.pop_text_wrap_pos()
    imgui.end_child()
    imgui.end()


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