# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class Dunedataprep(CMakePackage):
    """Dunedataprep"""

    git = "https://github.com/DUNE/dunedataprep"
    url = f"{git}/archive/v09_81_00d00.tar.gz"

    version("10.22.00d00", sha256="bf2460ba5f9ab48595d4ae007895a524cc0b735f6916f8fde2d7ca7ea80f0c60")
    version("10.21.02d00", sha256="b7b3d91df9164e6dde4fddbef0a2d3ff49d2e22738736e21419beb6b5852fb20")
    version("10.21.01d00", sha256="46a68ee1f6407967d901de6025e06eb09e0bd395ee7df757038bee2703b18e10")
    version("10.20.09d02", sha256="f16916223149de4c8925e5b2b9799c6cadf07cc43430ab172bc7132bba49a04a")
    version("10.20.03d01", sha256="02fcef670b77aaa6443e434576d3c7d49b77bbfaa7f9ca53a8f402935d44f653")
    version("10.11.01d00", sha256="d17b6c0ad85f9dfc7ff21f00652cce331a1c8c029bcac87feae8a0ca14da0e00")
    version("10.10.02d00", sha256="2a17eb3e4b812d1a889ad12e6b4f763aef7ebfb7e6da4806e5f6411bcb50769d")
    version("10.10.00d00", sha256="e45a5ebf022298b78cc9f3fad6ddc25f272729f541c1f94f358ee45e971777e4")
    version("10.09.00d00", sha256="24f24adb8991c9ea4c51d30c4c557c29e9880b7ec759742bc5e4691a206a8fb3")
    version("10.08.02d00", sha256="51a4e1511d88139e96e024150a1da592104d92d16e885dbe150fc9a7ef39406f")
    version("10.08.01d00", sha256="c7ba3ebd7d98b26abd04a6acfdcaac19faee7a54d4c8ca354512eb46ef8c8a29")
    version("10.08.00d00", sha256="81a6f2da7caf05f81cac6e483ccc0819db4f065bc293259200bcd0751c4df885")
    version("10.07.00d00", sha256="de9b0d250d83e5b1971d8b937ef4d3273e4612edb5a3ab57f8a66bd632aff646")
    version("10.06.00d01", sha256="473cca0042df58174eec398b05f63c98b29bfc930c44073acb15ca28a2eb27c7")
    version("10.06.00d00", sha256="3557189052de175ae109e6895c9acb0757056e75a5b299aa167273e1070f638c")
    version("10.00.03d00", sha256="673f451a37a0fb0884aa5f739af3bd66b15ef614e8e5c532d81c91c8c0ad65c5")
    version("09.91.04d01", sha256="487d9653934ad3f81e1abe3ed0611bfdcacb77247fb601fbaca1194cdd3a9007")
    version("09.92.00d00", sha256="6f636aa889a8b2e3b926c003e96bec098d79bc025417a2ae281750eb9ce0d57c")
    version("09.89.01d01", sha256="028bec795bf7da56b3acdd689110fa47498e9b3c766306b96ed14076c012642a")
    version("09.81.00d00", sha256="ac58dad4ac13bb742179b509bf3aab35a8fcbecd79364444342ca2ab69664dd7")
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

    def patch(self):

        filter_file(
                'find_package\( jsoncpp REQUIRED \)',
                'pkg_check_modules( JSONCPP REQUIRED IMPORTED_TARGET jsoncpp )',
                'CMakeLists.txt',
            )
        filter_file(
                'jsoncpp',
                'PkgConfig::jsoncpp',
                'dunedataprep/DataPrep/WctTool/CMakeLists.txt',
            )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("dunecore")
    depends_on("jsonnet")
    depends_on("jsoncpp")
    depends_on("larwirecell")
    depends_on("wire-cell-toolkit")
    depends_on("larwirecell")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")
    depends_on("root+spectrum")
    
    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", "Bool:True"),
            self.define("WIRECELL_LIB", "%s" % self.spec["wire-cell-toolkit"].prefix.lib64)
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
