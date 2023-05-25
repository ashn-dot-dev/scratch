#ifndef SHADER_HPP_INCLUDED
#define SHADER_HPP_INCLUDED

#include <cstdio>
#include <string>

#include <GL/glew.h>

class shader {
public:
    shader();
    ~shader();

    void
    create_from_string(std::string const& vertex, std::string const& fragment);
    void
    create_from_file(std::string const& vertex, std::string const& fragment);
    GLint get_projection_location();
    GLint get_model_location();
    void use_shader();
    void clear_shader();

private:
    GLuint shader_id;
    GLint uniform_projection;
    GLint uniform_model;

    void compile_shader(std::string const& vertex, std::string const& fragment);
    void add_shader(GLuint program, std::string const& code, GLenum type);
};

#endif
