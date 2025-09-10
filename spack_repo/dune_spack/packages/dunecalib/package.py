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
    git = "https://github.com/%s" % repo
    version_patterns = ["v09_00_00d00", "09.14.19"]

    version("10_10_02d00", sha256="19b8848adf351f8874727a8ba5756d8c96e32b622fcf97d546ed668a930183d6")
    version("10_10_00d00", sha256="adf709d4b54534adbd7a236e8c5c43657a06ee338425ae307a58d128ffc50b35")
    version("10_09_00d00", sha256="8a19779a089ca41de8cc6498ce37153dbeaf2af411b91026f2ae3255fbea10ad")
    version("10_08_02d00", sha256="059311324acce8eebb331923ad428397eb31e97965a18fb265de9a0d36436fc8")
    version("10_08_01d00", sha256="8ba902610b967397b6ca9281716bdba613b41b512872cd52345ea96d08c6c52d")
    version("10_08_00d00", sha256="33a2b8ab97db39172d589d1421606389d4edf88e6f2582991342059f36a9c832")
    version("10_07_00d00", sha256="4758c54f3eb3eb194bb359dd7b9ce6a7427332340da231c68ac8dbf8cf38751f")
    version("10_06_00d01", sha256="3f7b6414cb158193d93c787e820bcc5ec1bf7867f1263cf69e2303d24f142b4f")
    version("10_06_00d00", sha256="c981be97353dfcc9e8635761cefd835c556230c6c9a7035745ffa0d061958449")
    version("10_00_03d00", sha256="9e83970562ee11e07cc3da6c322c8773d73ea466e9ab5c33ab67c44172077404")
    version("09_91_04d01", sha256="419b2e89d72ce52583bd1ec16de584376daa9b3189faf6f7387a5ce44258015f")
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

    def _url_for_tag(self, version_str):
        return f"{self.git}/archive/refs/tags/v{version_str}.tar.gz"

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
