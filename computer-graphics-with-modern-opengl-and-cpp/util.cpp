#include "util.hpp"

#include <fstream>
#include <sstream>

std::optional<std::string>
read_entire_file(std::filesystem::path const& path)
{
    if (!std::filesystem::is_regular_file(path)) {
        return std::nullopt;
    }

    auto fstream = std::ifstream(path, std::ios::in | std::ios::binary);
    if (!fstream.is_open()) {
        return std::nullopt;
    }

    std::stringstream sstream;
    sstream << fstream.rdbuf();

    fstream.close();
    return sstream.str();
}
