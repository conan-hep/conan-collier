import os
from conans import ConanFile, CMake, tools
from conans.errors import ConanException
from conans.model.version import Version
from conans.tools import SystemPackageTool

# python 2 / 3 StringIO import
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class CollierConan(ConanFile):
    name = "COLLIER"
    version = "1.2.4"
    license = "GPL-3.0-only"
    author = "Alexander Voigt"
    url = "https://collier.hepforge.org/"
    description = "A Complex One-Loop Library with Extended Regularizations"
    topics = ("HEP")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    exports = ["LICENSE"]
    exports_sources = '*.patch'
    default_options = "shared=False", "fPIC=True"
    generators = ["cmake", "make", "pkg_config"]
    _source_subfolder = "COLLIER-{}".format(version)
    _module_subfolder = "{}{}modules".format(_source_subfolder, os.sep)

    def _have_fortran_compiler(self):
        return tools.which("gfortran") != None or tools.which("ifort") != None

    def source(self):
        src_file = "https://collier.hepforge.org/downloads/collier-{}.tar.gz".format(self.version)

        try:
            tools.get(src_file)
        except ConanException:
            raise ConanException("Could not download source code {}".format(src_file))

    def build(self):
        tools.patch(base_path=self._source_subfolder,
                    patch_file="00_add_definitions.patch")

        cmake = CMake(self)
        cmake.definitions["static"] = not(self.options.shared)
        cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()

    def system_requirements(self):
        installer = SystemPackageTool()

        if not self._have_fortran_compiler():
            if tools.os_info.is_linux:
                if tools.os_info.with_pacman or tools.os_info.with_yum or tools.os_info.with_zypper:
                    installer.install("gcc-fortran")
                else:
                    installer.install("gfortran")
                    versionfloat = Version(self.settings.compiler.version.value)
                    if self.settings.compiler == "gcc":
                        if versionfloat < "5.0":
                            installer.install("libgfortran-{}-dev".format(versionfloat))
                        else:
                            installer.install("libgfortran-{}-dev".format(int(versionfloat)))

        if tools.os_info.is_macos and Version(self.settings.compiler.version.value) > "7.3":
            try:
                installer.install("gcc", update=True, force=True)
            except Exception:
                self.output.warn("brew install gcc failed. Tying to fix it with 'brew link'")
                self.run("brew link --overwrite gcc")

    def package(self):
        self.copy("*.h", dst="include", src="src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.mod", dst="include", src=self._module_subfolder)
        self.copy("COPYING", src=self._source_subfolder, dst="licenses", keep_path=False)

    def _get_lib_path(self, libname):
        out = StringIO()
        try:
            self.run("gfortran --print-file-name {}".format(libname), output=out)
        except Exception as error:
            raise ConanException("Failed to run command: {}. Output: {}".format(error, out.getvalue()))
        path = os.path.normpath(out.getvalue().strip())
        return os.path.dirname(path) if os.path.exists(path) else None

    def package_info(self):
        self.cpp_info.libs = ["collier", "gfortran"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("m")

        # explicit paths to libraries on MacOS
        if self.settings.os == "Macos":
            # add path of libgfortran
            path = self._get_lib_path('libgfortran.dylib')
            if path: self.cpp_info.libdirs.append(path)
