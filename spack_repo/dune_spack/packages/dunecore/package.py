# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class Dunecore(CMakePackage):
    """Dunecore"""

    git = "https://github.com/DUNE/dunecore"
    url = f"{git}/archive/v09_81_00d00.tar.gz"

    version("10.11.01d00", sha256="273763ea8775e981b8c5085419125117456480a21d5fe785ce982edf21162c35")
    version("10.10.02d00", sha256="2d65081ec4ec52a2d341f4bb05326bad710ab41f25af3c369b9ea28f74ffb455")
    version("10.10.00d00", sha256="b7323d708b76b8729306bf6b669ed76549baf63a967224ec85034aab2e4ad765")
    version("10.09.00d00", sha256="3c5d359cfd658304a8de2531cafc1939a413cd0030de68c98f4c453c56239eb4") 
    version("10.08.02d00", sha256="e2f0667237b7982461fb6770805ee265dce76ba53e97ada93c33046dfb4a557c")
    version("10.08.01d00", sha256="09e6a73ef38156037ef77b30e56ef06cbb0c4bbaa11ec8c76791253c9236e6b9")
    version("10.08.00d00", sha256="f4f345ad81f1f3548c70362342c1b6646040f6f0f0f8c5f3895f6b55e4712e1d")
    version("10.07.00d00", sha256="0b18c8abe1c61e7ccf8d3a6927f9d10d731863c7c19a70d8358b66547646f85f")
    version("10.06.00d01", sha256="3b59c06f49c3d44bed7bbed0d755ce828c9f058e95d55caab9ae8d9faf1458b9")
    version("10.06.00d00", sha256="c05edc3808fa06010400133e3c03c5b7cb62f76faed6ce5772340e14f66eecea")
    version("10.00.03d00", sha256="853476dfd8e1c97e34e03d0bf47a393a4de2e61af3b7623a41a7004c24851647")
    version("09.92.00d00", sha256="37edf3afd3be02cbd64adef1ab1c5c9c7e275d7ffcee44ffce2172451f94dbcd")
    version("09.91.04d01", sha256="9ffa4a416c06f9d921b03f80e0b24eeaf877a5a7de67d3cb00ed145e0466dbfd")
    version("09.89.01d01", sha256="cf61a68d0810103bd45a1133a969378817caf2e09be87ebcaea718ac4bd09060")
    version("09.81.00d00", sha256="4dd8f63fd791167bc55c5fba28f0a9310c2339c0cc3c70bd15e510d36d0ff972")
    version("develop", branch="develop", get_full_repo=True)

    def url_for_version(self, version):
        return f"{self.git}/archive/v{version.underscored}.tar.gz"

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch('v09_81_00d00.patch', when='@09.81.00d00')
    patch('v09_92_00d00.patch', when='@09.92.00d00')
    patch('artdaq-core-4.0.patch', when='^artdaq-core@v4:')
    def patch(self):
        filter_file('LANGUAGES CXX', 'LANGUAGES CXX C', 'CMakeLists.txt')
        filter_file(r'find_package\( nusimdata REQUIRED EXPORT \)$',
                    'find_package( nusimdata REQUIRED EXPORT )\nfind_package( gallery REQUIRED EXPORT )',
                    'CMakeLists.txt')

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")
    depends_on("art")
    depends_on("artdaq-core")
    depends_on("art-root-io")
    depends_on("boost")
    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("clhep")
    depends_on("critic")
    depends_on("dunedaqdataformats")
    depends_on("dunedetdataformats")
    depends_on("dunepdlegacy")
    depends_on("duneutil")
    depends_on("eigen")
    depends_on("fftw")
    depends_on("fhicl-cpp")
    depends_on("gallery")
    depends_on("geant4")
    depends_on("genie")
    depends_on("hdf5@1.12:1.13")
    depends_on("hep-concurrency")
    depends_on("highfive@:2.99")
    depends_on("ifdh-art")
    depends_on("ifdhc")
    depends_on("larana")
    depends_on("larcore")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("lardata")
    depends_on("lardataalg")
    depends_on("lardataobj")
    depends_on("larevt")
    depends_on("larpandora")
    depends_on("larreco")
    depends_on("larsim")
    depends_on("messagefacility")
    depends_on("nlohmann-json")
    depends_on("nuevdb")
    depends_on("nufinder")
    depends_on("nug4")
    depends_on("nugen")
    depends_on("nurandom")
    depends_on("nusimdata")
    depends_on("nutools")
    depends_on("pandorasdk")
    depends_on("postgresql")
    depends_on("root")
    depends_on("sqlite")
    depends_on("trace")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("CMAKE_MODULE_PATH", "%s/Modules" % self.spec['nufinder'].prefix),
        ] 
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set("LD_LIBRARY_PATH", "%s/root" % self.spec["root"].prefix.lib)
        spack_env.prepend_path("CMAKE_PREFIX_PATH", self.build_directory)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("PATH", self.prefix.bin)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        run_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))

    def setup_dependent_run_environment(self, run_env, dspec):
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("PATH", self.prefix.bin)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        run_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
