from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apispec import APISpec  # type: ignore
    from apispec.ext.marshmallow import MarshmallowPlugin  # type: ignore
    from apispec_webframeworks.flask import FlaskPlugin  # type: ignore

try:
    from apispec import APISpec  # type: ignore
    from apispec.ext.marshmallow import MarshmallowPlugin  # type: ignore
    from apispec_webframeworks.flask import FlaskPlugin  # type: ignore
    
    spec = APISpec(
        title="BizFlow API",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )
    
    # Thêm Bearer token security scheme
    spec.components.security_scheme(
        "Bearer",
        {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Nhập token JWT từ /api/auth/login. Chỉ cần dán token, không cần chữ 'Bearer'"
        }
    )
    
    # Thêm security mặc định cho tất cả endpoints (trừ login)
    spec.options = {"security": [{"Bearer": []}]}
    
    APISPEC_AVAILABLE = True
except ImportError:
    spec = None
    APISPEC_AVAILABLE = False

if APISPEC_AVAILABLE:
    from api.schemas.todo import TodoRequestSchema, TodoResponseSchema
    from api.schemas.user import UserRequestSchema, UserResponseSchema, UserUpdateSchema
    from api.schemas.role import RoleRequestSchema, RoleResponseSchema, RoleUpdateSchema
    from api.schemas.function import FunctionRequestSchema, FunctionResponseSchema, FunctionUpdateSchema
    from api.schemas.role_function import RoleFunctionRequestSchema, RoleFunctionResponseSchema
    from api.schemas.customer import CustomerRequestSchema, CustomerResponseSchema, CustomerUpdateSchema
    from api.schemas.seller import SellerRequestSchema, SellerResponseSchema, SellerUpdateSchema
    
    # Đăng ký schema để tự động sinh model
    spec.components.schema("TodoRequest", schema=TodoRequestSchema)
    spec.components.schema("TodoResponse", schema=TodoResponseSchema)
    
    # User schemas
    spec.components.schema("UserRequest", schema=UserRequestSchema)
    spec.components.schema("UserResponse", schema=UserResponseSchema)
    spec.components.schema("UserUpdate", schema=UserUpdateSchema)
    
    # Role schemas
    spec.components.schema("RoleRequest", schema=RoleRequestSchema)
    spec.components.schema("RoleResponse", schema=RoleResponseSchema)
    spec.components.schema("RoleUpdate", schema=RoleUpdateSchema)
    
    # Function schemas
    spec.components.schema("FunctionRequest", schema=FunctionRequestSchema)
    spec.components.schema("FunctionResponse", schema=FunctionResponseSchema)
    spec.components.schema("FunctionUpdate", schema=FunctionUpdateSchema)
    
    # RoleFunction schemas
    spec.components.schema("RoleFunctionRequest", schema=RoleFunctionRequestSchema)
    spec.components.schema("RoleFunctionResponse", schema=RoleFunctionResponseSchema)
    
    # Customer schemas
    spec.components.schema("CustomerRequest", schema=CustomerRequestSchema)
    spec.components.schema("CustomerResponse", schema=CustomerResponseSchema)
    spec.components.schema("CustomerUpdate", schema=CustomerUpdateSchema)
    
    # Seller schemas
    spec.components.schema("SellerRequest", schema=SellerRequestSchema)
    spec.components.schema("SellerResponse", schema=SellerResponseSchema)
    spec.components.schema("SellerUpdate", schema=SellerUpdateSchema)