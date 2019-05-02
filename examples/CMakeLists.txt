cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX Fortran)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(COLLIER REQUIRED)

add_executable(test_cmake_fortran test_collier.f90)
target_link_libraries(test_cmake_fortran COLLIER::COLLIER)

add_executable(test_cmake_cpp test_collier.cpp)
target_link_libraries(test_cmake_cpp COLLIER::COLLIER gfortran)
