"""
Script để tạo Admin user - CHẠY TRƯỚC TIÊN
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
from infrastructure.models import User, Role

def seed_admin_user():
    app = create_app()
    
    with app.app_context():
        try:
            # 1. Kiem tra xem admin user da ton tai chua
            admin_user = session.query(User).filter_by(user_name='admin').first()
            if admin_user:
                print(f"[INFO] Admin user da ton tai: {admin_user.user_name}")
                return
            
            # 2. Lay Admin role
            admin_role = session.query(Role).filter_by(role_name='Admin').first()
            if not admin_role:
                print("[ERROR] Khong tim thay Admin role. Vui long tao role truoc.")
                return
            
            # 3. Tao Admin user
            admin = User(
                household_id=None,
                role_id=admin_role.id,
                user_name="admin",
                password="admin123",
                email="admin@example.com",
                description="Admin user - System Administrator",
                status="ACTIVE",
                created_by="system",
                updated_by="system"
            )
            session.add(admin)
            session.commit()
            print(f"[SUCCESS] Da tao Admin user thanh cong!")
            print(f"   - Username: {admin.user_name}")
            print(f"   - Password: {admin.password}")
            print(f"   - Role: Admin (ID: {admin.role_id})")
            
        except Exception as e:
            session.rollback()
            print(f"[ERROR] Loi: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    seed_admin_user()
