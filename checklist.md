# E-Commerce API Setup Checklist

Complete this checklist to ensure your API is properly configured and running.

## 📋 Pre-Installation

- [ ] Python 3.8+ installed (`python --version`)
- [ ] MySQL 5.7+ installed and running
- [ ] Git installed (for cloning repository)
- [ ] Virtual environment tool available

## 🗂️ Project Structure Verification

Ensure your project has the following structure:

```
ecommerce-api/
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── product.py
│   └── admin.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── product.py
├── schemas/
│   ├── __init__.py
│   ├── user.py
│   └── product.py
├── core/
│   ├── __init__.py
│   └── security.py
├── dependencies/
│   ├── __init__.py
│   ├── auth.py
│   └── roles.py
├── static/
│   ├── index.html
│   ├── status.html
│   ├── incidents.html
│   ├── docs-landing.html
│   └── swagger.html
├── database.py
├── main.py
├── tests.py
├── requirements.txt
├── requirements-minimal.txt
├── database_setup.sql
├── .env.example
├── .gitignore
└── README.md
```

## 🔧 Installation Steps

### 1. Clone Repository

- [ ] Repository cloned
- [ ] Navigated to project directory

```bash
git clone <your-repo-url>
cd ecommerce-api
```

### 2. Create Virtual Environment

- [ ] Virtual environment created
- [ ] Virtual environment activated

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

**Option A: Use existing requirements.txt**

- [ ] All packages installed

```bash
pip install fastapi uvicorn sqlalchemy pymysql pyjwt passlib python-dotenv email-validator pydantic
```

**Option B: Use minimal requirements**

- [ ] Minimal packages installed

```bash
pip install -r requirements-minimal.txt
```

### 4. Database Setup

- [ ] MySQL server running
- [ ] Database created
- [ ] Tables created

```bash
# Option 1: Run SQL file
mysql -u root -p < database_setup.sql

# Option 2: Manual creation
mysql -u root -p
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ecommerce_db;
-- Run the SQL from database_setup.sql
```

**Verification:**

```sql
USE ecommerce_db;
SHOW TABLES;
-- Should show: users, products
```

### 5. Environment Configuration

- [ ] `.env` file created
- [ ] Database credentials configured
- [ ] Secret keys generated
- [ ] All variables set

Create `.env` file:

```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/ecommerce_db
SECRET_KEY=your-generated-secret-key-here
RESET_SECRET_KEY=your-generated-reset-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Generate secure secret keys:**

```python
import secrets
print("SECRET_KEY:", secrets.token_urlsafe(32))
print("RESET_SECRET_KEY:", secrets.token_urlsafe(32))
```

### 6. Static Files Check

- [ ] `static/` folder exists
- [ ] All HTML files present
- [ ] Files accessible

Required files:

- `static/index.html`
- `static/status.html`
- `static/incidents.html`
- `static/docs-landing.html`
- `static/swagger.html`

### 7. Import Verification

- [ ] All modules import correctly

```python
# Test imports
python -c "from database import engine, Base, get_db; print('✓ Database imports OK')"
python -c "from models.user import User; from models.product import Product; print('✓ Model imports OK')"
python -c "from core.security import hash_password; print('✓ Security imports OK')"
python -c "from routers import auth, product, admin; print('✓ Router imports OK')"
```

## 🚀 First Run

### 8. Start Application

- [ ] Application starts without errors
- [ ] Database tables created automatically
- [ ] Server listening on port 8000

```bash
uvicorn main:app --reload
```

Expected output:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
Creating database tables...
Database tables created successfully!
```

### 9. Verify Endpoints

- [ ] Root endpoint accessible (`http://127.0.0.1:8000/`)
- [ ] Health check works (`http://127.0.0.1:8000/health`)
- [ ] Documentation available (`http://127.0.0.1:8000/docs`)

```bash
# Test endpoints
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api
```

### 10. Test User Registration

- [ ] Can register a user
- [ ] User appears in database

```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "TestPass123",
    "role": "buyer"
  }'
```

### 11. Test Authentication

- [ ] Can login successfully
- [ ] Receive JWT token
- [ ] Token works for protected endpoints

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

## 🧪 Run Test Suite

### 12. Execute Tests

- [ ] All tests pass
- [ ] No critical errors

```bash
python tests.py
```

Expected: All green checkmarks ✓

## 🔒 Security Check

### 13. Security Configuration

- [ ] `.env` file in `.gitignore`
- [ ] Strong secret keys set
- [ ] Default passwords changed
- [ ] CORS configured appropriately
- [ ] Database password is strong

### 14. Create `.gitignore`

- [ ] `.gitignore` file created

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Database
*.db
*.sqlite3

# OS
.DS_Store
Thumbs.db
```

## 📊 Monitoring Setup

### 15. Verify Monitoring Features

- [ ] Status page working (`http://127.0.0.1:8000/status`)
- [ ] Metrics updating (`http://127.0.0.1:8000/api/metrics`)
- [ ] Incidents page accessible (`http://127.0.0.1:8000/incidents`)

## 📝 Documentation Check

### 16. Documentation Access

- [ ] Swagger UI loads (`http://127.0.0.1:8000/docs-swagger`)
- [ ] ReDoc loads (`http://127.0.0.1:8000/docs-redoc`)
- [ ] OpenAPI JSON available (`http://127.0.0.1:8000/openapi.json`)
- [ ] Documentation landing page works

## 🎉 Final Verification

### 17. Complete System Test

Run through this workflow:

1. [ ] Register admin user
2. [ ] Register seller user
3. [ ] Register buyer user
4. [ ] Login as seller
5. [ ] Create a product
6. [ ] View products (no auth)
7. [ ] Update product (as seller)
8. [ ] Login as admin
9. [ ] View all users
10. [ ] Deactivate a user
11. [ ] View all products (including inactive)

## 🚨 Troubleshooting

### Common Issues

**Database Connection Error:**

```bash
# Check MySQL is running
sudo systemctl status mysql    # Linux
# Or check Task Manager / Activity Monitor

# Test connection
mysql -u root -p -e "SELECT 1"
```

**Import Errors:**

```bash
# Reinstall packages
pip install --upgrade --force-reinstall -r requirements-minimal.txt
```

**Port Already in Use:**

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:8000 | xargs kill -9
```

**Permission Denied:**

```bash
# Add execute permission
chmod +x main.py
```

## ✅ Setup Complete!

If all items are checked, your E-Commerce API is ready for development!

### Next Steps:

1. Read the API documentation
2. Create your first products
3. Test all endpoints
4. Customize for your needs
5. Deploy to production (see README for deployment guide)

### Quick Reference:

- **API Base URL:** http://127.0.0.1:8000
- **Swagger Docs:** http://127.0.0.1:8000/docs-swagger
- **Status Page:** http://127.0.0.1:8000/status
- **Health Check:** http://127.0.0.1:8000/health

---

**Need Help?** Check the README.md or open an issue on GitHub.
