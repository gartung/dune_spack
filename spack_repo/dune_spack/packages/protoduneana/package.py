# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Protoduneana(CMakePackage, FnalGithubPackage):
    """Protoduneana"""

    repo = "DUNE/protoduneana"
    git = "https://github.com/%s" % repo
    version_patterns = ["v09_00_00d00", "09.14.19"]

    version("10_10_02d00", sha256="ab13f95e06ae6ed29b1f1a1424cb703f8cae53d0145b5a9f2e23af9b9208f071")
    version("10_10_00d00", sha256="e5d9c3bc53fa5240b744db3074d854ebdf9fbc72c6d2b4f891867d5aaa382de4")
    version("10_09_00d00", sha256="c17d4727e6f15ca09ffd05cba23e0f3cdc482b90c46c41e01803b005c078fd98")
    version("10_08_02d00", sha256="d06274906c50c37bf9fa4f38ecdfa5ce40e44b2df5f925112b78c0a5c8d836e3")
    version("10_08_01d00", sha256="caa2e54f238843fdd04025793661cea95e9cd926c401a6624a89e071fa3d25f6")
    version("10_08_00d00", sha256="c605e43e51fc7bdf16751eae2ab196e3368def90e825357c5862949f189c0a14")
    version("10_07_00d00", sha256="f944561cfda2697385b984fbd27d62397497439643987ea2ebf5c795c9ac5c28")
    version("10_06_00d01", sha256="182a018aa8780801991297158d329ee9f59a211eeae1840f3531f73cdb71d5ca")
    version("10_06_00d00", sha256="6d9306c2b2279e724d3a6e5e4759e0a204c1d1351430d951ee4bf51b89231881")
    version("10_00_03d00", sha256="e94a603f2469e9c46d140882c6b44d902eb2d8f7d81db0f1ffcaf50d052263da")
    version("09_92_00d00", sha256="27d7a23868279c61c4f63407e89fadec342eb19c4a8d55882cf8dc875d858055")
    version("09_91_04d01", sha256="1a2d908938a0f15cde2859aff2400f99760faa06f83228730d8dda910a8c6b12")
    version("09_89_01d01", sha256="50df6c272d564a6c8d158f229d500a25fff9fa262821a47876083bd3059df213")
    version("09_81_00d00", sha256="f490a31fe519217539ecd2e46194f70d179fa70a023a163d84e89d9e07f41695")
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

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("duneprototypes")
    depends_on("geant4reweight")
    depends_on("nusystematics")
    depends_on("systematicstools")
    depends_on("larfinder", type="build")
    depends_on("nufinder", type="build")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("CMAKE_MODULE_PATH", "%s/Modules;%s/Modules" %
                       (self.spec['nufinder'].prefix, self.spec['larfinder'].prefix)),
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
