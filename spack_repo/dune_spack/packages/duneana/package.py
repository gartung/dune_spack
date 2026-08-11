# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *
import os

class Duneana(CMakePackage):
    """Duneana"""

    git = "https://github.com/DUNE/duneana"
    url = f"{git}/archive/v09_81_00d00.tar.gz"

    version("10.22.00d01", sha256="8f41a5f11df81f0e08ce5f29b4a701dbaeaada46a0701bb45bc2ff62f82b6470")
    version("10.22.00d00", sha256="1c5bfc5fd378a8e1616f59289cc1e8c6a44be0bd6e50935c008804bfdf02a502")
    version("10.21.02d00", sha256="12220ab5714396a7fd8b1d5942d9aca772a7ab7b6b10b8891a046ccaff160b8a")
    version("10.21.01d00", sha256="d4fa60a4ea67bf215b6cff271fe8eec23eb3ca61b456a2d68e5164165e954660")
    version("10.20.09d02", sha256="ee3734dec247403a51681b84156d2d0047a96a6651badaea95113af9aa85e091")
    version("10.20.03d01", sha256="7f304f1831b30d335d9d5157acef41aa12959a59b16890f7e47739714dd709f0")
    version("10.11.01d00", sha256="211d4cfce443077e5241ff6c06186ed54557c88a00546b2f7988fe457a9b7e2d")
    version("10.10.02d00", sha256="a467832e5e93c0b855e8eb5bc49b06eba0a7d30fa3e92a3a76047d6d91d00e92")
    version("10.10.00d00", sha256="4aff66fb5d49e041d2f5f6a5d60a70e637df37f8290bde1d42c14c1d32d01551")
    version("10.09.00d00", sha256="db3e5b55984992bd516f4ee4722c72400116d9e4cd5b3704b416459e65e5af72")
    version("10.08.02d00", sha256="7f9faf6bff0926c9958eaa2f74db6410559598788f48c5f0117e313d12fccee4")
    version("10.08.01d00", sha256="4b9446e3e445c7af5a22884ed2e8d1da8060fdab91e9e8263361b698114c4224")
    version("10.08.00d00", sha256="6e561a2bc757e0655348154ddf51bb334efb054b9921a344ead8e38bf07d9220")
    version("10.07.00d00", sha256="7b951a81393156bef9ac871725b527f3ce21ed375f8131c2c627797a70b5e8ad")
    version("10.06.00d01", sha256="ab36fb0371e20f8d8b8e582328a2c9a36a95424312f2f466d05ee1e6ef2a1e5a")
    version("10.06.00d00", sha256="7e8dfa5e461f2cbdb7916f601a685e48c14adfafaca4cbaaee3a8797ce53501c")
    version("10.00.03d00", sha256="0db33f7a710b5a85c669d77db6a735fdbb354c70feb689051b080797d8d26712")
    version("09.92.00d00", sha256="fc0700c36f3334f70f7b3929b868bdf530a9f71f44dc205daa052d3755e4d08f")
    version("09.91.04d01", sha256="d8773061e20fc3577aee2bdff33e6ca4b8b4fb2b5298a3dd4369cae652ef9746")
    version("09.89.01d01", sha256="8769e2e2dbac6e6664150acced6e276a491d78463a5e30bcaff2412cb3208da7")
    version("09.81.00d00", sha256="8c1fc6758232a9b4ba7a39924ea372d8e2698404bf4778c9b209a35d8888dcf4")
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
    patch('v09_92_00d00.patch', when='@09.92.00d00')

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
        filter_file(
                r"find_package\( larfinder REQUIRED \)",
                'find_package( larfinder REQUIRED )\nset(CMAKE_FIND_LIBRARY_SUFFIXES ".so", ".so.2")\nfind_package(TensorFlow REQUIRED)',
                "CMakeLists.txt"
                )
        filter_file(
                r"dunereco::CVN_func",
                "dunereco::CVN_func dunereco::RegCNNFunc duneanaobj_StandardRecord duneanaobj_StandardRecordFlat",
                "duneana/CAFMaker/CMakeLists.txt"
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
        if os.path.exists(self.spec["py-tensorflow"].prefix.lib64):
            spack_env.set("TENSORFLOW_DIR",
                join_path(
                    self.spec["py-tensorflow"].prefix.lib64,
                    "python%s/site-packages/tensorflow"
                    % self.spec["python"].version.up_to(2),
                )
            )
            spack_env.set(
            "TENSORFLOW_INC",
                join_path(
                    self.spec["py-tensorflow"].prefix.lib64,
                    "python%s/site-packages/tensorflow/include"
                    % self.spec["python"].version.up_to(2),
                )
            )
        else:
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
