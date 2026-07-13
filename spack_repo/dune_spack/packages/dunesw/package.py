# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


DUNE_PARDATA_DIR = "/cvmfs/dune.osgstorage.org/pnfs/fnal.gov/usr/dune/persistent/stash"


class Dunesw(CMakePackage):
    """Dunesw"""

    git = "https://github.com/DUNE/dunesw"
    url = f"{git}/archive/v09_81_00d00.tar.gz"

    version("10.20.09d02", sha256="6df790cc31cd7e50d1e6287d18958c2b8afe3ffa21aa3412ed58f6f859781134")
    version("10.20.03d01", sha256="6ab024528d992e73f40f5cd88eff2f027d60b83ff598ca654a98d088ba5daf79")
    version("10.11.01d00", sha256="023a7e33cfd7b8af300f1fcfe566083f3f6c7bc7385a14f42ce7ff15e5b9a99e")
    version("10.10.02d00", sha256="9189a294b331b6046bbf6dd1b5e9885c7b789f5725fbc3cec555597f3307516c")
    version("10.10.00d00", sha256="d06f45c220cc5bd68caadbc3066b7c05c760519ac94cd9b66c1d6758c8b62da3")
    version("10.09.00d00", sha256="ac08d28083ec2611542c542748e6c189fe5e376a00de7ac9d81254e421274fe8")
    version("10.08.02d00", sha256="d617560b80eadff1bac4e0b17a7ada47f187062341de83f6293e94126816f3dd")
    version("10.08.01d00", sha256="200315053559d1467d58b9e753de0054ed8ae1f11007b7037eaf9c7c82c5d834")
    version("10.08.00d00", sha256="a756730d682bb05ac888d2cdc27f2af743cbe41ae5152c7682f90e24f071a59c")
    version("10.07.00d00", sha256="5328cb0c2fb93c2967fd0d276c6a454348b07a11c261716876cca2f8d00dab74")
    version("10.06.00d01", sha256="da36c4db529f33edb1f038d055b6701943065246119f67aa0f6a51e0ff32acd3")
    version("10.06.00d00", sha256="0d1ce7bb39c2bf91574b116c75732b855bc44e8755bb1c8d0975215255871249")
    version("10.05.00d00", sha256="305594eefa4ee3c12e4600911913632738d6ed13d263f097031859cb0d8313d7")
    version("10.04.07d01", sha256="a52c44a29da140159498e45144f6ff7eb76e01a72e059a12b0533bd7ee26b46b")
    version("10.04.07d00", sha256="fcd5b54e748f0a8114a495ff4833fc370ed347c1e8582a7b78e84630d1846c5f")
    version("10.04.06d00", sha256="0e14f88e3d3146c23cee3d092c2403d0aeae930fc57f0a9561f70ed3bd45676b")
    version("10.00.03d00", sha256="dbfc1dfa606a0c44152b39ae9f4efc5084436984dcbe00370da354c9f44fb966")
    version("09.92.00d00", sha256="0e3bae89b9e01f3b29303d5b65a72c5122c906e7f54c92ed9f282e13641d12c0")
    version("09.91.04d01", sha256="a2e64abc0527c91bd66c1854507a95659b81cfc322713e96319e4cf0e0e748c3")
    version("09.89.01d01", sha256="d516d3f7c00ed99fe23de77152bad556b5a6a24e777e3e5ec7d7a4beddaff3cb")
    version("09.81.00d01", sha256="126477cb91b6fd7a69ef2753505ca8dcd5739f4f509409cbf6f93f0774574862")
    version("09.81.00d00", sha256="f32da1e3e3ac4482674dcd3559c23a8acd10bc994e95df37ac22778e63fd72cd")
    version("develop", branch="develop")

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

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("duneana")
    depends_on("dunedataprep")
    depends_on("duneexamples")
    depends_on("protoduneana")
    depends_on("nurandom")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")
    depends_on("justin", type="run")
    depends_on("larg4", type="run")
    depends_on("dune-pardata", type="run")

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
        run_env.prepend_path("FW_SEARCH_PATH", DUNE_PARDATA_DIR)

    def setup_dependent_run_environment(self, run_env, dspec):
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("PATH", self.prefix.bin)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        run_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
        run_env.prepend_path("FW_SEARCH_PATH", DUNE_PARDATA_DIR)
