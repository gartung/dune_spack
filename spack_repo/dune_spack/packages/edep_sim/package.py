# This package.py written by Liam O'Sullivan <liam.osullivan@uni-mainz.de>
# For reasons™, explicitly including root and geant4 as dependencies
# causes the build to fail (missing blas or whatevs).
# If you spack load root and geant4 it builds fine though.

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *

class EdepSim(CMakePackage):
    """edep-sim -- an energy deposit simulation based on Geant4"""

    license("MIT")
    homepage = "https://github.com/ClarkMcGrew/edep-sim"
    git = "https://github.com/ClarkMcGrew/edep-sim.git"
    url = "https://github.com/ClarkMcGrew/edep-sim/archive/refs/tags/3.2.0.tar.gz"

    executables = ["^edep-sim$", "^edep-disp$"]

    maintainers("LiamOS") # Maintainer on FNAL SPack, maintainer of edep-sim is Clark McGrew

    version("master", branch="master")
    version("develop", branch="master")
    # Actual releases:
    version("3.2.0", sha256="119a5b274601cf721d4f954dee8191e089f157b7b9feb97b10e6a1de399f7771")
    version("3.1.0", sha256="7ac82d4ef30259b98b82b7d6bca4e556b5c1f65a4e7b9f7bd24df2304ebdd97e")
    version("3.0.0", sha256="b91343f986ecb66505de813c6221a74c42d3635c4bb9bfe947cf6a1ac397bc15")
    # We don't really need these ones though, surely...
    #version("2.0.1", sha256="")
    #version("2.0.0", sha256="")
    #version("1.0.0", sha256="")
    #version("0.1.0", sha256="")
    #version("0.0.2", sha256="")
    #version("0.0.1", sha256="")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("cmake", type="build")
    depends_on("nlohmann-json")
    #depends_on("root") # TODO: In theory it does depend on ROOT and Geant4, but fails when they're enabled here
    #depends_on("geant4")

    def setup_run_environment(self, env): 
        env.set("EDEP_ROOT", self.prefix)
        env.set("EDEPSIM_LIB", self.prefix.lib)
        env.set("EDEPSIM_INC", self.prefix.include)


