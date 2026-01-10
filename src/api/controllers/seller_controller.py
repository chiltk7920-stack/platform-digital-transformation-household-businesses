from flask import Blueprint, request, jsonify
from services.seller_service import SellerService
from infrastructure.repositories.seller_repository import SellerRepository
from api.schemas.seller import SellerRequestSchema, SellerResponseSchema, SellerUpdateSchema
from infrastructure.databases.mssql import session
from api.decorators.auth_decorators import require_permission
from api.utils.auth_utils import get_current_household_id

# Owner endpoints for sellers
owner_bp = Blueprint('owner_sellers', __name__, url_prefix='/api/owner/sellers')
seller_service = SellerService(SellerRepository(session))
request_schema = SellerRequestSchema()
response_schema = SellerResponseSchema()
update_schema = SellerUpdateSchema()

@owner_bp.route('/', methods=['GET'])
@require_permission(function_code="F110", methods=["GET"])
def list_sellers_owner():
    """
    List all sellers (Owner only)
    ---
    get:
      summary: List all sellers
      security:
        - Bearer: []
      tags:
        - Owner Sellers
      responses:
        200:
          description: List of sellers
        400:
          description: Household ID is required
    """
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    sellers = seller_service.list_sellers(household_id=household_id)
    return jsonify(response_schema.dump(sellers, many=True)), 200

@owner_bp.route('/', methods=['POST'])
@require_permission(function_code="F110", methods=["POST"])
def create_seller_owner():
    """
    Create seller (Owner only)
    ---
    post:
      summary: Create seller
      security:
        - Bearer: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SellerRequest'
      tags:
        - Owner Sellers
      responses:
        201:
          description: Seller created successfully
        400:
          description: Bad request or Household ID required
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    seller = seller_service.create_seller(
        household_id=household_id,
        tax_code=data.get('tax_code'),
        name=data.get('name'),
        phone=data.get('phone'),
        address=data.get('address'),
        description=data.get('description'),
        status=data['status'],
        created_by=data.get('created_by')
    )
    return jsonify(response_schema.dump(seller)), 201

@owner_bp.route('/<int:seller_id>', methods=['GET'])
@require_permission(function_code="F110", methods=["GET"])
def get_seller_owner(seller_id):
    """
    Get seller by id (Owner only)
    ---
    get:
      summary: Get seller by id
      security:
        - Bearer: []
      parameters:
        - name: seller_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Owner Sellers
      responses:
        200:
          description: Seller found
        403:
          description: Seller does not belong to your household
        404:
          description: Seller not found
    """
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    seller = seller_service.get_seller(seller_id)
    if not seller:
        return jsonify({'message': 'Seller not found'}), 404
    if seller.household_id != household_id:
        return jsonify({'error': 'Seller does not belong to your household'}), 403
    return jsonify(response_schema.dump(seller)), 200

@owner_bp.route('/<int:seller_id>', methods=['PUT'])
@require_permission(function_code="F110", methods=["PUT"])
def update_seller_owner(seller_id):
    """
    Update seller (Owner only)
    ---
    put:
      summary: Update seller
      security:
        - Bearer: []
      parameters:
        - name: seller_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SellerUpdate'
      tags:
        - Owner Sellers
      responses:
        200:
          description: Seller updated successfully
        403:
          description: Seller does not belong to your household
        404:
          description: Seller not found
    """
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    existing = seller_service.get_seller(seller_id)
    if not existing:
        return jsonify({'error': 'Seller not found'}), 404
    if existing.household_id != household_id:
        return jsonify({'error': 'Seller does not belong to your household'}), 403
    data = request.get_json()
    errors = update_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    try:
        seller = seller_service.update_seller(
            seller_id=seller_id,
            household_id=household_id,
            tax_code=data.get('tax_code'),
            name=data.get('name'),
            phone=data.get('phone'),
            address=data.get('address'),
            description=data.get('description'),
            status=data.get('status'),
            updated_by=data.get('updated_by')
        )
        return jsonify(response_schema.dump(seller)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@owner_bp.route('/<int:seller_id>', methods=['DELETE'])
@require_permission(function_code="F110", methods=["DELETE"])
def delete_seller_owner(seller_id):
    """
    Delete seller (Owner only)
    ---
    delete:
      summary: Delete seller
      security:
        - Bearer: []
      parameters:
        - name: seller_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Owner Sellers
      responses:
        204:
          description: Seller deleted successfully
        403:
          description: Seller does not belong to your household
        404:
          description: Seller not found
    """
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    existing = seller_service.get_seller(seller_id)
    if not existing:
        return jsonify({'error': 'Seller not found'}), 404
    if existing.household_id != household_id:
        return jsonify({'error': 'Seller does not belong to your household'}), 403
    try:
        seller_service.delete_seller(seller_id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
