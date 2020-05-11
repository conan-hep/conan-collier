cmake_minimum_required(VERSION 2.8.12)
project(PackageTest C Fortran)

set(CMAKE_VERBOSE_MAKEFILE ON)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_executable(example_f example.f90)
target_link_libraries(example_f CONAN_PKG::COLLIER)

add_executable(example_c example.c)
target_link_libraries(example_c CONAN_PKG::COLLIER)
