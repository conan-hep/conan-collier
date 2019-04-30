from conans import ConanFile, CMake, tools
from conans.errors import ConanException


class CollierConan(ConanFile):
    name = "COLLIER"
    version = "1.2.3"
    license = "GPL-3.0-only"
    author = "Alexander Voigt"
    url = "https://collier.hepforge.org/"
    description = "A Complex One-Loop Library with Extended Regularizations"
    topics = ("HEP")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    exports = ["LICENSE", "FindCOLLIER.cmake"]
    default_options = "shared=False", "fPIC=True"
    generators = ["cmake", "make", "pkg_config"]
    _source_subfolder = "COLLIER-{}".format(version)

    def source(self):
        src_file = "https://collier.hepforge.org/downloads/collier-{}.tar.gz".format(self.version)

        try:
            tools.get(src_file)
        except ConanException:
            raise ConanException("Could not download source code {}".format(src_file))

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("COPYING", src=self._source_subfolder, dst="licenses", keep_path=False)
        self.copy('FindCOLLIER.cmake', '.', '.')

    def package_info(self):
        self.cpp_info.libs = ["collier"]
