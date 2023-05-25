#include <cassert>
#include <stdexcept>

#include "window.hpp"

static void
key_callback(GLFWwindow* window, int key, int scancode, int action, int mods)
{
    (void)scancode;
    (void)mods;

    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS) {
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    }
}

window::window(int w, int h, std::string const& title, bool make_current)
{
    glfw_window = glfwCreateWindow(w, h, title.c_str(), nullptr, nullptr);
    if (!glfw_window) {
        throw std::runtime_error("GLFW window creation failed");
    }

    glfwSetKeyCallback(glfw_window, key_callback);
    glfwGetFramebufferSize(
        glfw_window, &glfw_framebuffer_w, &glfw_framebuffer_h);

    if (make_current) {
        window::make_current();
    }
}

window::~window()
{
    glfwDestroyWindow(glfw_window);
}

int
window::framebuffer_w()
{
    return glfw_framebuffer_w;
}

int
window::framebuffer_h()
{
    return glfw_framebuffer_h;
}

void
window::make_current()
{
    glfwMakeContextCurrent(glfw_window);
}

bool
window::should_close()
{
    return glfwWindowShouldClose(glfw_window);
}

void
window::present()
{
    glfwSwapBuffers(glfw_window);
}
