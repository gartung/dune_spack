# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package
from spack.package import *


class Dunedetdataformats(Package):
    """Dunedetdataformats"""
    git = "https://github.com/DUNE/dunedetdataformats"
    url = f"{git}/archive/v4_4_5.tar.gz"

    version("4.4.5", sha256="82e69cb0397d910f53664a8276766230489440f37001a4980520b13c7e23b4fc")
    version("4.4.4", sha256="ae4f18a4f3c09f503a0dca5373fb9b08ad04bfc4ead323605121ff3ec76a22df")
    version("4.4.0", sha256="1312f255869f6b021df8c9a7885925192e62094f46808d3b7f6bd99d6efc0a20")
    version("4.1.0", sha256="479de5f1392b6303c258bced663b9aebd22ccd4a0aab2dd2910a9e1e295808b8")
    version("develop", branch="main", get_full_repo=True)

    def url_for_version(self, version):
        return f"{self.git}/archive/v{version.underscored}.tar.gz"

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, self.spec.prefix)
