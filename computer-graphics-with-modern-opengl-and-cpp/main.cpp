#include <cstdio>
#include <cstdlib>
#include <cstring>

#include <GL/glew.h>
#include <GLFW/glfw3.h>

static constexpr GLint WINDOW_W = 800;
static constexpr GLint WINDOW_H = 600;

static GLuint VAO;
static GLuint VBO;
static GLuint program;

// Vertex Shader
static char const* vshader = R"SOURCE(
#version 330

layout (location = 0) in vec3 pos;

void main() {
    gl_Position = vec4(0.4 * pos.x, 0.4 * pos.y, pos.z, 1.0);
}
)SOURCE";

// Fragment Shader
static char const* fshader = R"SOURCE(
#version 330

out vec4 colors;

void main() {
    colors = vec4(1.0, 0.0, 0.0, 1.0);
}
)SOURCE";

static void
key_callback(GLFWwindow* window, int key, int scancode, int action, int mods)
{
    (void)scancode;
    (void)mods;

    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS) {
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    }
}

static void
create_triangle()
{
    GLfloat vertices[] = {
        // clang-format off
        -1.0f, -1.0f, +0.0f,
        +1.0f, -1.0f, +0.0f,
        +0.0f, +1.0f, +0.0f,
        // clang-format on
    };

    glGenVertexArrays(1, &VAO);
    glBindVertexArray(VAO);

    glGenBuffers(1, &VBO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    // GL_STATIC_DRAW: Data in the vertices will not change.
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    // Index of 0 is used for `location = 0` for `pos` in the vertex shader.
    // Stride of 0: Data is tightly packed.
    // Pointer of 0: No offset into the data.
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0);
    glEnableVertexAttribArray(0);

    glBindBuffer(GL_ARRAY_BUFFER, 0); // unbind VBO
    glBindVertexArray(0); // unbind VAO
}

static void
add_shader(GLuint program, char const* shader_code, GLenum shader_type)
{
    GLuint shader = glCreateShader(shader_type);
    GLchar const* code[1];
    code[0] = shader_code;

    GLint code_length[1];
    code_length[0] = std::strlen(shader_code);

    glShaderSource(shader, 1, code, code_length);
    glCompileShader(shader);

    GLint result = 0;
    GLchar elog[1024] = {0};

    glGetShaderiv(shader, GL_COMPILE_STATUS, &result);
    if (!result) {
        glGetShaderInfoLog(shader, sizeof(elog), NULL, elog);
        std::fprintf(
            stderr, "error compiling shader %d: %s\n", (int)shader_type, elog);
        return;
    }

    glAttachShader(program, shader);
}

static void
compile_shaders()
{
    program = glCreateProgram();

    if (!program) {
        std::fprintf(stderr, "error creating shader program\n");
        return;
    }

    add_shader(program, vshader, GL_VERTEX_SHADER);
    add_shader(program, fshader, GL_FRAGMENT_SHADER);

    GLint result = 0;
    GLchar elog[1024] = {0};

    glLinkProgram(program);
    glGetProgramiv(program, GL_LINK_STATUS, &result);
    if (!result) {
        glGetProgramInfoLog(program, sizeof(elog), NULL, elog);
        std::fprintf(stderr, "error linking program: %s\n", elog);
        return;
    }

    glValidateProgram(program);
    glGetProgramiv(program, GL_VALIDATE_STATUS, &result);
    if (!result) {
        glGetProgramInfoLog(program, sizeof(elog), NULL, elog);
        std::fprintf(stderr, "error validating program: %s\n", elog);
        return;
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

    std::printf("VERTEX SHADER:\n```%s```\n", vshader);
    std::printf("FRAGMENT SHADER:\n```%s```\n", fshader);
    create_triangle();
    compile_shaders();

    /* Main loop. */
    while (!glfwWindowShouldClose(window)) {
        /* Get and handle user input events. */
        glfwPollEvents();

        /* Clear window. */
        glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        glUseProgram(program);
        glBindVertexArray(VAO);
        glDrawArrays(GL_TRIANGLES, 0, 3);
        glBindVertexArray(0);
        glUseProgram(0);

        /* Present the window. */
        glfwSwapBuffers(window);
    }

    std::printf("exiting successfully\n");
    return EXIT_SUCCESS;
}
