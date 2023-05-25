#ifndef MESH_HPP_INCLUDED
#define MESH_HPP_INCLUDED

#include <cstddef>

#include <GL/glew.h>
#include <GLFW/glfw3.h>

class mesh {
public:
    mesh();
    ~mesh();

    mesh(mesh const&) = delete;
    mesh& operator=(mesh const&) = delete;

    void create_mesh(
        GLfloat* vertices,
        std::size_t vertices_count,
        GLuint* indices,
        std::size_t indices_count);
    void render_mesh();
    void clear_mesh();

private:
    GLuint VAO;
    GLuint VBO;
    GLuint IBO;
    GLsizei indices_count;
};

#endif
