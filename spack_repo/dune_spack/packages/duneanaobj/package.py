# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class Duneanaobj(CMakePackage):
    """Duneanaobj"""

    git = "https://github.com/DUNE/duneanaobj"
    url = f"{git}/archive/v03_03_00.tar.gz"

    version("04.01.00", sha256="7e1eb6ac797b98718fbf33acad1cf29904939d83dd1d1e6068925e08f8061a00")
    version("04.00.00", sha256="4425c906ba117e3823c479feb2c5ba168707c157df063f7c5aded2f77e16d595")
    version("03.15.00", sha256="d05a9ce506597d954bee6e62138336d8cfcbfc249e0ecb6874638aaeb1895d4c")
    version("03.12.00", sha256="32a0134bdfd4e7c41ae04bf8d4ea137175cf49fbe9566379f0237f033ca2228f")
    version("03.11.00", sha256="b386cb3b448b38d880bb64457cc15434fd5d872168a0287712edf23544e70550")
    version("03.10.00", sha256="35f025b77b3f5c6cc4666d1bbd04b2ff8f837a51670bbe5c0d80a7e3145164d8")
    version("03.09.00", sha256="c1bc56a25d8280349292363e74b3d3f32424f54daa5b0554a8fd94b72438750f")
    version("03.08.00", sha256="89581845fc12a156e0541e2d3eef866efc631794f03f255731367023b5fd50eb")
    version("03.07.00", sha256="2f8ef24312520ab362cf06a5d2264f71ce26ae7974d32e81ccca7149de81da0c")
    version("03.06.01", sha256="ad0647930712d5680c77c03f8d0af3a9e44f222c15c753d631ac8752ddf07e67")
    version("03.06.00", sha256="28be5276666146e88501fe73df6907fde9552969824e8f7dc8115598c914d5da")
    version("03.05.00", sha256="00e227bccf02ef0c8faa5931b39b6f6c65ff88563e2c328e35e1c3109bcf8c63")
    version("03.04.00", sha256="3cfc96a0aae4fab7e51f501b071d9b9bfe32cfaa9bd288a3a9b159fde18b4f3b")
    version("03.03.00", sha256="4d00eaa72997b8ff6a6f59e9eedadd11806ab06c83d28064d523dfa9f00e15e5")
    version("develop", branch="main", get_full_repo=True)

    def url_for_version(self, version):
        return f"{self.git}/archive/v{version.underscored}.tar.gz"

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch('main-spack.patch', when="@03.10.00")
    patch('v03_06_01.patch', when="@03.06.01")
    patch('v09_81_00d00.patch', when="@03.03.00")
    patch('v09_93_00d00.patch', when="@03.06.00")

    def patch(self):
        filter_file('^cet_cmake_config','#cet_cmake_config', 'CMakeLists.txt')

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("root")
    depends_on("canvas-root-io")
    depends_on("py-srproxy@00.43:")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")
    depends_on("py-srproxy")
    
    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("CMAKE_BUILD_DIR", self.prefix),
            self.define("CMAKE_INSTALL_INCLUDEDIR", self.prefix.include),
        ] 
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set("LD_LIBRARY_PATH", "%s/root" % self.spec["root"].prefix.lib)
        spack_env.set("ROOT_INC", "%s" % self.spec["root"].prefix.include)
        spack_env.set("DUNEANAOBJ_DIR", "%s" % os.path.realpath(self.stage.source_path))
        spack_env.set("SRPROXY_INC", "%s" % os.path.realpath(self.build_directory))
        spack_env.set("UPS_DIR", "%s" % os.path.realpath(self.stage.source_path))

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
