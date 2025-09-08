# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Dunesim(CMakePackage, FnalGithubPackage):
    """Dunesim"""

    repo = "DUNE/dunesim"
    git = "https://github.com/%s.git" % repo
    version_patterns = ["v09_00_00d00", "09.14.19"]

    version("10_08_02d00", sha256="afe07128fe9fbe6214314b2dd6bb247e30747d7646d6ecb30de5160054e58277")
    version("10_00_03d00", sha256="9a62b3c10eada40b443c512cd59d7f30458f7906d1c719da21795932a3b612ae")
    version("09_92_00d00", sha256="281df90bd373866bf9ab9005c1308b8eb74d75109fcd6cdeca1635d4f6435a17")
    version("09_89_01d01", sha256="130c0b293e35cbf3d693ba3239642751bf87b4ad636a640bcdc137a3c66b7160")
    version("09_81_00d00", sha256="60907d1c14a16c2734757950a09834bf4627509f3f02735c26b8bee00a612d21")
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

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("art")
    depends_on("art-root-io")
    depends_on("larevt")
    depends_on("larsim")
    depends_on("lardataalg")
    depends_on("lardataobj")
    depends_on("larcore")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("nusimdata")
    depends_on("nurandom")
    depends_on("dunecore")
    depends_on("lardata")
    depends_on("clhep")
    depends_on("nugen")
    depends_on("dk2nudata")
    depends_on("geant4")
    depends_on("genie-xsec")
    depends_on("genie-phyopt")
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
