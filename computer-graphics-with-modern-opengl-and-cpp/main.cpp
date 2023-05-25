#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <stdexcept>
#include <vector>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include "mesh.hpp"
#include "shader.hpp"
#include "window.hpp"
#include "util.hpp"

static constexpr GLint WINDOW_W = 800;
static constexpr GLint WINDOW_H = 600;

std::vector<mesh*> mesh_list;
std::vector<shader*> shader_list;

static void
create_objects()
{
    GLfloat vertices[] = {
        // clang-format off
        -1.0f, -1.0f, +0.0f,
        +0.0f, -1.0f, +1.0f,
        +1.0f, -1.0f, +0.0f,
        +0.0f, +1.0f, +0.0f,
        // clang-format on
    };
    GLuint indices[] = {
        // clang-format off
        0, 3, 1,
        1, 3, 2,
        2, 3, 0,
        0, 1, 2
        // clang-format on
    };

    auto m = new mesh();
    m->create_mesh(
        vertices,
        sizeof(vertices) / sizeof(*vertices),
        indices,
        sizeof(indices) / sizeof(*indices));
    mesh_list.push_back(m);
}

static void
create_shaders()
{
    auto s = new shader();
    s->create_from_file("shaders/shader.vert", "shaders/shader.frag");
    shader_list.push_back(s);
}

int
main()
{
    auto start = std::chrono::high_resolution_clock::now();

    /* Init GLFW */
    if (!glfwInit()) {
        std::fprintf(stderr, "GLFW initialization failed\n");
        std::exit(EXIT_FAILURE);
    }
    DEFER(glfwTerminate());

    /* Setup GLFW window properties. */
    // OpenGL version.
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    // Core profile: No backwards compatibility.
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    // Allow forward compatibility.
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);

    auto window = ::window(WINDOW_W, WINDOW_H, "TEST WINDOW");

    glewExperimental = GL_TRUE;
    if (GLEW_OK != glewInit()) {
        std::fprintf(stderr, "GLEW initialization failed\n");
        std::exit(EXIT_FAILURE);
    }

    int const buffer_w = window.framebuffer_w();
    int const buffer_h = window.framebuffer_h();

    /* Enable depth test. */
    glEnable(GL_DEPTH_TEST);

    /* Setup viewport size. */
    glViewport(0, 0, buffer_w, buffer_h); // entire window

    create_objects();
    create_shaders();

    float fovy = 45.0f; // FOV in the Y direction.
    float aspect = (GLfloat)buffer_w / (GLfloat)buffer_h;
    float z_near = 0.1f;
    float z_far = 100.0f;
    glm::mat4 projection = glm::perspective(fovy, aspect, z_near, z_far);

    /* Main loop. */
    while (!window.should_close()) {
        auto now = std::chrono::high_resolution_clock::now();
        std::chrono::duration<float> elapsed = now - start;

        /* Get and handle user input events. */
        glfwPollEvents();

        float x_translation = 0.5f * std::sin(elapsed.count());
        float y_translation = 0.5f * std::cos(elapsed.count());
        [[maybe_unused]] float angle = elapsed.count();
        [[maybe_unused]] float scale = 0.5f + std::sin(elapsed.count()) / 4.0f;

        /* Clear window (color and depth). */
        glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        shader_list[0]->use_shader();
        glUniformMatrix4fv(
            shader_list[0]->get_projection_location(),
            1,
            GL_FALSE,
            glm::value_ptr(projection));

        glm::mat4 model(1.0f);
        model = glm::translate(
            model, glm::vec3(x_translation, y_translation, -2.5f));
        model = glm::rotate(model, angle, glm::vec3(0.0f, 1.0f, 0.0f));
        model = glm::scale(model, glm::vec3(0.4f, 0.4f, 0.8f));
        glUniformMatrix4fv(
            shader_list[0]->get_model_location(),
            1,
            GL_FALSE,
            glm::value_ptr(model));
        mesh_list[0]->render_mesh();

        model = glm::mat4(1.0f);
        model = glm::translate(
            model, glm::vec3(-x_translation, -y_translation, -2.5f));
        model = glm::rotate(model, angle, glm::vec3(0.0f, 1.0f, 0.0f));
        model = glm::scale(model, glm::vec3(0.4f, 0.4f, 0.8f));
        glUniformMatrix4fv(
            shader_list[0]->get_model_location(),
            1,
            GL_FALSE,
            glm::value_ptr(model));
        mesh_list[0]->render_mesh();

        glUseProgram(0);

        /* Present the window. */
        window.present();
    }

    std::printf("exiting successfully\n");
    return EXIT_SUCCESS;
}
