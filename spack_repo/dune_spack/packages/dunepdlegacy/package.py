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
    version_patterns = ["09_00_00", "09.14.19"]

    version("1_01_05", sha256="60876ea0041c6054dba31789806d248bb9a2e74eec76bb90ae9711b6c8b86705")
    version("1_01_04", sha256="9662e6c2b3e7d4abc2d0e45ac249251359d6595e0a757ebb965521a9bcb043da")
    version("1_01_00", sha256="926130733ed28753ff637e52b120dc4ee669cf0a769e0d8f7049693670ee907a")
    version("develop", branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch('v1_01_05.patch', when='@1_01_05')
    patch('v09_81_00d00.patch', when='@1_01_00')

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

