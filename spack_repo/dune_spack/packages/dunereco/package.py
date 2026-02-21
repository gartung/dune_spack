# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *
import os

class Dunereco(CMakePackage):
    """Dunereco"""

    git = "https://github.com/DUNE/dunereco"
    url = f"{git}/archive/v09_81_00d00.tar.gz"

    version("10.11.01d00", sha256="fb8868d47572189c071f4e0fb817eddcf3c5064eb1558bdc573147f9b76ec0d2")
    version("10.10.02d00", sha256="a7c2a656b88ec253cfbec107995825c36775ba3f449691dce228e6288aec0362")
    version("10.10.00d00", sha256="7c94cb5479fcb3503a3e8aaa9d6ad4a4c33a77f13af4d7576461648532dd124f")
    version("10.09.00d00", sha256="7fbd243b9d25f37489a5da5e2529891c6121a2fd4f6fd96039ec22800908b7de")
    version("10.08.01d00", sha256="c6af443bbd9ef67c4fc31ca1b80ccdafb62d7a256dd5ca0188a0809654dfa377")
    version("10.08.00d00", sha256="79cd268a1dbcbdb394e313ff09aa2c5febfea40a1fcd43d8acbc03a346d663bf")
    version("10.07.00d00", sha256="23167271ad932b9063f0cfa42611d9605a5c3c811ba17c9b023b72768ca8d552")
    version("10.06.00d01", sha256="4c48f715cfebb315c14f7cb6523b2d63617567b503347dd373b6a9f23c77b692")
    version("10.06.00d00", sha256="4eb8d0e8f4bab7dc5af96b15a8a6fd964b4d334fa9010d198e38f300bed16dea")
    version("10.08.02d00", sha256="1e2c283ceb0a59c6f907be327255b5fc5234a233e0a998d1b90e42fb4ec6e793")
    version("10.00.03d00", sha256="1c14a337a18b610accc24e5fb7816b029b7bde5e02f95e0684677e02847e3c5c")
    version("09.92.00d00", sha256="6bc62ced928ca36a5c9502bf7f9e6c341caeeaebf85614463a8c4fd676083248")
    version("09.91.04d01", sha256="e097a07840bc02cc30753cfbd47184d4e82318e7854765d603ba947fa16538b9")
    version("09.89.01d01", sha256="f9e352729f3c30496252de67f7f1e2b579dbcfd27076e31ee7d62a29d9260dd3")
    version("09.81.00d00", sha256="a7a64f3ed8fa5abd0f85998f065634c16c3db080123afde3faeecfb7dc2ddb46")
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

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("hep-hpc")
    #depends_on("python")
    depends_on("py-tensorflow")
    depends_on("py-torch")
    depends_on("triton")
    depends_on("protobuf")
    depends_on("larrecodnn")
    depends_on("dunecore")
    depends_on("larfinder")
    depends_on("nufinder")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")

    def patch(self):
        filter_file('#include "tensorflow/cc/saved_model/tag_constants.h"',
                    '#include "tensorflow/cc/saved_model/bundle_v2.h"\n#include "tensorflow/cc/saved_model/constants.h"\n#include "tensorflow/cc/saved_model/loader.h"',
                    "dunereco/CVN/tf/tf_bundle.cc",
                    )
        filter_file("{tensorflow::kSavedModelTagServe},",
                    "{},",
                    "dunereco/CVN/tf/tf_bundle.cc",
                    )
        filter_file('find_package\( Eigen3 REQUIRED \)',
                'find_package(protobuf REQUIRED)\nfind_package( Eigen3 REQUIRED )',
                "CMakeLists.txt"
                )
        filter_file('find_ups_product\( dunepdlegacy \)',
                'find_package(dunepdlegacy REQUIRED)\nfind_package(artdaq_core REQUIRED)',
                "CMakeLists.txt"
                )
    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("CMAKE_MODULE_PATH", "%s/Modules;%s/Modules" %
                       (self.spec['nufinder'].prefix, self.spec['larfinder'].prefix)),
        ] 
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set("TRITON_DIR", self.spec["triton"].prefix.lib)
        if os.path.exists(self.spec["py-torch"].prefix.lib64):
            spack_env.set("LIBTORCH_DIR", join_path(
                    self.spec["py-torch"].prefix.lib64,
                    "python%s/site-packages/torch"
                    % self.spec["python"].version.up_to(2),
                )
            )
        else:
            spack_env.set("LIBTORCH_DIR", join_path(
                    self.spec["py-torch"].prefix.lib,
                    "python%s/site-packages/torch"
                    % self.spec["python"].version.up_to(2),
                )
            )
        if os.path.exists(self.spec["protobuf"].prefix.lib64):
            spack_env.set("PROTOBUF_DIR", self.spec["protobuf"].prefix.lib64)
        else:
            spack_env.set("PROTOBUF_DIR", self.spec["protobuf"].prefix.lib)
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
