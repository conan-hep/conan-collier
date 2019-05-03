cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX Fortran)

set(CMAKE_VERBOSE_MAKEFILE ON)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(COLLIER REQUIRED)

add_executable(example example.f90)
target_link_libraries(example COLLIER::COLLIER)
