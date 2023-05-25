#ifndef UTIL_HPP_INCLUDED
#define UTIL_HPP_INCLUDED

#include <filesystem>
#include <optional>

[[nodiscard]] std::optional<std::string>
read_entire_file(std::filesystem::path const& path);

template<typename F>
struct defer_type {
    defer_type() = delete;
    defer_type(defer_type const&) = delete;

    // clang-format off
    defer_type(F f) : f(f) {}
    ~defer_type() { f(); }
    // clang-format on

private:
    F f;
};

#define CONCAT(a, b) CONCAT_(a, b)
#define CONCAT_(a, b) a##b
#define DEFER(code)                                                            \
    auto CONCAT(defer_, __COUNTER__) = defer_type([&]() { code; })

#endif
