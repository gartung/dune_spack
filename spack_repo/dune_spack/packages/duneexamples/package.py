# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Duneexamples(CMakePackage, FnalGithubPackage):
    """Duneexamples"""

    repo = "DUNE/duneexamples"
    version_patterns = ["09_00_00d00", "09.14.19"]

    version("10_00_03d00", sha256="3e91fbcd0fbd6cae65f7f3e29784cfcf2ebeaeb3d5a2195964d432f9b5f7233e")
    version("09_92_00d00", sha256="e251ec860ae0c401cecc6c4ac985b203b625a8c1675d46a7a06309d7461598c4")
    version("09_89_01d01", sha256="fadad2d0d0f363bd9f52191ab0b6e0534f34b086098a16cafe9c93e5843cd99b")
    version("09_81_00d00", sha256="5ca163fe371aee48601d4ee63da447f26901a610d3bb175070aac113f93a5779")
    version("develop", branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch('v09_81_00d00.patch', when='@09_81_00d00')

    depends_on("art")
    depends_on("art-root-io")
    depends_on("canvas-root-io")
    depends_on("boost")
    depends_on("root")
    depends_on("dunecore")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
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
