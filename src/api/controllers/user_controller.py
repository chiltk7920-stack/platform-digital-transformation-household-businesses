from flask import Blueprint, request, jsonify
from services.user_service import UserService
from infrastructure.repositories.user_repository import UserRepository
from api.schemas.user import UserRequestSchema, UserResponseSchema, UserUpdateSchema
from infrastructure.databases.mssql import session
from api.decorators.auth_decorators import require_permission
from api.utils.auth_utils import get_current_household_id

# Admin endpoints
admin_bp = Blueprint('admin_users', __name__, url_prefix='/api/admin/users')
user_service = UserService(UserRepository(session))
request_schema = UserRequestSchema()
response_schema = UserResponseSchema()
update_schema = UserUpdateSchema()


@admin_bp.route('/', methods=['GET'])
@require_permission(function_code="F001", methods=["GET"])
def list_users():
    """List all users (Admin only). Supports optional filters via query params."""
    role_id = request.args.get('role_id', type=int)
    status = request.args.get('status', type=str)
    household_id = request.args.get('household_id', type=int)
    search_term = request.args.get('search', type=str)

    try:
        users = user_service.list_users(
            exclude_employee=True,
            role_id=role_id,
            status=status,
            household_id=household_id,
            search_term=search_term,
        )
        return jsonify(response_schema.dump(users, many=True)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 403


@admin_bp.route('/', methods=['POST'])
@require_permission(function_code="F005", methods=["POST"])
def create_user():
    """Create user (Admin only)."""
    data = request.get_json() or {}
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    try:
        user = user_service.create_user(
            household_id=data.get('household_id'),
            role_id=data['role_id'],
            user_name=data['user_name'],
            password=data['password'],
            email=data.get('email'),
            description=data.get('description'),
            status=data['status'],
            created_by=data.get('created_by'),
            is_admin_creating=True,
        )
        return jsonify(response_schema.dump(user)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 403


@admin_bp.route('/<int:user_id>', methods=['GET'])
@require_permission(function_code="F005", methods=["GET"])
def get_user(user_id):
    """Get user by id (Admin only)."""
    try:
        user = user_service.get_user(user_id, is_admin_accessing=True)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        return jsonify(response_schema.dump(user)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 403


@admin_bp.route('/<int:user_id>', methods=['PUT'])
@require_permission(function_code="F005", methods=["PUT"])
def update_user(user_id):
    """Update user (Admin only)."""
    data = request.get_json() or {}
    errors = update_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    try:
        user = user_service.update_user(
            user_id=user_id,
            household_id=data.get('household_id'),
            role_id=data.get('role_id'),
            user_name=data.get('user_name'),
            password=data.get('password'),
            email=data.get('email'),
            description=data.get('description'),
            status=data.get('status'),
            updated_by=data.get('updated_by'),
            is_admin_updating=True,
        )
        return jsonify(response_schema.dump(user)), 200
    except ValueError as e:
        if 'not found' in str(e).lower():
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 403


@admin_bp.route('/<int:user_id>', methods=['DELETE'])
@require_permission(function_code="F005", methods=["DELETE"])
def delete_user(user_id):
    """Delete user (Admin only)."""
    try:
        user_service.delete_user(user_id, is_admin_deleting=True)
        return '', 204
    except ValueError as e:
        if 'not found' in str(e).lower():
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 403


# Owner endpoints
owner_bp = Blueprint('owner_employees', __name__, url_prefix='/api/owner/employees')


@owner_bp.route('/', methods=['GET'])
@require_permission(function_code="F101", methods=["GET"])
def list_employees():
    """List employees of household (Owner only)."""
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400

    users = user_service.get_users_by_household(household_id)
    return jsonify(response_schema.dump(users, many=True)), 200


@owner_bp.route('/', methods=['POST'])
@require_permission(function_code="F101", methods=["POST"])
def create_employee():
    """Create employee (Owner only)."""
    data = request.get_json() or {}
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400

    user = user_service.create_user(
        household_id=household_id,
        role_id=data['role_id'],
        user_name=data['user_name'],
        password=data['password'],
        email=data.get('email'),
        description=data.get('description'),
        status=data['status'],
        created_by=data.get('created_by'),
    )
    return jsonify(response_schema.dump(user)), 201


@owner_bp.route('/<int:employee_id>', methods=['GET'])
@require_permission(function_code="F101", methods=["GET"])
def get_employee(employee_id):
    """Get employee by id (Owner only)."""
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400

    user = user_service.get_user(employee_id)
    if not user:
        return jsonify({'message': 'Employee not found'}), 404
    if user.household_id != household_id:
        return jsonify({'error': 'Employee does not belong to your household'}), 403

    return jsonify(response_schema.dump(user)), 200


@owner_bp.route('/<int:employee_id>', methods=['PUT'])
@require_permission(function_code="F101", methods=["PUT"])
def update_employee(employee_id):
    """Update employee (Owner only)."""
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400

    existing_user = user_service.get_user(employee_id)
    if not existing_user:
        return jsonify({'error': 'Employee not found'}), 404
    if existing_user.household_id != household_id:
        return jsonify({'error': 'Employee does not belong to your household'}), 403

    data = request.get_json() or {}
    errors = update_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    try:
        user = user_service.update_user(
            user_id=employee_id,
            household_id=household_id,
            role_id=data.get('role_id'),
            user_name=data.get('user_name'),
            password=data.get('password'),
            email=data.get('email'),
            description=data.get('description'),
            status=data.get('status'),
            updated_by=data.get('updated_by'),
        )
        return jsonify(response_schema.dump(user)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@owner_bp.route('/<int:employee_id>', methods=['DELETE'])
@require_permission(function_code="F101", methods=["DELETE"])
def delete_employee(employee_id):
    """Delete employee (Owner only)."""
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400

    existing_user = user_service.get_user(employee_id)
    if not existing_user:
        return jsonify({'error': 'Employee not found'}), 404
    if existing_user.household_id != household_id:
        return jsonify({'error': 'Employee does not belong to your household'}), 403

    try:
        user_service.delete_user(employee_id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
