# Copyright (c) 2019, IRIS-HEP
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from flask import current_app as app


def add_routes(api, transformer_manager, rabbit_mq_adaptor,
               object_store, elasticsearch_adapter, code_gen_service,
               lookup_result_processor, docker_repo_adapter):
    from servicex.resources.submit_transformation_request import SubmitTransformationRequest
    from servicex.resources.transform_start import TransformStart
    from servicex.resources.transform_status \
        import TransformationStatus, TransformationStatusInternal
    from servicex.resources.file_transform_status import FileTransformationStatus
    from servicex.resources.all_transformation_requests import AllTransformationRequests
    from servicex.resources.transformation_request import TransformationRequest
    from servicex.resources.add_file_to_dataset import AddFileToDataset
    from servicex.resources.preflight_check import PreflightCheck
    from servicex.resources.fileset_complete import FilesetComplete
    from servicex.resources.transformer_file_complete import TransformerFileComplete
    from servicex.resources.transform_errors import TransformErrors
    from servicex.resources.info import Info

    from servicex.resources.users.all_users import AllUsers
    from servicex.resources.users.token_refresh import TokenRefresh
    from servicex.resources.users.accept_user import AcceptUser
    from servicex.resources.users.delete_user import DeleteUser
    from servicex.resources.users.pending_users import PendingUsers
    from servicex.resources.users.slack_interaction import SlackInteraction

    from servicex.web import home, sign_in, sign_out, auth_callback, \
        view_profile, edit_profile, api_token, servicex_file

    # Must be its own module to allow patching
    from servicex.web.create_profile import create_profile

    SubmitTransformationRequest.make_api(rabbitmq_adaptor=rabbit_mq_adaptor,
                                         object_store=object_store,
                                         elasticsearch_adapter=elasticsearch_adapter,
                                         code_gen_service=code_gen_service,
                                         lookup_result_processor=lookup_result_processor,
                                         docker_repo_adapter=docker_repo_adapter)

    # Web Frontend Routes
    app.add_url_rule('/', 'home', home)
    app.add_url_rule('/sign-in', 'sign_in', sign_in)
    app.add_url_rule('/sign-out', 'sign_out', sign_out)
    app.add_url_rule('/auth-callback', 'auth_callback', auth_callback)
    app.add_url_rule('/api-token', 'api_token', api_token)
    app.add_url_rule('/.servicex', 'servicex-file', servicex_file)
    app.add_url_rule('/profile', 'profile', view_profile)
    app.add_url_rule('/profile/new', 'create_profile', create_profile,
                     methods=['GET', 'POST'])
    app.add_url_rule('/profile/edit', 'edit_profile', edit_profile,
                     methods=['GET', 'POST'])

    # User management and Authentication Endpoints
    api.add_resource(TokenRefresh, '/token/refresh')
    api.add_resource(AllUsers, '/users')
    api.add_resource(AcceptUser, '/accept')
    api.add_resource(DeleteUser, '/users/<user_id>')
    api.add_resource(PendingUsers, '/pending')
    api.add_resource(SlackInteraction, '/slack')

    # Client public endpoints
    api.add_resource(Info, '/servicex')
    api.add_resource(SubmitTransformationRequest, '/servicex/transformation')

    api.add_resource(AllTransformationRequests, '/servicex/transformation')
    api.add_resource(TransformationRequest,
                     '/servicex/transformation/<string:request_id>')

    api.add_resource(TransformationStatus,
                     '/servicex/transformation/<string:request_id>/status')

    api.add_resource(TransformErrors,
                     '/servicex/transformation/<string:request_id>/errors')

    # Internal service endpoints
    api.add_resource(TransformationStatusInternal,
                     '/servicex/internal/transformation/<string:request_id>/status')

    AddFileToDataset.make_api(lookup_result_processor, elasticsearch_adapter)
    api.add_resource(AddFileToDataset,
                     '/servicex/internal/transformation/<string:request_id>/files')

    PreflightCheck.make_api(lookup_result_processor)
    api.add_resource(PreflightCheck,
                     '/servicex/internal/transformation/<string:request_id>/preflight')

    FilesetComplete.make_api(lookup_result_processor)
    api.add_resource(FilesetComplete,
                     '/servicex/internal/transformation/<string:request_id>/complete')

    TransformStart.make_api(transformer_manager)
    api.add_resource(TransformStart,
                     '/servicex/internal/transformation/<string:request_id>/start')

    api.add_resource(FileTransformationStatus,
                     '/servicex/internal/transformation/<string:request_id>/<int:file_id>/status')

    TransformerFileComplete.make_api(transformer_manager, elasticsearch_adapter)
    api.add_resource(TransformerFileComplete,
                     '/servicex/internal/transformation/<string:request_id>/file-complete')
