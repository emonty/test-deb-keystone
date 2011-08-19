# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import routes

from keystone.common import wsgi
import keystone.backends as db
from keystone.controllers.auth import AuthController
from keystone.controllers.endpointtemplates import EndpointTemplatesController
from keystone.controllers.roles import RolesController
from keystone.controllers.services import ServicesController
from keystone.controllers.staticfiles import StaticFilesController
from keystone.controllers.tenant import TenantController
from keystone.controllers.user import UserController
from keystone.controllers.version import VersionController
from keystone.controllers.extensions import ExtensionsController


class AdminApi(wsgi.Router):
    """WSGI entry point for admin Keystone API requests."""

    def __init__(self, options):
        self.options = options
        mapper = routes.Mapper()
        db.configure_backends(options)

        # Token Operations
        auth_controller = AuthController(options)
        mapper.connect("/tokens", controller=auth_controller,
                       action="authenticate",
                       conditions=dict(method=["POST"]))
        mapper.connect("/tokens/{token_id}", controller=auth_controller,
                        action="validate_token",
                        conditions=dict(method=["GET"]))
        mapper.connect("/tokens/{token_id}", controller=auth_controller,
                        action="delete_token",
                        conditions=dict(method=["DELETE"]))

        # Tenant Operations
        tenant_controller = TenantController(options)
        mapper.connect("/tenants", controller=tenant_controller,
                    action="create_tenant",
                    conditions=dict(method=["PUT", "POST"]))
        mapper.connect("/tenants", controller=tenant_controller,
                    action="get_tenants", conditions=dict(method=["GET"]))
        mapper.connect("/tenants/{tenant_id}",
                    controller=tenant_controller,
                    action="get_tenant", conditions=dict(method=["GET"]))
        mapper.connect("/tenants/{tenant_id}",
                    controller=tenant_controller,
                    action="update_tenant", conditions=dict(method=["PUT"]))
        mapper.connect("/tenants/{tenant_id}",
                    controller=tenant_controller,
                    action="delete_tenant", conditions=dict(method=["DELETE"]))

        # User Operations
        user_controller = UserController(options)
        mapper.connect("/users",
                    controller=user_controller,
                    action="create_user",
                    conditions=dict(method=["PUT", "POST"]))
        mapper.connect("/users",
                    controller=user_controller,
                    action="get_users",
                    conditions=dict(method=["GET"]))
        mapper.connect("/users/{user_id}",
                    controller=user_controller,
                    action="get_user",
                    conditions=dict(method=["GET"]))
        mapper.connect("/users/{user_id}",
                    controller=user_controller,
                    action="update_user",
                    conditions=dict(method=["PUT"]))
        mapper.connect("/users/{user_id}",
                    controller=user_controller,
                    action="delete_user",
                    conditions=dict(method=["DELETE"]))
        mapper.connect("/users/{user_id}/password",
                    controller=user_controller,
                    action="set_user_password",
                    conditions=dict(method=["PUT"]))
        mapper.connect("/users/{user_id}/tenant",
                    controller=user_controller,
                    action="update_user_tenant",
                    conditions=dict(method=["PUT"]))
        # Test this, test failed
        mapper.connect("/users/{user_id}/enabled",
                    controller=user_controller,
                    action="set_user_enabled",
                    conditions=dict(method=["PUT"]))
        mapper.connect("/tenants/{tenant_id}/users",
                    controller=user_controller,
                    action="get_tenant_users",
                    conditions=dict(method=["GET"]))

        #Roles
        roles_controller = RolesController(options)
        mapper.connect("/roles", controller=roles_controller,
                    action="create_role", conditions=dict(method=["POST"]))
        mapper.connect("/roles", controller=roles_controller,
                    action="get_roles", conditions=dict(method=["GET"]))
        mapper.connect("/roles/{role_id}", controller=roles_controller,
                    action="get_role", conditions=dict(method=["GET"]))
        mapper.connect("/roles/{role_id}", controller=roles_controller,
            action="delete_role", conditions=dict(method=["DELETE"]))
        mapper.connect("/users/{user_id}/roleRefs",
            controller=roles_controller, action="get_role_refs",
            conditions=dict(method=["GET"]))
        mapper.connect("/users/{user_id}/roleRefs",
            controller=roles_controller, action="create_role_ref",
            conditions=dict(method=["POST"]))
        mapper.connect("/users/{user_id}/roleRefs/{role_ref_id}",
            controller=roles_controller, action="delete_role_ref",
            conditions=dict(method=["DELETE"]))

        #EndpointTemplatesControllers and Endpoints
        endpoint_templates_controller = EndpointTemplatesController(options)
        mapper.connect("/endpointTemplates",
            controller=endpoint_templates_controller,
                action="get_endpoint_templates",
                    conditions=dict(method=["GET"]))
        mapper.connect("/endpointTemplates",
            controller=endpoint_templates_controller,
                action="add_endpoint_template",
                    conditions=dict(method=["POST"]))
        mapper.connect("/endpointTemplates/{endpoint_templates_id}",
                controller=endpoint_templates_controller,
                    action="get_endpoint_template",
                        conditions=dict(method=["GET"]))
        mapper.connect("/endpointTemplates/{endpoint_templates_id}",
                controller=endpoint_templates_controller,
                    action="delete_endpoint_template",
                        conditions=dict(method=["DELETE"]))
        mapper.connect("/tenants/{tenant_id}/endpoints",
                       controller=endpoint_templates_controller,
                    action="get_endpoints_for_tenant",
                    conditions=dict(method=["GET"]))
        mapper.connect("/tenants/{tenant_id}/endpoints",
                       controller=endpoint_templates_controller,
                     action="add_endpoint_to_tenant",
                     conditions=dict(method=["POST"]))
        mapper.connect(
                "/tenants/{tenant_id}/endpoints/{endpoints_id}",
                controller=endpoint_templates_controller,
                action="remove_endpoint_from_tenant",
                conditions=dict(method=["DELETE"]))

        # Miscellaneous Operations
        version_controller = VersionController(options)
        mapper.connect("/", controller=version_controller,
                    action="get_version_info", file="admin/version",
                    conditions=dict(method=["GET"]))

        extensions_controller = ExtensionsController(options)
        mapper.connect("/extensions",
                        controller=extensions_controller,
                        action="get_extensions_info",
                        path="content/admin/extensions",
                        conditions=dict(method=["GET"]))

        # Static Files Controller
        static_files_controller = StaticFilesController(options)
        mapper.connect("/identityadminguide.pdf",
                    controller=static_files_controller,
                    action="get_pdf_contract",
                    root="content/admin/", pdf="identityadminguide.pdf",
                    conditions=dict(method=["GET"]))
        mapper.connect("/identity-admin.wadl",
                    controller=static_files_controller,
                    action="get_wadl_contract",
                    root="content/admin/", wadl="identity-admin.wadl",
                    conditions=dict(method=["GET"]))
        mapper.connect("/common.ent",
                    controller=static_files_controller,
                    action="get_wadl_contract",
                    root="content/common/", wadl="common.ent",
                    conditions=dict(method=["GET"]))
        mapper.connect("/xsd/{xsd}",
                    controller=static_files_controller,
                    action="get_xsd_contract",
                    root="content/admin/",
                    conditions=dict(method=["GET"]))
        mapper.connect("/xsd/atom/{xsd}",
                    controller=static_files_controller,
                    action="get_xsd_atom_contract",
                    root="content/admin/",
                    conditions=dict(method=["GET"]))
        mapper.connect("/xslt/{file:.*}",
                    controller=static_files_controller,
                    action="get_static_file",
                    root="content/common/", path="xslt/",
                    mimetype="application/xml",
                    conditions=dict(method=["GET"]))
        mapper.connect("/js/{file:.*}",
                    controller=static_files_controller,
                    action="get_static_file",
                    root="content/common/", path="js/",
                    mimetype="application/javascript",
                    conditions=dict(method=["GET"]))
        mapper.connect("/style/{file:.*}",
                    controller=static_files_controller,
                    action="get_static_file",
                    root="content/common/", path="style/",
                    mimetype="application/css",
                    conditions=dict(method=["GET"]))
        mapper.connect("/samples/{file:.*}",
                    controller=static_files_controller,
                    action="get_static_file",
                    root="content/common/", path="samples/",
                    conditions=dict(method=["GET"]))

        # Services Controller
        services_controller = ServicesController(options)
        mapper.connect("/services",
                    controller=services_controller,
                    action="get_services",
                    conditions=dict(method=["GET"]))
        mapper.connect("/services",
                    controller=services_controller,
                    action="create_service",
                    conditions=dict(method=["POST"]))
        mapper.connect("/services/{service_id}",
                    controller=services_controller,
                    action="delete_service",
                    conditions=dict(method=["DELETE"]))
        mapper.connect("/services/{service_id}",
                    controller=services_controller,
                    action="get_service",
                    conditions=dict(method=["GET"]))
        super(AdminApi, self).__init__(mapper)
