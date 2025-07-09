# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Dunecore(CMakePackage, FnalGithubPackage):
    """Dunecore"""

    repo = "DUNE/dunecore"
    version_patterns = ["09_00_00d00", "09.14.19"]

    version("10_08_02d00", sha256="e2f0667237b7982461fb6770805ee265dce76ba53e97ada93c33046dfb4a557c")
    version("10_00_03d00", sha256="853476dfd8e1c97e34e03d0bf47a393a4de2e61af3b7623a41a7004c24851647")
    version("09_92_00d00", sha256="37edf3afd3be02cbd64adef1ab1c5c9c7e275d7ffcee44ffce2172451f94dbcd")
    version("09_89_01d01", sha256="cf61a68d0810103bd45a1133a969378817caf2e09be87ebcaea718ac4bd09060")
    version("09_81_00d00", sha256="4dd8f63fd791167bc55c5fba28f0a9310c2339c0cc3c70bd15e510d36d0ff972")
    version("develop", branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch('v09_81_00d00.patch', when='@09_81_00d00')
    patch('v09_92_00d00.patch', when='@09_92_00d00')

    def patch(self):
        filter_file('LANGUAGES CXX', 'LANGUAGES CXX C', 'CMakeLists.txt')
        filter_file(r'find_package\( nusimdata REQUIRED EXPORT \)$',
                    'find_package( nusimdata REQUIRED EXPORT )\nfind_package( gallery REQUIRED EXPORT )',
                    'CMakeLists.txt')
    depends_on("boost")
    depends_on("geant4")
    depends_on("root")
    depends_on("eigen")
    depends_on("art")
    depends_on("art-root-io")
    depends_on("artdaq-core")
    depends_on("trace")
    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("cetlib-except")
    depends_on("cetlib")
    depends_on("clhep")
    depends_on("critic")
    depends_on("fhicl-cpp")
    depends_on("nufinder")
    depends_on("genie")
    depends_on("hep-concurrency")
    depends_on("ifdh-art")
    depends_on("ifdhc")
    depends_on("dunepdlegacy")
    depends_on("gallery")
    depends_on("duneutil")
    depends_on("larsoft")
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
    depends_on("nuevdb")
    depends_on("nug4")
    depends_on("nugen")
    depends_on("nurandom")
    depends_on("nusimdata")
    depends_on("nutools")
    depends_on("pandora")
    depends_on("dunedaqdataformats")
    depends_on("dunedetdataformats")
    depends_on("postgresql")
    depends_on("fftw")
    depends_on("sqlite")
    depends_on("nlohmann-json")
    depends_on("highfive")
    depends_on("hdf5@1.12.2")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("CMAKE_MODULE_PATH", "%s/Modules" % self.spec['nufinder'].prefix)
        ] 
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set("LD_LIBRARY_PATH", "%s/root" % self.spec["root"].prefix.lib)

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
