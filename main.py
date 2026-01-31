import imgui, glfw, OpenGL.GL, sys
import imgui.integrations.glfw
glfwWorked=(glfw.init())
if not glfwWorked:
    print("Failed to initialize GLFW")
    sys.exit(1)
print("GLFW initialized")
window=glfw.create_window(800,600,"imgui-glfw-opengl3 example",None,None)
print("Creating window...")

# Check if window creation was successful
if not window:
    glfw.terminate()
    print("Failed to create GLFW window")
    sys.exit(1)


# Make the OpenGL context current
glfw.make_context_current(window)
glfw.swap_interval(1) # Enable vsync
imgui.create_context()
impl=imgui.integrations.glfw.GlfwRenderer(window)
print("Window created")

# Main loop
while not glfw.window_should_close(window):
    glfw.poll_events() #have window respond to inputs
    OpenGL.GL.glClearColor(1.1,.1,1.1,1) #pick color to clear screen to
    OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT) #clear screen
    #add hello world to screen

    #Needs keepalive code to keep window open
    glfw.swap_buffers(window) #update window with cleared color

# Cleanup and exit
glfw.terminate()
print("GLFW terminated")