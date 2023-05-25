#ifndef WINDOW_HPP_INCLUDED
#define WINDOW_HPP_INCLUDED

#include <string>
#include <GL/glew.h>
#include <GLFW/glfw3.h>

class window {
public:
    window() = delete;
    window(window const&) = delete;
    window(
        int w,
        int h,
        std::string const& title,
        bool make_context_current = true);
    ~window();

    int framebuffer_w();
    int framebuffer_h();
    void make_current();
    bool should_close();
    void present();

private:
    GLFWwindow* glfw_window;
    int glfw_framebuffer_w;
    int glfw_framebuffer_h;
};

#endif
