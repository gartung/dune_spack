# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Dunecalib(CMakePackage, FnalGithubPackage):
    """Dunecalib"""

    repo = "DUNE/dunecalib"
    version_patterns = ["09_00_00d00", "09.14.19"]

    version("10_08_02d00", sha256="059311324acce8eebb331923ad428397eb31e97965a18fb265de9a0d36436fc8")
    version("10_00_03d00", sha256="9e83970562ee11e07cc3da6c322c8773d73ea466e9ab5c33ab67c44172077404")
    version("09_92_00d00", sha256="56749441ad39915e7a3cb807b57f5bc619f2a7806e374cc6f83c73610b369a06")
    version("09_81_00d00", sha256="2bdd7f71f6a0596b3bbb34b2956e6a01274773bde9697965dd887ada36f8801a")
    version("develop", branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch('v09_81_00d00.patch', when='@09_81_00d00')

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("dunecore")
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
