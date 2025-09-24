# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Duneana(CMakePackage, FnalGithubPackage):
    """Duneana"""

    repo = "DUNE/duneana"
    git = "https://github.com/%s" % repo
    version_patterns = ["v09_00_00d00", "09.14.19"]

    version("10_10_02d00", sha256="a467832e5e93c0b855e8eb5bc49b06eba0a7d30fa3e92a3a76047d6d91d00e92")
    version("10_10_00d00", sha256="4aff66fb5d49e041d2f5f6a5d60a70e637df37f8290bde1d42c14c1d32d01551")
    version("10_09_00d00", sha256="db3e5b55984992bd516f4ee4722c72400116d9e4cd5b3704b416459e65e5af72")
    version("10_08_02d00", sha256="7f9faf6bff0926c9958eaa2f74db6410559598788f48c5f0117e313d12fccee4")
    version("10_08_01d00", sha256="4b9446e3e445c7af5a22884ed2e8d1da8060fdab91e9e8263361b698114c4224")
    version("10_08_00d00", sha256="6e561a2bc757e0655348154ddf51bb334efb054b9921a344ead8e38bf07d9220")
    version("10_07_00d00", sha256="7b951a81393156bef9ac871725b527f3ce21ed375f8131c2c627797a70b5e8ad")
    version("10_06_00d01", sha256="ab36fb0371e20f8d8b8e582328a2c9a36a95424312f2f466d05ee1e6ef2a1e5a")
    version("10_06_00d00", sha256="7e8dfa5e461f2cbdb7916f601a685e48c14adfafaca4cbaaee3a8797ce53501c")
    version("10_00_03d00", sha256="0db33f7a710b5a85c669d77db6a735fdbb354c70feb689051b080797d8d26712")
    version("09_92_00d00", sha256="fc0700c36f3334f70f7b3929b868bdf530a9f71f44dc205daa052d3755e4d08f")
    version("09_91_04d01", sha256="d8773061e20fc3577aee2bdff33e6ca4b8b4fb2b5298a3dd4369cae652ef9746")
    version("09_89_01d01", sha256="8769e2e2dbac6e6664150acced6e276a491d78463a5e30bcaff2412cb3208da7")
    version("09_81_00d00", sha256="8c1fc6758232a9b4ba7a39924ea372d8e2698404bf4778c9b209a35d8888dcf4")
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

    def patch(self):

        filter_file(
                r'find_package\( duneanaobj REQUIRED EXPORT \)',
                '',
                'CMakeLists.txt',
            )
        for f in ('WireAna','AnaTree','CAFMaker'):
            filter_file(
                     r'duneanaobj::[a-zA-Z0-9]*',
                     '',
                     f'duneana/{f}/CMakeLists.txt',
                 )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("duneanaobj")
    depends_on("dunereco")
    depends_on("nufinder")
    depends_on("larfinder")
    depends_on("py-tensorflow")
    #depends_on("python")
    depends_on("systematicstools")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")
    depends_on("duneopdet")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("CMAKE_MODULE_PATH", "%s/Modules;%s/Modules" %
                       (self.spec['nufinder'].prefix, self.spec['larfinder'].prefix)),
            self.define("CMAKE_CXX_FLAGS","-I%s" % self.spec['duneanaobj'].prefix.include),
        ] 
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set("TENSORFLOW_DIR",
                join_path(
                    self.spec["py-tensorflow"].prefix.lib,
                    "python%s/site-packages/tensorflow"
                    % self.spec["python"].version.up_to(2),
                )
        )
        spack_env.set(
            "TENSORFLOW_INC",
                join_path(
                    self.spec["py-tensorflow"].prefix.lib,
                    "python%s/site-packages/tensorflow/include"
                    % self.spec["python"].version.up_to(2),
                )
        )

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
