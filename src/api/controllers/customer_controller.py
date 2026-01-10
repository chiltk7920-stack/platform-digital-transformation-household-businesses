from flask import Blueprint, request, jsonify
from services.customer_service import CustomerService
from infrastructure.repositories.customer_repository import CustomerRepository
from api.schemas.customer import CustomerRequestSchema, CustomerResponseSchema, CustomerUpdateSchema
from infrastructure.databases.mssql import session
from api.decorators.auth_decorators import require_permission
from api.utils.auth_utils import get_current_household_id

# Owner endpoints
owner_bp = Blueprint('owner_customers', __name__, url_prefix='/api/owner/customers')
customer_service = CustomerService(CustomerRepository(session))
request_schema = CustomerRequestSchema()
response_schema = CustomerResponseSchema()
update_schema = CustomerUpdateSchema()

@owner_bp.route('/', methods=['GET'])
@require_permission(function_code="F109", methods=["GET"])
def list_customers_owner():
    """
    List all customers (Owner only)
    ---
    get:
      summary: List all customers
      security:
        - Bearer: []
      tags:
        - Owner Customers
      responses:
        200:
          description: List of customers
        400:
          description: Household ID is required
    """
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    customers = customer_service.list_customers(household_id=household_id)
    return jsonify(response_schema.dump(customers, many=True)), 200

@owner_bp.route('/', methods=['POST'])
@require_permission(function_code="F109", methods=["POST"])
def create_customer_owner():
    """
    Create customer (Owner only)
    ---
    post:
      summary: Create customer
      security:
        - Bearer: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CustomerRequest'
      tags:
        - Owner Customers
      responses:
        201:
          description: Customer created successfully
        400:
          description: Bad request or Household ID required
    """
    data = request.get_json() or {}
    # Ensure status defaults to ACTIVE when missing
    if 'status' not in data or data.get('status') is None:
      data['status'] = 'ACTIVE'
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    customer = customer_service.create_customer(
        household_id=household_id,
        tax_code=data.get('tax_code'),
        name=data.get('name'),
        phone=data.get('phone'),
        address=data.get('address'),
        description=data.get('description'),
        status=data.get('status'),
        created_by=data.get('created_by')
    )
    return jsonify(response_schema.dump(customer)), 201

@owner_bp.route('/<int:customer_id>', methods=['GET'])
@require_permission(function_code="F109", methods=["GET"])
def get_customer_owner(customer_id):
    """
    Get customer by id (Owner only)
    ---
    get:
      summary: Get customer by id
      security:
        - Bearer: []
      parameters:
        - name: customer_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Owner Customers
      responses:
        200:
          description: Customer found
        403:
          description: Customer does not belong to your household
        404:
          description: Customer not found
    """
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    customer = customer_service.get_customer(customer_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    if customer.household_id != household_id:
        return jsonify({'error': 'Customer does not belong to your household'}), 403
    return jsonify(response_schema.dump(customer)), 200

@owner_bp.route('/<int:customer_id>', methods=['PUT'])
@require_permission(function_code="F109", methods=["PUT"])
def update_customer_owner(customer_id):
    """
    Update customer (Owner only)
    ---
    put:
      summary: Update customer
      security:
        - Bearer: []
      parameters:
        - name: customer_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CustomerUpdate'
      tags:
        - Owner Customers
      responses:
        200:
          description: Customer updated successfully
        403:
          description: Customer does not belong to your household
        404:
          description: Customer not found
    """
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    existing = customer_service.get_customer(customer_id)
    if not existing:
        return jsonify({'error': 'Customer not found'}), 404
    if existing.household_id != household_id:
        return jsonify({'error': 'Customer does not belong to your household'}), 403
    data = request.get_json()
    errors = update_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    try:
        customer = customer_service.update_customer(
            customer_id=customer_id,
            household_id=household_id,
            tax_code=data.get('tax_code'),
            name=data.get('name'),
            phone=data.get('phone'),
            address=data.get('address'),
            description=data.get('description'),
            status=data.get('status'),
            updated_by=data.get('updated_by')
        )
        return jsonify(response_schema.dump(customer)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@owner_bp.route('/<int:customer_id>', methods=['DELETE'])
@require_permission(function_code="F109", methods=["DELETE"])
def delete_customer_owner(customer_id):
    """
    Delete customer (Owner only)
    ---
    delete:
      summary: Delete customer
      security:
        - Bearer: []
      parameters:
        - name: customer_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Owner Customers
      responses:
        204:
          description: Customer deleted successfully
        403:
          description: Customer does not belong to your household
        404:
          description: Customer not found
    """
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    existing = customer_service.get_customer(customer_id)
    if not existing:
        return jsonify({'error': 'Customer not found'}), 404
    if existing.household_id != household_id:
        return jsonify({'error': 'Customer does not belong to your household'}), 403
    try:
        customer_service.delete_customer(customer_id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@owner_bp.route('/<int:customer_id>/history', methods=['GET'])
@require_permission(function_code="F109", methods=["GET"])
def customer_history_owner(customer_id):
    """
    Get customer purchase history (Owner only)
    ---
    get:
      summary: Get customer purchase history
      security:
        - Bearer: []
      parameters:
        - name: customer_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Owner Customers
      responses:
        200:
          description: Customer purchase history
        403:
          description: Customer does not belong to your household
        404:
          description: Customer not found
    """
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    existing = customer_service.get_customer(customer_id)
    if not existing:
        return jsonify({'error': 'Customer not found'}), 404
    if existing.household_id != household_id:
        return jsonify({'error': 'Customer does not belong to your household'}), 403
    history = customer_service.get_purchase_history(customer_id)
    # Simple serialization
    result = []
    for inv in history:
        result.append({
            'id': inv.id,
            'invoice_type': inv.invoice_type,
            'total_amount': float(inv.total_amount or 0),
            'status': inv.status,
            'created_at': inv.created_at
        })
    return jsonify(result), 200

@owner_bp.route('/<int:customer_id>/debt', methods=['GET'])
@require_permission(function_code="F109", methods=["GET"])
def customer_debt_owner(customer_id):
    """
    Get customer outstanding debt (Owner only)
    ---
    get:
      summary: Get customer outstanding debt
      security:
        - Bearer: []
      parameters:
        - name: customer_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Owner Customers
      responses:
        200:
          description: Customer debt information
        403:
          description: Customer does not belong to your household
        404:
          description: Customer not found
    """
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    existing = customer_service.get_customer(customer_id)
    if not existing:
        return jsonify({'error': 'Customer not found'}), 404
    if existing.household_id != household_id:
        return jsonify({'error': 'Customer does not belong to your household'}), 403
    debt = customer_service.get_debt(customer_id)
    return jsonify(debt), 200

# Employee endpoints (read-only)
employee_bp = Blueprint('employee_customers', __name__, url_prefix='/api/employee/customers')

@employee_bp.route('/', methods=['GET'])
@require_permission(function_code="F205", methods=["GET"])
def list_customers_employee():
    """
    List all customers (Employee only, read-only)
    ---
    get:
      summary: List all customers
      security:
        - Bearer: []
      tags:
        - Employee Customers
      responses:
        200:
          description: List of customers
    """
    # Employee can list customers (data isolation handled elsewhere if needed)
    customers = customer_service.list_customers()
    return jsonify(response_schema.dump(customers, many=True)), 200

@employee_bp.route('/<int:customer_id>', methods=['GET'])
@require_permission(function_code="F206", methods=["GET"])
def get_customer_employee(customer_id):
    """
    Get customer by id (Employee only, read-only)
    ---
    get:
      summary: Get customer by id
      security:
        - Bearer: []
      parameters:
        - name: customer_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Employee Customers
      responses:
        200:
          description: Customer found
        404:
          description: Customer not found
    """
    customer = customer_service.get_customer(customer_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    return jsonify(response_schema.dump(customer)), 200

@employee_bp.route('/<int:customer_id>/debt', methods=['GET'])
@require_permission(function_code="F206", methods=["GET"])
def customer_debt_employee(customer_id):
    """
    Get customer debt (Employee only, read-only)
    ---
    get:
      summary: Get customer outstanding debt
      security:
        - Bearer: []
      parameters:
        - name: customer_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Employee Customers
      responses:
        200:
          description: Customer debt information
        404:
          description: Customer not found
    """
    customer = customer_service.get_customer(customer_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    debt = customer_service.get_debt(customer_id)
    return jsonify(debt), 200
