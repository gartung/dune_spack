# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class Duneexamples(CMakePackage):
    """Duneexamples"""

    git = "https://github.com/DUNE/duneexamples"
    url = f"{git}/archive/v09_81_00d00.tar.gz"

    version("10.22.00d00", sha256="a412e0407fc75b887d902f9c2e8747dd49dd57e487d4df8cfa2eb0fb0c85162e")
    version("10.21.02d00", sha256="7f1e84a743f69f8f741da6c62e708cc43fcb72f5361a901b78ffbb983968f1d2")
    version("10.21.01d00", sha256="fea1982f3760fdfed49bd2708a6c99afde261d28e58b56a82c64573b967b96ce")
    version("10.20.09d02", sha256="c4f85aaea7f413705169f4fcc6ca272d1473e3be66ee436c1e54c46f6182fdb3")
    version("10.20.03d01", sha256="6cd99020c3f6a6ee6de91a9f5fd6b202f4c84a3aa7de8147f2c1e6aea0a4a255")
    version("10.11.01d00", sha256="664e657465e4dfc9fdd63f9d029f4d15bdefa8a4794de65bfa8e11b01922bb5c")
    version("10.10.02d00", sha256="194b6e89a0bd3727d0a23f4ba54c87d9b4f02a6417131e3101ff809f848ba0de")
    version("10.10.00d00", sha256="fa2bdbb0715e83dc4a34646d4a39821552bd002ee2796e8849403d2b9703a21a")
    version("10.09.00d00", sha256="c3ff5ac8ad4e700fce9d45994077400dcb58076075a1c4ff8a04eb6eadf808e1")
    version("10.08.01d00", sha256="5837a9c0b46d88c10afd7fca6e578be8bddfe56d9ccb76100d87857e83a558a9")
    version("10.08.00d00", sha256="49c8f7db8faff3ac7a4a979d0127617089cb08dfa0153c5651aaa871cfdd056c")
    version("10.07.00d00", sha256="3190ab9cf85295059d9edc9b3aad80faab5b3be1d9724582985a183324b2a618")
    version("10.06.00d01", sha256="bd93cfb28a7e4bbf0dee1eb1e4b43953a89d57f6d5d285ed066bc3eafb9a2e3b")
    version("10.06.00d00", sha256="10671834502443b9b48e8c712457e8c5bcbf0ad4cccca8ec1ff79231b0a9614f")
    version("10.08.02d00", sha256="4a307d556c7b5d70a2a3f171c6b744405ef0134190cdcd9578c0fb35b1ee6c65")
    version("10.00.03d00", sha256="3e91fbcd0fbd6cae65f7f3e29784cfcf2ebeaeb3d5a2195964d432f9b5f7233e")
    version("09.92.00d00", sha256="e251ec860ae0c401cecc6c4ac985b203b625a8c1675d46a7a06309d7461598c4")
    version("09.91.04d01", sha256="6542ef796de3909ebbd23900690d7c918dd848e3ef3fa61bc383adc286dc4d17")
    version("09.89.01d01", sha256="fadad2d0d0f363bd9f52191ab0b6e0534f34b086098a16cafe9c93e5843cd99b")
    version("09.81.00d00", sha256="5ca163fe371aee48601d4ee63da447f26901a610d3bb175070aac113f93a5779")
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
    depends_on("art")
    depends_on("art-root-io")
    depends_on("canvas-root-io")
    depends_on("boost")
    depends_on("root")
    depends_on("dunecore")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ] 
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set("LD_LIBRARY_PATH", "%s/root" % self.spec["root"].prefix.lib)

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
