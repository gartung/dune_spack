# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *
from spack_repo.fnal_art.packages.fnal_github_package.package import *

class Duneopdet(CMakePackage, FnalGithubPackage):
    """Duneopdet"""

    repo = "DUNE/duneopdet"
    version_patterns = ["09_00_00d00", "09.14.19"]

    version("10_08_02d00", sha256="c6913cb4f58faea4c279300ea41f51bf51e2c822c2fbd2b5daad70dd97648109")
    version("10_00_03d00", sha256="b3b62f15d20a2db3389e1cdd4480280316f87ee915a81fd4f0d050fc9e202868")
    version("09_92_00d00", sha256="6003147a6b8a0d943a9f11ceebc4ab2fbac48b9041ad78f560a7bd3ae27b4929")
    version("09_89_01d01", sha256="d39bf58d4dedf985f51d8b2d272354047603fc520145b282d17c85cd7877fdbe")
    version("09_81_00d00", sha256="ea4e39071507f9f1697ba2251481d2ff9396238a33ee38c0fe68070c2c1a9750")
    version("develop", branch="develop", get_full_repo=True)


    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch('v10_00_03d00.patch', when='@10_00_03d00')
    patch('v09_81_00d00.patch', when='@09_81_00d00')

    def patch(self):
        filter_file("LANGUAGES CXX", "LANGUAGES CXX C", "CMakeLists.txt")

    depends_on("duneana")
    depends_on("dunecore")
    depends_on("nlohmann-json")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ] 
        return args

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
