# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *

class PyMergeUtils(PythonPackage):
    """DUNE file merging tools"""

    homepage = "https://github.com/DUNE/merge-utils"
    git = "https://github.com/DUNE/merge-utils"
    url = "https://github.com/DUNE/merge-utils/archive/v1.0.2.tar.gz"

    maintainers("vhewes")
    license("Apache-2.0", checked_by="vhewes")

    version("1.0.2", sha256="26ffd73fc7bf81a37d5bf9725974992d63712d251207053b5d3ae671aabf75ed")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-hatchling", type="build")
    depends_on("py-tomli", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
