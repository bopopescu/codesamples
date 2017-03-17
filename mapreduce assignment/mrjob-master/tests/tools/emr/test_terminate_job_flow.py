# Copyright 2009-2012 Yelp
# Copyright 2015 Yelp
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Test the job flow termination tool"""
from mrjob.emr import EMRJobRunner
from mrjob.patched_boto import patched_describe_cluster
from mrjob.tools.emr.terminate_job_flow import main as terminate_main
from mrjob.tools.emr.terminate_job_flow import make_option_parser

from tests.tools.emr import ToolTestCase


class TerminateToolTestCase(ToolTestCase):

    def test_make_option_parser(self):
        make_option_parser()
        self.assertEqual(True, True)

    def test_terminate_job_flow(self):
        cluster_id = self.make_cluster(pool_emr_job_flows=True)
        self.monkey_patch_argv('--quiet', '--no-conf', 'j-MOCKCLUSTER0')

        terminate_main()

        emr_conn = EMRJobRunner(conf_paths=[]).make_emr_conn()
        cluster = patched_describe_cluster(emr_conn, cluster_id)
        self.assertEqual(cluster.status.state, 'TERMINATED')
