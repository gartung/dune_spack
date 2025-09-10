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
    git = "https://github.com/%s" % repo
    version_patterns = ["v09_00_00d00", "09.14.19"]

    version("10_10_02d00", sha256="ab2035194df1c8a9f5acbf9098c3f368254bfc71a6cd88f375583655a1d976ab")
    version("10_10_00d00", sha256="d6e1f046eb2a84622734a66862a9a6ef43922844ff54e74de03994970b890336")
    version("10_09_00d00", sha256="22b2589a4d1e66f38c1669881d8896506f0640ff5568ad88a5f15a0617704331")
    version("10_08_01d00", sha256="c2d8fb46a41e73e3ffe8020fc2962a8bc042dba70ad5823c9ff81c809165d115")
    version("10_08_00d00", sha256="2f4855488926d06a92e6d1b6b8e18e1136b854398a6a674fc7224d57ccadec67")
    version("10_07_00d00", sha256="4366ec942152959a3ffd70a0824f3a995231b01a6a597b35b87e5514a93ee34c")
    version("10_06_00d01", sha256="11e9de585e0be364a1e4893d81dfac8bbbde40e62eea79895bf2a8e62b197e07")
    version("10_06_00d00", sha256="f06d23287dfebb7b43ea0a3839a8e2c3f2c58a6e13de728af311c07ecd3d6962")
    version("10_08_02d00", sha256="afe07128fe9fbe6214314b2dd6bb247e30747d7646d6ecb30de5160054e58277")
    version("10_00_03d00", sha256="9a62b3c10eada40b443c512cd59d7f30458f7906d1c719da21795932a3b612ae")
    version("09_92_00d00", sha256="281df90bd373866bf9ab9005c1308b8eb74d75109fcd6cdeca1635d4f6435a17")
    version("09_91_04d01", sha256="f7ef9deb35d69d2d06381036819aa0357f471dd6c1e6d3285ced3f5157dc6ba5")
    version("09_89_01d01", sha256="130c0b293e35cbf3d693ba3239642751bf87b4ad636a640bcdc137a3c66b7160")
    version("09_81_00d00", sha256="60907d1c14a16c2734757950a09834bf4627509f3f02735c26b8bee00a612d21")
    version("develop", branch="develop", get_full_repo=True)

    def _url_for_tag(self, version_str):
        return f"{self.git}/archive/refs/tags/v{version_str}.tar.gz"

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
