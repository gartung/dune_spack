# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Duneprototypes(CMakePackage, FnalGithubPackage):
    """Duneprototypes"""

    repo = "DUNE/duneprototypes"
    version_patterns = ["09_00_00d00", "09.14.19"]

    version("10_08_02d00", sha256="650e67104dba0a42d283c3afac2d509adab821762cc2d9a41fa4a584e6272632")
    version("10_00_03d00", sha256="c3ed09c70ce39df44edc506680b7eb1eac7b562a05e7d703284a915525af0e49")
    version("09_92_00d00", sha256="536429aa8cfb94f54cd790609128fef311a8ef9b92449e4c79a2e4459891f272")
    version("09_89_01d01", sha256="140a6a20b2ddabd70572172d57c348ea618d6b0a1bfe0ade29c767842e540fe2")
    version("09_81_00d00", sha256="99a3e4eb98bfb9c7e7adeb3eb295332b71008c5bf6749587413ec97688532c85")
    version("develop", branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch('v09_81_00d00.patch', when='@09_81_00d00')

    def patch(self):
        # clean out vestigial dunesim, duneprototypes references
        filter_file(
            '#include "dunesim/DetSim/Service/DPhaseSimChannelExtractService.h"',
            '',
            'duneprototypes/Protodune/dualphase/Purity_module.cc'
            )
        filter_file(
                'r#include "duneopdet.*',
                '',
                'duneprototypes/Protodune/singlephase/NearlineMonitor/PlotOpticalDetails_module.cc',
            )
        filter_file(
            'dunesim::DetSim',
            '',
            'duneprototypes/Protodune/dualphase/CMakeLists.txt'
            )
        filter_file(
            'find_package\\( (dunesim|duneopdet) REQUIRED EXPORT \\)',
            '',
            'CMakeLists.txt'
            )
        filter_file(
                'duneopdet::OpticalDetector',
                '',
                'duneprototypes/Protodune/singlephase/NearlineMonitor/CMakeLists.txt',
            )
        filter_file(
                '#include "duneopdet.*',
                '',
                'duneprototypes/Protodune/singlephase/NearlineMonitor/PlotOpticalDetails_module.cc',
            )

        for cmf in (
                'CMakeLists.txt',
                'duneprototypes/Coldbox/hd/CMakeLists.txt',
                'duneprototypes/Coldbox/vd/CMakeLists.txt',
                'duneprototypes/Iceberg/RawDecoding/CMakeLists.txt',
                'duneprototypes/Protodune/dualphase/CMakeLists.txt',
                'duneprototypes/Protodune/dualphase/Purity_module.cc',
                'duneprototypes/Protodune/hd/RawDecoding/CMakeLists.txt',
                'duneprototypes/Protodune/singlephase/NearlineMonitor/CMakeLists.txt',
                'duneprototypes/Protodune/singlephase/NearlineMonitor/PlotOpticalDetails_module.cc',
                'duneprototypes/Protodune/singlephase/PhotonDetectors/CMakeLists.txt',
                'duneprototypes/Protodune/singlephase/RawDecoding/CMakeLists.txt',
                'duneprototypes/Protodune/spsbsm/SPSFilter/CMakeLists.txt',
                'duneprototypes/Protodune/spsbsm/SPSProducer/CMakeLists.txt',
                'duneprototypes/Protodune/vd/RawDecoding/CMakeLists.txt'):
            filter_file(
                'artdaq_core',
                'artdaq-core',
                cmf
                )
            filter_file(
                'artdaq.core::artdaq.core_(Utilities|Data)',
                'artdaq-core::\\1',
                cmf
                )


    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")
    depends_on("dunecalib")
    # makes a cycle, may not actually be used(!)
    #depends_on("dunesim")
    #depends_on("duneopdet")
    depends_on("nuevdb")


    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
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
