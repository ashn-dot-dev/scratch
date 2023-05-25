#include "mesh.hpp"

mesh::mesh()
{
    VAO = 0;
    VBO = 0;
    IBO = 0;
    indices_count = 0;
}

mesh::~mesh()
{
    clear_mesh();
}

void
mesh::create_mesh(
    GLfloat* vertices,
    std::size_t vertices_count,
    GLuint* indices,
    std::size_t indices_count)
{
    this->indices_count = (GLsizei)indices_count;

    glGenVertexArrays(1, &VAO);
    glBindVertexArray(VAO);

    // GL_STATIC_DRAW: Data in the vertices will not change.

    glGenBuffers(1, &IBO);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, this->IBO);
    glBufferData(
        GL_ELEMENT_ARRAY_BUFFER,
        indices_count * sizeof(*indices),
        indices,
        GL_STATIC_DRAW);

    glGenBuffers(1, &VBO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(
        GL_ARRAY_BUFFER,
        vertices_count * sizeof(*vertices),
        vertices,
        GL_STATIC_DRAW);

    // Index of 0 is used for `location = 0` for `pos` in the vertex shader.
    // Stride of 0: Data is tightly packed.
    // Pointer of 0: No offset into the data.
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0);
    glEnableVertexAttribArray(0);

    glBindBuffer(GL_ARRAY_BUFFER, 0); // unbind VBO
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0); // unbind IBO
    glBindVertexArray(0); // unbind VAO
}

void
mesh::render_mesh()
{
    glBindVertexArray(VAO);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO);
    // glDrawArrays w/ GL_TRIANGLES: Draw using points from the VAO (used
    // without binding to the IBO).
    // glDrawElements w/ GL_TRIANGLES: Draw using points from the VAO
    // indexed by the IBO.
    glDrawElements(GL_TRIANGLES, indices_count, GL_UNSIGNED_INT, 0);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
    glBindVertexArray(0);
}

void
mesh::clear_mesh()
{
    if (IBO != 0) {
        glDeleteBuffers(1, &IBO);
        IBO = 0;
    }
    if (VBO != 0) {
        glDeleteBuffers(1, &VBO);
        VBO = 0;
    }
    if (VAO != 0) {
        glDeleteVertexArrays(1, &VAO);
        VAO = 0;
    }
    indices_count = 0;
}
