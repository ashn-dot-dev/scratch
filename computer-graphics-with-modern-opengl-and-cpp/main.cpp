#include <cstdio>
#include <cstdlib>

#include <GL/glew.h>
#include <GLFW/glfw3.h>

static constexpr GLint WINDOW_W = 800;
static constexpr GLint WINDOW_H = 600;

static void
key_callback(GLFWwindow* window, int key, int scancode, int action, int mods)
{
    (void)scancode;
    (void)mods;

    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS) {
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    }
}

int
main()
{
    /* Init GLFW */
    if (!glfwInit()) {
        std::fprintf(stderr, "GLFW initialization failed\n");
        std::exit(EXIT_FAILURE);
    }

    /* Setup GLFW window properties. */
    // OpenGL version.
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    // Core profile: No backwards compatibility.
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    // Allow forward compatibility.
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);

    /* Create window. */
    GLFWwindow* window =
        glfwCreateWindow(WINDOW_W, WINDOW_H, "TEST WINDOW", NULL, NULL);
    if (!window) {
        std::fprintf(stderr, "GLFW window creation failed\n");
        glfwTerminate();
        std::exit(EXIT_FAILURE);
    }
    glfwSetKeyCallback(window, key_callback);

    /* Get buffer size information. */
    int buffer_w = -1;
    int buffer_h = -1;
    glfwGetFramebufferSize(window, &buffer_w, &buffer_h);
    std::printf("window size: %dx%d\n", buffer_w, buffer_h);

    /* Set context for GLEW to use. */
    glfwMakeContextCurrent(window);

    /* Allow modern extension features. */
    glewExperimental = GL_TRUE;
    if (GLEW_OK != glewInit()) {
        std::fprintf(stderr, "GLEW initialization failed\n");
        glfwDestroyWindow(window);
        glfwTerminate();
        std::exit(EXIT_FAILURE);
    }

    /* Setup viewport size. */
    glViewport(0, 0, buffer_w, buffer_h); // entire window

    /* Main loop. */
    while (!glfwWindowShouldClose(window)) {
        /* Get and handle user input events. */
        glfwPollEvents();

        /* Clear window. */
        glClearColor(1.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        /* Present the window. */
        glfwSwapBuffers(window);
    }

    std::printf("exiting successfully\n");
    return EXIT_SUCCESS;
}
