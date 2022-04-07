import sys

import imgui
import glfw
from imgui.integrations.glfw import GlfwRenderer
import OpenGL.GL as gl

def start_window(width: int, height: int,
                 window_name: str, render_function):
    """
    width: window width
    height: window height
    render_function:  
    """
    imgui.create_context()
    window = impl_glfw_init(width, height, window_name)
    impl = GlfwRenderer(window)

    while not glfw.window_should_close(window):
        render_frame(impl, window, render_function)

    impl.shutdown()
    glfw.terminate()
    

def render_frame(impl, window, render_function):
    """
    impl: GlfwRenderer
    window: GLFWwindow object
    frame_commands: function
    """
    glfw.poll_events()
    impl.process_inputs()
    imgui.new_frame()
    
    gl.glClearColor(0.1, 0.1, 0.1, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    
    render_function()
    imgui.render()
    impl.render(imgui.get_draw_data())
    glfw.swap_buffers(window)
    

def impl_glfw_init(width: int, height: int, window_name: str):
    """
    width: window width
    height: windows height
    window_name: window name
    """
    if not glfw.init():
        print("Could not initialize OpenGL context")
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    window = glfw.create_window(width, height, window_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        sys.exit(1)

    return window