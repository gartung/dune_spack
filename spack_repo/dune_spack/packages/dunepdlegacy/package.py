# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Dunepdlegacy(CMakePackage, FnalGithubPackage):
    """Dunepdlegacy"""

    repo = "DUNE/dunepdlegacy"
    git = "https://github.com/%s" % repo
    version_patterns = ["v09_00_00", "09.14.19"]

    version("1_01_05", sha256="60876ea0041c6054dba31789806d248bb9a2e74eec76bb90ae9711b6c8b86705")
    version("1_01_04", sha256="9662e6c2b3e7d4abc2d0e45ac249251359d6595e0a757ebb965521a9bcb043da")
    version("1_01_00", sha256="926130733ed28753ff637e52b120dc4ee669cf0a769e0d8f7049693670ee907a")
    version("1_01_03", sha256="a15cf2cfa0d7fceb299bd195f34c452a12d21122ff501c42654a0f495de56912")
    version("1_01_02", sha256="975188592fe6e17c66e907438e9ead8f5b4290bff8fdcf1115217001c0cbddb6")
    version("1_01_01", sha256="b6826ca4df2df1aa254a2b0e44f658c5c785e17acc8b9ee7410d97d712744ff2")
    version("1_00_03", sha256="79dddb2e6d53d277367744bb222f13fcb4f30801f954a3465d2240f5ede4adac")
    version("1_00_02", sha256="a961b82fbff90b964cd58ee45157d9e0fc9faa2b9a6407698c0386136e667d2e")
    version("1_00_01", sha256="16a6da7419792b6446c61a8958cc19aa8f5438b5d6b33853e94806417cf27860")
    version("1_00_00", sha256="6ebd9bef3e6fdba018dc2d45c7ec62dd754375fc99367dade0e668f844624423")

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

    patch('v1_01_05.patch', when='@1_01_05')
    patch('v09_81_00d00.patch', when='@1_01_00')

    @when('^artdaq-core@v4_00_00:')
    def patch(self):
        filter_file(
                "artdaq_core",
                "artdaq-core",
                "CMakeLists.txt"
                )
        filter_file(
                "artdaq_core",
                "artdaq-core",
                "dunepdlegacy/Overlays/CMakeLists.txt"
                )
        filter_file(
                "artdaq-core::artdaq-core_Data",
                "artdaq-core::Data",
                "dunepdlegacy/Overlays/CMakeLists.txt"
                )
        filter_file(
                "artdaq-core::artdaq-core_Utilities",
                "artdaq-core::Utilities",
                "dunepdlegacy/Overlays/CMakeLists.txt"
                )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("gallery")
    depends_on("art")
    depends_on("artdaq-core")
    depends_on("cetlib")
    depends_on("nufinder")
    depends_on("messagefacility")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ] 
        return args

