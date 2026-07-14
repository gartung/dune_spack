# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *
import glob

class DunePardata(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.example.com"
    url = "https://scisoft.fnal.gov/scisoft/packages/dune_pardata/v01_84_00/dune_pardata-01.84.00-noarch.tar.bz2"

    license("UNKNOWN", checked_by="github_user1")

    version("01.84.00", sha256="49e0ceb3538c9a0a270363b90adc230523267744d064fa4c59f271c6c50273d1")

    def url_for_version(self, version):
        url = "https://scisoft.fnal.gov/scisoft/packages/dune_pardata/v{0}/dune_pardata-{1}-noarch.tar.bz2"
        return url.format(version.underscored, version.dotted)

    def install(self, spec, prefix):
        src = glob.glob("%s/v*[0-9]" % self.stage.source_path)[0]
        install_tree(src, prefix)

    def setup_run_environment(self, env):
        env.set("DUNE_PARDATA_VERSION", "v%s" % self.version.underscored)
        env.prepend_path("FW_SEARCH_PATH","%s" % self.prefix )
        env.prepend_path("FW_SEARCH_PATH", "%s/FieldResponse" % self.prefix )
        env.prepend_path("FW_SEARCH_PATH", "%s/ADCStuckCodeProbabilities35t" % self.prefix )
        env.prepend_path("FW_SEARCH_PATH", "%s/FieldResponse" % self.prefix )
        env.prepend_path("FW_SEARCH_PATH", "%s/GenieFluxFiles" % self.prefix )
        env.prepend_path("FW_SEARCH_PATH", "%s/OnlineChannelMaps35t" % self.prefix )
        env.prepend_path("FW_SEARCH_PATH", "%s/PhotonPropagation" % self.prefix )
        env.prepend_path("FW_SEARCH_PATH", "%s/PhotonPropagation/LibraryData" % self.prefix )
        env.prepend_path("FW_SEARCH_PATH", "%s/SpaceCharge35t" % self.prefix )

        env.set("WIRECELL_PATH", "%s/WireCellData" % self.prefix )
