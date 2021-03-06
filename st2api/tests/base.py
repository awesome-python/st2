# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    import simplejson as json
except ImportError:
    import json

from st2api import app
from st2tests.api import BaseFunctionalTest
from st2tests.api import BaseAPIControllerWithRBACTestCase


class FunctionalTest(BaseFunctionalTest):
    app_module = app


class APIControllerWithRBACTestCase(BaseAPIControllerWithRBACTestCase):
    app_module = app


class FakeResponse(object):

    def __init__(self, text, status_code, reason):
        self.text = text
        self.status_code = status_code
        self.reason = reason

    def json(self):
        return json.loads(self.text)

    def raise_for_status(self):
        raise Exception(self.reason)


class BaseActionExecutionControllerTestCase(object):

    @staticmethod
    def _get_actionexecution_id(resp):
        return resp.json['id']

    @staticmethod
    def _get_liveaction_id(resp):
        return resp.json['liveaction']['id']

    def _do_get_one(self, actionexecution_id, *args, **kwargs):
        return self.app.get('/v1/executions/%s' % actionexecution_id, *args, **kwargs)

    def _do_post(self, liveaction, *args, **kwargs):
        return self.app.post_json('/v1/executions', liveaction, *args, **kwargs)

    def _do_delete(self, actionexecution_id, expect_errors=False):
        return self.app.delete('/v1/executions/%s' % actionexecution_id,
                               expect_errors=expect_errors)

    def _do_put(self, actionexecution_id, updates, *args, **kwargs):
        return self.app.put_json('/v1/executions/%s' % actionexecution_id, updates, *args, **kwargs)
