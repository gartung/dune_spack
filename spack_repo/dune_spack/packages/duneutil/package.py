# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Duneutil(CMakePackage, FnalGithubPackage):
    """Duneutil"""

    repo = "DUNE/duneutil"
    git = "https://github.com/%s" % repo
    version_patterns = ["v09_00_00d00", "09.14.19"]

    version("10_10_02d00", sha256="b0ed3a45d5f3cdd30c72cf470106595c3a81a3514086085baa6d0ea8ae587184")
    version("10_10_00d00", sha256="b2c648cc6100c267ea9bf3f4a3ca0f938dbbb7bfb6c91fbd941c4f8d271dfab0")
    version("10_09_00d00", sha256="5259e670c80c7c0c5b7dc60143b13bea4a4e5c300120fb50e08124e7652a2b2f")
    version("10_08_02d00", sha256="41666f3e06f5f5b9c36ac8c38b7578fd38a92f6fb16b94196c0e58da8af462b9")
    version("10_08_01d00", sha256="86919e8aa4a3b60890476a3134ba971cc898135b54a4e2b55f99f7aa9a15fa5a")
    version("10_08_00d00", sha256="3cae45dc25638a807a945bdb60437db7087c29b9a211832dd474a61191a15d53")
    version("10_07_00d00", sha256="aec1908f425ba2dce9d212bde799797e030e7081e0068b9bcd090dd1a5ea2914")
    version("10_06_00d01", sha256="31c9e8957f91e5f81c57950a15f5a3d50ff3b0faae4fa50985458d9feb7b893a")
    version("10_06_00d00", sha256="17aeffb621f67bf9f7c1e3a5f57255028b229504c23877edc78246e636a7f856")
    version("10_00_03d00", sha256="883877e913a99590a05f18d2d212cbf63d6ae3e574f094aeda4d72887c700d1d")
    version("09_92_00d00", sha256="fc0cb55678361a3488a17769cfcbe101ca1f513e8748261beb67caf86fb3974b")
    version("09_91_04d01", sha256="a10b60ecf36d087935fe54d6800f846ba46904f903ec1c3cbda139e9bc9c365f")
    version("09_89_01d01", sha256="e7f451fb6409afb261d5ad8b1a4381e7410db338dd2c601f688cda6164f5492f")
    version("09_81_00d00", sha256="3cd857e366c7ecf1648f0f7aa76c2821ba25fe8b8d702ff47e2d7291d006a3bf")
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

    patch('v09_81_00d00.patch', when='@9_81_00d00')

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("art-root-io")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ] 
        return args

