# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *

class Duneopdet(CMakePackage):
    """Duneopdet"""

    git = "https://github.com/DUNE/duneopdet"
    url = f"{git}/archive/v09_81_00d00.tar.gz"

    version("10.22.00d00", sha256="e11c4525e4cfe3d4fd18f33a03362a062bf864297b92b08cadeea91dd670e747")
    version("10.21.02d00", sha256="2f2f47ddc23f9ebfbcc0f0840f70760a0cadbe37c71db4abf8d89a4d02d9b85a")
    version("10.21.01d00", sha256="e3a0b42c1b6a9230afb7630440ec9de09a50a34f878df7461c017425d1b1225b")
    version("10.20.09d02", sha256="203a2a4359cda12dea387037e7135335e2309f41111b475c6a989e2986e72567")
    version("10.20.03d01", sha256="9a9af7bba2b4fa63f76abf87e41474aea9a1f63c6f9a579e3644402df1fb906c")
    version("10.11.01d00", sha256="5f312ed45baef06947b903a900fe0e296fd8179396033fc345fe29402d58bede")
    version("10.10.02d00", sha256="7d9ca71730dfff92e71f4944f4773b707e9d3cf25e0e39633117d1cccfcd73e7")
    version("10.10.00d00", sha256="57ebcaa2c6bde3fa92b6d6d7a2055357b4159fa16763d9442aa779413ae8da03")
    version("10.09.00d00", sha256="5400fd1965fe8fb8e7b593df211e5bdb58304ce4666cf3a64e84323c1cad8571")
    version("10.08.02d00", sha256="c6913cb4f58faea4c279300ea41f51bf51e2c822c2fbd2b5daad70dd97648109")
    version("10.08.01d00", sha256="c07a292819fbbfc355b6ebf07b20e31229b52ab447bb63623ed5581d3828d299")
    version("10.08.00d00", sha256="11289d52d4dba384159759b877bccf2fee767a9797e58a47c49d04838985e528")
    version("10.07.00d00", sha256="906ed91786cad969b8a284853d0c5255757b7f4dda70213c92d5db38a60082fd")
    version("10.06.00d01", sha256="f296d7e723f61cc1ec4494a11e9f1e4acc42547ecffe89f849f0b4de4487109f")
    version("10.06.00d00", sha256="664b5ae1194ab24649ffa539b88345d636b0c9ce549545b1d13233c96a7d3d2a")
    version("10.00.03d00", sha256="b3b62f15d20a2db3389e1cdd4480280316f87ee915a81fd4f0d050fc9e202868")
    version("09.92.00d00", sha256="6003147a6b8a0d943a9f11ceebc4ab2fbac48b9041ad78f560a7bd3ae27b4929")
    version("09.91.04d01", sha256="de57b818cad3c7fea523666d0b2da423d05524a90e8892909c347eef830eaaa2")
    version("09.89.01d01", sha256="d39bf58d4dedf985f51d8b2d272354047603fc520145b282d17c85cd7877fdbe")
    version("09.81.00d00", sha256="ea4e39071507f9f1697ba2251481d2ff9396238a33ee38c0fe68070c2c1a9750")
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

    patch('v10_11_01d00.patch', when='@10.11.01d00',
          sha256='6c9554c58ac7bbff14475dcfa756bd1369ffd8298d85d03fa0e1b27e71cb9252')
    patch('v10_00_03d00.patch', when='@10.00.03d00')
    patch('v09_81_00d00.patch', when='@09.81.00d00')

    def patch(self):
        filter_file("LANGUAGES CXX", "LANGUAGES CXX C", "CMakeLists.txt")
        filter_file(
                r'find_package\( dunecore REQUIRED EXPORT \)',
                'find_package( dunecore REQUIRED EXPORT )\nfind_package( duneprototypes REQUIRED EXPORT)',
                'CMakeLists.txt'
            )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("dunecore")
    depends_on("duneprototypes")
    depends_on("nlohmann-json")
    depends_on("larfinder")
    depends_on("py-tensorflow")
    depends_on("protobuf")
    depends_on("grpc")
    depends_on("larsimdnn")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
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
            spack_env.set("TENSORFLOW_INC",
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
            spack_env.set( "TENSORFLOW_INC",
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
