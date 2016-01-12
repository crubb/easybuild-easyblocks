##
# Copyright 2009-2015 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
Support for building and installing picard, implemented as an easyblock.

@author: Stijn De Weirdt (Ghent University)
@author: Dries Verdegem (Ghent University)
@author: Kenneth Hoste (Ghent University)
@author: Pieter De Baets (Ghent University)
@author: Jens Timmerman (Ghent University)
"""

import os
import re
import shutil

from distutils.version import LooseVersion
from easybuild.framework.easyblock import EasyBlock
from easybuild.tools.build_log import EasyBuildError


class EB_picard(EasyBlock):
    """Support for building and installing picard."""

    def configure_step(self):
        """No configure step for picard"""
        pass

    def build_step(self):
        """No build step for picard"""
        pass

    def install_step(self):
        """Install picard by copying required files"""
        # recent version may contain more than just the picard-tools subdirectory
        picard_tools_dir = 'picard-tools-%s' % self.version
        if not re.search("%s/?$" % picard_tools_dir, self.cfg['start_dir']):
            self.cfg['start_dir'] = os.path.join(self.cfg['start_dir'], picard_tools_dir)
            if not os.path.exists(self.cfg['start_dir']):
                raise EasyBuildError("Path %s to copy files from doesn't exist.", self.cfg['start_dir'])

        for jar in os.listdir(self.cfg['start_dir']):
            src = os.path.join(self.cfg['start_dir'], jar)
            dst = os.path.join(self.installdir, jar)
            try:
                shutil.copy2(src, dst)
                self.log.info("Successfully copied %s to %s" % (src, dst))
            except OSError, err:
                raise EasyBuildError("Failed to copy %s to %s (%s)", src, dst, err)

    def sanity_check_step(self):
        """Custom sanity check for picard"""
        """All versions prior to 1.124 have these jar files"""
        if LooseVersion(self.version) < LooseVersion('1.124'):
            jar_files = [
                'picard-%s' % self.version,
                
                'AddOrReplaceReadGroups',
                'BamIndexStats',
                'BamToBfq',
                'BuildBamIndex',
                'CalculateHsMetrics',
                'CheckIlluminaDirectory',
                'CleanSam',
                'CollectAlignmentSummaryMetrics',
                'CollectGcBiasMetrics',
                'CollectInsertSizeMetrics',
                'CollectMultipleMetrics',
                'CollectRnaSeqMetrics',
                'CollectTargetedPcrMetrics',
                'CompareSAMs',
                'CreateSequenceDictionary',
                'DownsampleSam',
                'EstimateLibraryComplexity',
                'ExtractIlluminaBarcodes',
                'ExtractSequences',
                'FastqToSam',
                'FilterSamReads',
                'FixMateInformation',
                'IlluminaBasecallsToFastq',
                'IlluminaBasecallsToSam',
                'IntervalListTools',
                'MakeSitesOnlyVcf',
                'MarkDuplicates',
                'MarkIlluminaAdapters',
                'MeanQualityByCycle',
                'MergeBamAlignment',
                'MergeSamFiles',
                'MergeVcfs',
                'NormalizeFasta',
                'QualityScoreDistribution',
                'ReorderSam',
                'ReplaceSamHeader',
                'RevertSam',
                'SamFormatConverter',
                'SamToFastq',
                'SortSam',
                'SplitVcfs',
                'ValidateSamFile',
                'VcfFormatConverter',
                'ViewSam',
            ]
            
            """The following jar files were only available in the specified versions of picard"""
            if LooseVersion(self.version) >= LooseVersion('1.100') and LooseVersion(self.version) < LooseVersion('1.114'):
                jar_files += [
                    'sam-%s' % self.version,
                    'tribble-%s' % self.version,
                    'variant-%s' % self.version,
                ]
            if LooseVersion(self.version) >= LooseVersion('1.109'):
                jar_files += [
                    'RevertOriginalBaseQualitiesAndAddMateCigar',
                ]
            if LooseVersion(self.version) >= LooseVersion('1.111'):
                jar_files += [
                    'GatherBamFiles',
                ]
            if LooseVersion(self.version) >= LooseVersion('1.113'):
                jar_files += [
                    'AddCommentsToBam',
                    'CollectWgsMetrics',
                ]
            if LooseVersion(self.version) >= LooseVersion('1.114'):
                jar_files += [
                    'htsjdk-%s' % self.version,
                ]
            if LooseVersion(self.version) >= LooseVersion('1.119'):
                jar_files += [
                    'CollectBaseDistributionByCycle',
                    'FifoBuffer',
                ]
            if LooseVersion(self.version) >= LooseVersion('1.120'):
                jar_files += [
                    'BedToIntervalList',
                ]
            if LooseVersion(self.version) >= LooseVersion('1.121'):
                jar_files += [
                    'SortVcf',
                ]
            if LooseVersion(self.version) >= LooseVersion('1.122'):
                jar_files += [
                    'CollectHiSeqXPfFailMetrics',
                    'GenotypeConcordance',
                    'MarkDuplicatesWithMateCigar',
                    'UpdateVcfSequenceDictionary',
                    'VcfToIntervalList',
                ]
        else:
            """Starting with v1.124 a major structural change was made to picard"""
            """All versions >= 1.124 now only have these jar files"""
            jar_files = [
                'htsjdk-%s' % self.version,
                'picard',
                'picard-lib'
            ]
        
        custom_paths = {
            'files': ["%s.jar" % (x) for x in jar_files],
            'dirs': [],
        }

        super(EB_picard, self).sanity_check_step(custom_paths=custom_paths)

    def make_module_extra(self):
        """Add module entries specific to picard"""
        txt = super(EB_picard, self).make_module_extra()
        txt += self.module_generator.prepend_paths('PATH', '')
        return txt
