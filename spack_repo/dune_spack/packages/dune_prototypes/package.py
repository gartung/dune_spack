# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class DunePrototypes(CMakePackage):
    """Duneprototypes"""

    git = "https://github.com/DUNE/duneprototypes"
    url = f"{git}/archive/v09_81_00d00.tar.gz"

    version("10.11.01d00", sha256="48092deb82a301620004b04738ab61d4540ce55237c9f15e4968f931c6f841a8")
    version("10.10.02d00", sha256="51da2c142dbce1fc722fbab763a351f55ed261b046af3c512f51fc05f329c305")
    version("10.10.00d00", sha256="cc516a47bce46c93b2cd7a0a2335e3d249f6603551f92d8497959bb22e976fdb")
    version("10.09.00d00", sha256="5acd267eab98f36dafefa1d8dad928145932b878d86df5de532f13ab6806550d")
    version("10.08.01d00", sha256="53269c0e244d86e8a2c222ef06b4bcf4aa2ccc2b31c3ada24d70e9a05d020c06")
    version("10.08.00d00", sha256="fc74e2fd11a7d92806746af4f8e79bda19fe7194f386569a6af38d9ebc78575e")
    version("10.07.00d00", sha256="95cd3551ce003510baa5ef9495ff3d7aab21aa63f6d834347ed638e14c6436fe")
    version("10.06.00d01", sha256="6a4408db6dbcbc3cec48c9f383f6b83b55a3c47b09be4c15c83c66aff20b7d28")
    version("10.06.00d00", sha256="25d2db6be55b1d39214c3d9ca781d0982e67e4c053b6394f8c41ad5b40dad483")
    version("10.08.02d00", sha256="650e67104dba0a42d283c3afac2d509adab821762cc2d9a41fa4a584e6272632")
    version("10.00.03d00", sha256="c3ed09c70ce39df44edc506680b7eb1eac7b562a05e7d703284a915525af0e49")
    version("09.92.00d00", sha256="536429aa8cfb94f54cd790609128fef311a8ef9b92449e4c79a2e4459891f272")
    version("09.91.04d01", sha256="7c423246df1e518d63270e6da9f3f437f1aa2be4756f6794b24cea1a4060e66d")
    version("09.89.01d01", sha256="140a6a20b2ddabd70572172d57c348ea618d6b0a1bfe0ade29c767842e540fe2")
    version("09.81.00d00", sha256="99a3e4eb98bfb9c7e7adeb3eb295332b71008c5bf6749587413ec97688532c85")
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

    patch('artdaq-core-4.0.patch', when='^artdaq-core@v4:')

    # clean out vestigial dunesim, duneprototypes references
    patch('v10_10_02d00.patch', when='@10.10.02d00') 


    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")
    depends_on("dune-calib")
    # makes a cycle, may not actually be used(!)
    #depends_on("dune-sim")
    #depends_on("dune-op-det")
    depends_on("nuevdb")


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
