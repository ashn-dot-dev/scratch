#include "shader.hpp"

#include <cassert>
#include <cstdio>
#include <optional>

#include "util.hpp"

shader::shader()
{
    shader_id = 0;
    uniform_projection = 0;
    uniform_model = 0;
}

shader::~shader()
{
    clear_shader();
}

void
shader::create_from_string(
    std::string const& vertex, std::string const& fragment)
{
    compile_shader(vertex, fragment);
}

void
shader::create_from_file(std::string const& vertex, std::string const& fragment)
{
    auto vert_optional = read_entire_file(vertex);
    auto frag_optional = read_entire_file(fragment);
    assert(vert_optional.has_value());
    assert(frag_optional.has_value());
    create_from_string(vert_optional.value(), frag_optional.value());
}

GLint
shader::get_projection_location()
{
    return uniform_projection;
}

GLint
shader::get_model_location()
{
    return uniform_model;
}

void
shader::use_shader()
{
    glUseProgram(shader_id);
}

void
shader::clear_shader()
{
    if (shader_id != 0) {
        glDeleteProgram(shader_id);
        shader_id = 0;
    }

    uniform_projection = 0;
    uniform_model = 0;
}

void
shader::compile_shader(std::string const& vertex, std::string const& fragment)
{
    shader_id = glCreateProgram();

    if (!shader_id) {
        std::fprintf(stderr, "error creating shader program\n");
        return;
    }

    add_shader(shader_id, vertex, GL_VERTEX_SHADER);
    add_shader(shader_id, fragment, GL_FRAGMENT_SHADER);

    GLint result = 0;
    GLchar elog[1024] = {0};

    glLinkProgram(shader_id);
    glGetProgramiv(shader_id, GL_LINK_STATUS, &result);
    if (!result) {
        glGetProgramInfoLog(shader_id, sizeof(elog), NULL, elog);
        std::fprintf(stderr, "error linking shader program: %s\n", elog);
        return;
    }

    glValidateProgram(shader_id);
    glGetProgramiv(shader_id, GL_VALIDATE_STATUS, &result);
    if (!result) {
        glGetProgramInfoLog(shader_id, sizeof(elog), NULL, elog);
        std::fprintf(stderr, "error validating shader program: %s\n", elog);
        return;
    }

    uniform_model = glGetUniformLocation(shader_id, "model");
    uniform_projection = glGetUniformLocation(shader_id, "projection");
}

void
shader::add_shader(GLuint program, std::string const& code, GLenum type)
{
    GLuint shader = glCreateShader(type);
    GLchar const* code_buf[1];
    code_buf[0] = code.c_str();

    GLint code_len[1];
    code_len[0] = (GLint)code.length();

    glShaderSource(shader, 1, code_buf, code_len);
    glCompileShader(shader);

    GLint result = 0;
    GLchar elog[1024] = {0};

    glGetShaderiv(shader, GL_COMPILE_STATUS, &result);
    if (!result) {
        glGetShaderInfoLog(shader, sizeof(elog), NULL, elog);
        std::fprintf(
            stderr, "error compiling shader %d: %s\n", (int)type, elog);
        return;
    }

    glAttachShader(program, shader);
}
