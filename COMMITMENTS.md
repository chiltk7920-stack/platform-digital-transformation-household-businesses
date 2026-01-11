# CAM KẾT VÀ GHI NHỚ - BIZFLOW PROJECT

## 📋 TỔNG HỢP CAM KẾT

---

## 1. 🏗️ KIẾN TRÚC CLEAN ARCHITECTURE

### Luồng dữ liệu chuẩn:
```
JSON Body 
  → Controller (validate schema, tạo Object DTO từ Domain)
  → Service (nhận Object DTO, xử lý business logic)
  → Repository (nhận Object DTO, mapping DTO → ORM Model)
  → Database (ORM Model)
```

### Các Layer:
- **Presentation Layer (API)**: Controller + Schemas (Marshmallow)
- **Application Layer (Services)**: Business logic, business rules, nhận DTO, gọi Repository
- **Domain Layer**: Object DTO + Domain Models + Interface Repository
- **Infrastructure Layer**: Repository implementation + ORM Models + Database

---

## 2. 📜 RULES TỪ DOCUMENTS.MD

1. **25 model entities ở infrastructure là nền tảng** - KHÔNG ĐỤNG VÀO, bám sát để code BE, yêu cầu đúng từng field và các quan hệ khóa chính khóa ngoại.

2. **Todo là code mẫu, là chuẩn mực** - Yêu cầu dựa vào để code toàn bộ Flask clean architecture system.

3. **API flow**: Controller → Service → Repositories

4. **DTO Pattern**: 
   - API được gọi nhận JSON body
   - Ở phần Domain thực hiện Object Data Transfer Object
   - Tầng Service lấy Object DTO đó quăng xuống thằng Repositories
   - Repositories thực hiện quá trình mapping từ Object DTO thành Object Model
   - Rồi mới migrations xuống cơ sở dữ liệu

5. **Luồng ngược lại**: Khi call API, FE nhận Json body để thực hiện.

6. **Không tạo các file.md** để tránh rối code.

7. **Đọc kĩ file documents.md** là yêu cầu từ khách hàng, đối chiếu yêu cầu và 25 models để thực hiện đầy đủ.

8. **Chưa đụng tới phần AI Draft Orders.**

---

## 3. ✅ TODO CODE (CHUẨN MỰC)

- **Giữ nguyên Todo code hiện tại** (đã test tốt, API hoạt động ngon lành)
- **Dùng Todo làm reference/template** cho các module khác
- **Các module mới sẽ theo pattern có DTO** (theo sơ đồ kiến trúc)

### Cấu trúc Todo:
- `domain/models/todo.py` - Domain model
- `domain/models/itodo_repository.py` - Interface repository
- `services/todo_service.py` - Business logic
- `infrastructure/repositories/todo_repository.py` - Repository implementation
- `infrastructure/models/todo_model.py` - ORM Model
- `api/controllers/todo_controller.py` - REST API endpoints
- `api/schemas/todo.py` - Marshmallow schemas

---

## 4. 🎯 40 FUNCTIONS & SCREENFLOW

- ✅ **40 functions đã được map đầy đủ vào SCREENFLOW.MD** (100% khớp)
- ✅ Mỗi function có screens tương ứng rõ ràng
- ✅ Methods (C,R,U,D) được map đúng vào các screens

### Phân bổ:
- **Admin (F0xx)**: 7 functions
- **Owner (F1xx)**: 18 functions  
- **Employee (F2xx)**: 15 functions

---

## 5. 💻 CAM KẾT CODE MODULE MỚI

### Pattern cho module mới (theo sơ đồ kiến trúc):

#### **Domain Layer:**
- `domain/models/{entity}.py` - Domain model class
- `domain/models/{entity}_dto.py` - **Object DTO class** (mới, theo sơ đồ)
- `domain/models/i{entity}_repository.py` - Interface repository (abstract)

#### **Service Layer:**
- `services/{entity}_service.py` - **Nhận Object DTO**, xử lý business logic

#### **Infrastructure Layer:**
- `infrastructure/repositories/{entity}_repository.py` - **Mapping DTO → Model**
- `infrastructure/models/{entity}_model.py` - ORM Model (từ 25 models, không đụng vào)

#### **API Layer:**
- `api/controllers/{entity}_controller.py` - **Tạo DTO từ JSON**, gọi Service
- `api/schemas/{entity}.py` - Marshmallow schemas (RequestSchema, ResponseSchema)

### Luồng code module mới:
1. Controller nhận JSON → validate schema
2. Controller tạo Object DTO từ Domain
3. Controller gọi Service với Object DTO
4. Service nhận DTO, xử lý business logic
5. Service gọi Repository với Object DTO
6. Repository mapping Object DTO → Object Model (ORM)
7. Repository save vào Database

---

## 6. 🛠️ TECH STACK

### Backend:
- **Language**: Python
- **Framework**: Flask
- **Architecture**: Clean Architecture

### Database:
- **SQL Server** và **PostgreSQL**
- **Cache**: Redis

### AI:
- **RAG**: ChromaDB, text-embedding-3-small
- **LLM**: OpenAI/Gemini
- **Speech-to-Text**: Google Speech-to-Text/Whisper

### Frontend:
- **Mobile**: Flutter, Notification
- **Web**: NextJS, Tanstack Query, Shadcn UI, TailwindCSS

---

## 7. 🔐 CAM KẾT HỆ THỐNG XÁC THỰC VÀ PHÂN QUYỀN

### Quan hệ hệ thống:
```
User → Role (1 user có 1 role)
  ↓
Role → Function (many-to-many: 1 role có nhiều functions)
  ↓
User → Household (user thuộc household, Admin thì household_id = NULL)
  ↓
Household → Subscription Plan (household đăng ký subscription plan)
```

### 6 CAM KẾT:

#### 1. ✅ Xác thực (Authentication)
- **Login**: `POST /api/auth/login` với `user_name` + `password`
- **JWT token**: Chứa `user_id`, `role_id`, `household_id` (nếu có)
- **Token expiration**: 2-24 giờ (configurable)
- **Password**: Hash bằng bcrypt/werkzeug trước khi lưu

#### 2. ✅ Phân quyền (Authorization)
- **Role-based**: User có role (Admin, Owner, Employee)
- **Function-based**: Role có nhiều functions (F0xx, F1xx, F2xx)
- **Method check**: Function có HTTP methods (C, R, U, D)
- **Kiểm tra theo thứ tự**:
  1. User có tồn tại và active?
  2. User có role hợp lệ?
  3. Role có function tương ứng với endpoint?
  4. Function có HTTP method phù hợp?
  5. User thuộc Household? (trừ Admin)
  6. Household có Subscription Plan active? (nếu Owner/Employee)

#### 3. ✅ Subscription Plan Check
- **Tự động check** subscription cho Owner/Employee
- **Mỗi request**: Lấy `household_id` từ JWT → Check `subscriptions` table
- **Điều kiện**: `household_id`, `is_active = True`, `end_date > now()`
- **Nếu không active**: Trả 403 Forbidden
- **Admin**: Không cần check subscription

<<<<<<< HEAD
=======
**Business Rules về Subscription:**
- **KHÔNG được đăng ký Plan B khi đã có Plan A active**: Một household chỉ được có 1 subscription active tại một thời điểm
- **Owner tự quản lý subscription** (không cần Admin):
  - **Registration flow**: Owner đăng ký plan → Subscription tự tạo trong registration flow
  - **Upgrade flow**: Owner muốn upgrade plan → Gọi `PUT /api/owner/subscription` với `plan_id` mới → Subscription tự update
  - Owner có endpoints: `GET /api/owner/subscription` (xem), `PUT /api/owner/subscription` (upgrade)
  - Owner chỉ được xem/update subscription của household mình (data isolation)
- **Admin quản lý subscription** (F003):
  - Admin CHỈ được list all subscriptions và deactivate (is_active=false)
  - **KHÔNG được**: Create subscription (Owner tự đăng ký qua registration flow)
  - **KHÔNG được**: Update plan_id, start_date, end_date (Owner tự upgrade qua PUT /api/owner/subscription)
  - **KHÔNG được**: Delete subscription
  - **KHÔNG được**: Activate subscription (Owner tự activate khi upgrade)
- **Upgrade flow cho Owner**:
  - Owner gọi `PUT /api/owner/subscription` với `plan_id` mới
  - System tự động: Update plan_id, start_date (default: today), end_date (tính từ billing_cycle của plan mới)

>>>>>>> upstream/main
#### 4. ✅ Data Isolation
- **Owner/Employee**: Chỉ truy cập data của household mình (filter by `household_id`)
- **Admin**: Xem tất cả data (không filter)
- **Tự động filter** trong Repository layer

<<<<<<< HEAD
=======
**Business Rules về Data Isolation:**
- **Owner GET household**: Chỉ được xem household của chính mình (household_id từ JWT token)
- **Owner KHÔNG được query "hết"**: Không có endpoint `GET /api/owner/households` (list all)
- **Owner chỉ có endpoint**: `GET /api/owner/household` (singular) - lấy household của chính mình
- **household_id từ JWT**: Owner không thể fake được household_id vì nó được lấy từ JWT token trong middleware
- **Repository layer**: Chỉ query theo household_id cụ thể, không query all households cho Owner

>>>>>>> upstream/main
#### 5. ✅ Security
- **Password hashing**: Bcrypt/werkzeug
- **Token expiration**: Configurable, default 2-24 giờ
- **Secure headers**: CORS, security headers
- **Error handling**: 401 (Unauthorized), 403 (Forbidden) rõ ràng

#### 6. ✅ Scalable Architecture
- **Dễ thêm role/function mới**: Chỉ cần thêm vào database
- **Decorator pattern**: `@require_permission()`, `@require_role()`
- **Middleware**: JWT decode, permission check
- **Service layer**: `auth_service.py`, `permission_service.py`, `subscription_service.py`

### Logic phân quyền:

#### **Admin** (`household_id = NULL`):
<<<<<<< HEAD
- Có tất cả functions (F0xx)
- Không cần check subscription
- Quản lý toàn bộ hệ thống
- Không filter data

#### **Owner** (`household_id != NULL`, `role_id = Owner`):
- Có functions của Owner (F1xx)
- Phải có subscription active
- Chỉ truy cập data của household mình
- Filter by `household_id`
=======
- Có functions (F0xx): F002, F003, F004, F005, F006, F007
- **KHÔNG có F001 manage_households** - Admin không quản lý Household
- **F003 manage_subscriptions**: CHỈ được list all subscriptions và deactivate (KHÔNG được create, update plan_id, delete)
- Không cần check subscription
- Quản lý: Subscription Plans, Subscriptions (CHỈ list và deactivate), Users (Admin/Owner), Platform Analytics, System Config, Accounting Ledgers
- Không filter data

#### **Owner** (`household_id != NULL`, `role_id = Owner`):
- Có functions của Owner (F1xx): F101-F118
- **Có F102 view_own_household (R, U)** - Quản lý household và subscription của chính mình
- Phải có subscription active
- Chỉ truy cập data của household mình
- Filter by `household_id`
- **Owner Registration Flow**: Chọn Plan → Tạo Household → Tạo Owner Account → Tạo Subscription (Public endpoints)
- **Owner tự quản lý subscription**:
  - `GET /api/owner/subscription` - Xem subscription của household mình
  - `PUT /api/owner/subscription` - Upgrade subscription plan (tự update, không cần Admin)
>>>>>>> upstream/main

#### **Employee** (`household_id != NULL`, `role_id = Employee`):
- Có functions của Employee (F2xx)
- Phải có subscription active của household
- Chỉ truy cập data của household mình
- Filter by `household_id`

### Luồng request:
```
1. Request đến API
   ↓
2. Auth Middleware: Decode JWT → lấy user_id, role_id, household_id
   ↓
3. Permission Middleware: 
   - Check user có function code tương ứng?
   - Check HTTP method có trong function.http_methods?
   ↓
4. Subscription Check (nếu Owner/Employee):
   - Check household có subscription active?
   ↓
5. Controller: Xử lý request (tự động filter by household_id nếu Owner/Employee)
   ↓
6. Service: Business logic
   ↓
7. Repository: Database operations (với household_id filter)
   ↓
8. Response
```

---

## 8. ✅ CHECKLIST KHI CODE MODULE MỚI

- [ ] Đọc Documents.md để hiểu requirements
- [ ] Đối chiếu với 25 models ở infrastructure
- [ ] Tạo Domain model + DTO + Interface repository
- [ ] Tạo Service nhận DTO
- [ ] Tạo Repository mapping DTO → Model
- [ ] Tạo Controller tạo DTO từ JSON
- [ ] Tạo Schemas (RequestSchema, ResponseSchema)
- [ ] Đăng ký routes trong `api/routes.py`
- [ ] Test API endpoints
- [ ] Đảm bảo đúng Clean Architecture flow

---

## 9. 📋 CAM KẾT CHO 6 THÀNH VIÊN CÒN LẠI

### Họ chỉ cần làm 3 bước:

#### 1. ✅ Import decorators và utils
```python
from api.decorators.auth_decorators import require_permission
from api.utils.auth_utils import get_current_household_id
```

#### 2. ✅ Decorate endpoint với function code
```python
@bp.route('/products', methods=['GET'])
@require_permission(function_code="F104", methods=["GET"])
def list_products():
    pass
```

#### 3. ✅ Lấy household_id và truyền vào service
```python
household_id = get_current_household_id()  # Tự động None nếu Admin
products = product_service.list_products(household_id)
```

### Checklist mỗi endpoint:
- [ ] Import decorator và utils
- [ ] Decorate với function code đúng (từ Documents.md)
- [ ] Lấy `household_id` nếu cần filter (Owner/Employee)
- [ ] Truyền `household_id` vào service

### Lưu ý:
- **Function code**: Lấy từ Documents.md (F0xx, F1xx, F2xx)
- **Admin endpoints**: Không cần filter (household_id = None)
- **Owner/Employee endpoints**: Luôn lấy household_id để filter
- **Tự động check**: Permission, subscription, role (không cần code)

---

## 10. 🧪 CAM KẾT TEST API

### Test bằng Swagger UI (giống Todo):
- **URL**: `http://localhost:6868/docs`
- **Swagger JSON**: `http://localhost:6868/swagger.json`
- **Cách test**: Mở browser → Swagger UI → Click "Try it out" → Nhập data → Execute
- **Docstring format**: Mỗi endpoint có docstring theo Swagger/OpenAPI format để tự động generate documentation
- **Không cần unit test files**: Test trực tiếp trên Swagger UI

---

## 📝 LƯU Ý QUAN TRỌNG

1. **Giữ Todo code làm chuẩn mực** - Không sửa Todo
2. **Bám sát 25 models** - Không thay đổi structure
3. **DTO pattern bắt buộc** cho module mới
4. **Controller → Service → Repository** (không bỏ qua layer)
5. **Đối chiếu Documents.md** với SCREENFLOW.MD
6. **Không tạo file .md** trong code (trừ file này để ghi nhớ)

---

**Cập nhật lần cuối**: 2025-01-XX
**Trạng thái**: ✅ Đã ghi nhận và cam kết thực hiện
