# Example installation of COLLIER using conan

Run the following commands to setup the `build` directory and install
the project dependencies locally:

    mkdir build
    cd build
    conan install ..

Build with CMake/make:

    cmake ..
    make

Build with Meson/ninja:

    export PKG_CONFIG_PATH=.
    meson ..
    ninja

Build with make:

    make -f ../Makefile
