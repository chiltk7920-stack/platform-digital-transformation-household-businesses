from infrastructure.databases.mssql import session
from infrastructure.models import Seller, User, Household

def seed_sellers():
    # Tìm owner user hoặc household
    owner = session.query(User).filter_by(user_name='kc1015').first()
    if not owner:
        print('[ERROR] Owner user kc1015 not found. Run seed_sample_data.py first.')
        return
    household_id = owner.household_id
    sellers = session.query(Seller).filter_by(household_id=household_id).all()
    if sellers:
        print(f'[INFO] Found {len(sellers)} existing sellers for household {household_id}. No changes made.')
        return

    s1 = Seller(
        household_id=household_id,
        tax_code='TAX123456',
        name='Nguyen Van A',
        phone='0909000001',
        address='10 Le Loi, HCM',
        description='Seller sample 1',
        status='ACTIVE',
        created_by='seed'
    )
    s2 = Seller(
        household_id=household_id,
        tax_code='TAX123457',
        name='Tran Thi B',
        phone='0909000002',
        address='20 Nguyen Trai, HCM',
        description='Seller sample 2',
        status='ACTIVE',
        created_by='seed'
    )
    session.add_all([s1, s2])
    session.commit()
    print(f'[OK] Created 2 sellers for household {household_id}')

if __name__ == '__main__':
    seed_sellers()
