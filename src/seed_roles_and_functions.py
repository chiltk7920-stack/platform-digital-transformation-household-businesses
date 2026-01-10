"""
Script để tạo Roles và Functions - CHẠY ĐẦU TIÊN
Tạo 3 roles (Admin, Owner, Employee) và các functions cho hệ thống
"""
import sys
import os
# Set encoding for Windows console
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

from app import create_app
from infrastructure.databases.mssql import session
from infrastructure.models import Role, Function, RoleFunction

def seed_roles_and_functions():
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("SEEDING ROLES & FUNCTIONS")
            print("=" * 60)
            
            # 1. TẠO ROLES
            print("\n[1] Creating Roles...")
            
            roles_data = [
                {
                    'role_name': 'Admin',
                    'description': 'System Administrator - Full access to all functions'
                },
                {
                    'role_name': 'Owner',
                    'description': 'Household Business Owner - Can manage household and employees'
                },
                {
                    'role_name': 'Employee',
                    'description': 'Household Employee - Limited access for daily operations'
                }
            ]
            
            roles_map = {}
            for role_data in roles_data:
                existing_role = session.query(Role).filter_by(role_name=role_data['role_name']).first()
                if existing_role:
                    print(f"   [SKIP] Role '{role_data['role_name']}' already exists (ID: {existing_role.id})")
                    roles_map[role_data['role_name']] = existing_role
                else:
                    role = Role(
                        role_name=role_data['role_name'],
                        description=role_data['description']
                    )
                    session.add(role)
                    session.flush()
                    roles_map[role_data['role_name']] = role
                    print(f"   [OK] Created role '{role_data['role_name']}' (ID: {role.id})")
            
            # 2. TẠO FUNCTIONS
            print("\n[2] Creating Functions...")
            
            functions_data = [
                # Admin Functions
                {
                    'function_code': 'F001',
                    'function_name': 'Manage Users',
                    'url_pattern': '/api/admin/users/*',
                    'http_methods': 'C,R,U,D',
                    'resource_type': 'user',
                    'description': 'Create, Read, Update, Delete users'
                },
                {
                    'function_code': 'F002',
                    'function_name': 'Manage Roles',
                    'url_pattern': '/api/admin/roles/*',
                    'http_methods': 'C,R,U,D',
                    'resource_type': 'role',
                    'description': 'Create, Read, Update, Delete roles'
                },
                {
                    'function_code': 'F003',
                    'function_name': 'Manage Functions',
                    'url_pattern': '/api/admin/functions/*',
                    'http_methods': 'C,R,U,D',
                    'resource_type': 'function',
                    'description': 'Create, Read, Update, Delete functions'
                },
                {
                    'function_code': 'F004',
                    'function_name': 'Assign Functions to Roles',
                    'url_pattern': '/api/admin/roles/<role_id>/functions',
                    'http_methods': 'C,R,D',
                    'resource_type': 'role_function',
                    'description': 'Assign or remove functions from roles'
                },
                # Owner Functions (F109, F110, F205, F206, etc.)
                {
                    'function_code': 'F109',
                    'function_name': 'Manage Customers',
                    'url_pattern': '/api/owner/customers/*',
                    'http_methods': 'C,R,U,D',
                    'resource_type': 'customer',
                    'description': 'Create, Read, Update, Delete customers'
                },
                {
                    'function_code': 'F110',
                    'function_name': 'Manage Sellers',
                    'url_pattern': '/api/owner/sellers/*',
                    'http_methods': 'C,R,U,D',
                    'resource_type': 'seller',
                    'description': 'Create, Read, Update, Delete sellers'
                },
                {
                    'function_code': 'F111',
                    'function_name': 'View Customer History',
                    'url_pattern': '/api/owner/customers/<customer_id>/history',
                    'http_methods': 'R',
                    'resource_type': 'customer',
                    'description': 'View customer purchase history'
                },
                {
                    'function_code': 'F112',
                    'function_name': 'View Customer Debt',
                    'url_pattern': '/api/owner/customers/<customer_id>/debt',
                    'http_methods': 'R',
                    'resource_type': 'customer',
                    'description': 'View customer debt information'
                },
                # Employee Functions
                {
                    'function_code': 'F205',
                    'function_name': 'View Customers (Employee)',
                    'url_pattern': '/api/employee/customers/*',
                    'http_methods': 'R',
                    'resource_type': 'customer',
                    'description': 'View customers (read-only for employees)'
                },
                {
                    'function_code': 'F206',
                    'function_name': 'View Customer Debt (Employee)',
                    'url_pattern': '/api/employee/customers/<customer_id>/debt',
                    'http_methods': 'R',
                    'resource_type': 'customer',
                    'description': 'View customer debt information (employee access)'
                },
                # Other Functions
                {
                    'function_code': 'F050',
                    'function_name': 'Manage Household Employees',
                    'url_pattern': '/api/owner/employees/*',
                    'http_methods': 'C,R,U,D',
                    'resource_type': 'employee',
                    'description': 'Create, Read, Update, Delete employees in household'
                },
                {
                    'function_code': 'F010',
                    'function_name': 'Manage Households',
                    'url_pattern': '/api/admin/households/*',
                    'http_methods': 'C,R,U,D',
                    'resource_type': 'household',
                    'description': 'Manage households'
                },
            ]
            
            functions_map = {}
            for func_data in functions_data:
                existing_func = session.query(Function).filter_by(
                    function_code=func_data['function_code']
                ).first()
                
                if existing_func:
                    print(f"   [SKIP] Function {func_data['function_code']} already exists")
                    functions_map[func_data['function_code']] = existing_func
                else:
                    func = Function(
                        function_code=func_data['function_code'],
                        function_name=func_data['function_name'],
                        url_pattern=func_data['url_pattern'],
                        http_methods=func_data['http_methods'],
                        resource_type=func_data['resource_type'],
                        description=func_data['description']
                    )
                    session.add(func)
                    session.flush()
                    functions_map[func_data['function_code']] = func
                    print(f"   [OK] Created function {func_data['function_code']}: {func_data['function_name']}")
            
            # 3. ASSIGN FUNCTIONS TO ROLES
            print("\n[3] Assigning Functions to Roles...")
            
            role_function_mapping = {
                'Admin': ['F001', 'F002', 'F003', 'F004', 'F109', 'F110', 'F111', 'F112', 'F050', 'F010', 'F205', 'F206'],
                'Owner': ['F109', 'F110', 'F111', 'F112', 'F050'],
                'Employee': ['F205', 'F206']
            }
            
            for role_name, function_codes in role_function_mapping.items():
                role = roles_map[role_name]
                for func_code in function_codes:
                    # Check if already assigned
                    existing = session.query(RoleFunction).filter_by(
                        role_id=role.id,
                        function_id=functions_map[func_code].id
                    ).first()
                    
                    if existing:
                        print(f"   [SKIP] {role_name} already has {func_code}")
                    else:
                        role_func = RoleFunction(
                            role_id=role.id,
                            function_id=functions_map[func_code].id
                        )
                        session.add(role_func)
                        print(f"   [OK] Assigned {func_code} to {role_name}")
            
            # 4. COMMIT
            session.commit()
            
            print("\n" + "=" * 60)
            print("[SUCCESS] Roles and Functions seeded successfully!")
            print("=" * 60)
            print("\nRoles created:")
            for role_name, role in roles_map.items():
                print(f"   - {role_name} (ID: {role.id})")
            
            print("\nNext step: Run seed_admin_user.py to create Admin user")
            
        except Exception as e:
            session.rollback()
            print(f"[ERROR] Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    seed_roles_and_functions()
