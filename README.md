# E-Commerce REST API

A secure, scalable RESTful API for e-commerce applications built with FastAPI, featuring JWT authentication, role-based
access control, and comprehensive product management.

![Python](https://img.shields.io/badge/python-3.13.+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.+-green.svg)
![License](https://img.shields.io/badge/license-MIT-red.svg)

## Features

- **JWT Authentication** - Secure stateless authentication
- **Role-Based Access Control (RBAC)** - Admin, Seller, and Buyer roles
- **Product Management** - Full CRUD operations with soft delete
- **Search & Filter** - Advanced product search capabilities
- **Real-time Metrics** - Live system monitoring dashboard
- **Incident Logging & Tracking** - Built-in incident management system
- **Interactive Documentation** - Swagger UI + Custom Static UI and ReDoc
- **Password Reset** - Secure token-based password recovery

## Tech Stack

- **Framework:** FastAPI
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (PyJWT)
- **Password Hashing:** passlib with PBKDF2-SHA256
- **Database Driver:** PyMySQL

## Prerequisites

- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ShadowAmitendu/eCommerceApis
cd ecommerce-api
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** If you already have a `requirements.txt` with many packages, you can install just the core dependencies:

```bash
pip install fastapi==0.128.0 uvicorn==0.40.0 sqlalchemy==2.0.45 pymysql==1.1.2 pyjwt==2.10.1 passlib==1.7.4 python-dotenv==1.2.1 email-validator==2.3.0 pydantic==2.12.5
```

### 4. Set Up MySQL Database

**Option A: Using MySQL Client**

```bash
mysql -u root -p < database_setup.sql
```

**Option B: Manual Setup**

```sql
CREATE
DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE
ecommerce_db;
```

Then run the SQL file provided in the repository.

### 5. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://root:your_password@localhost/ecommerce_db

# Security Keys (Change these in production!)
SECRET_KEY=your-super-secret-key-change-in-production
RESET_SECRET_KEY=your-reset-secret-key-change-in-production

# JWT Configuration
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**⚠️ Important:** Never commit your `.env` file to version control!

### 6. Initialize Database Tables

The application will automatically create tables on first run via the `lifespan` function. Alternatively, you can verify
table creation:

```bash
# Connect to MySQL
mysql -u root -p

# Switch to database
USE ecommerce_db;

# Show tables
SHOW TABLES;

# Expected output: users, products
```

You can also manually create tables using Python:

```python
python - c
"from database import engine, Base; from models import user, product; Base.metadata.create_all(bind=engine); print('Tables created!')"
```

### 7. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## Quick Start

### 1. Access the API Documentation

- **Home Page:** http://127.0.0.1:8000/
- **Swagger UI:** http://127.0.0.1:8000/docs-swagger
- **ReDoc:** http://127.0.0.1:8000/docs-redoc
- **Status Dashboard:** http://127.0.0.1:8000/status

### 2. Register a User

```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "role": "buyer"
  }'
```

### 3. Login to Get Token

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "email": "john@example.com",
  "role": "buyer"
}
```

### 4. Use the Token

Add the token to your requests:

```bash
curl -X GET "http://127.0.0.1:8000/products/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## API Endpoints

### Authentication

| Method | Endpoint                | Description               | Auth Required |
|--------|-------------------------|---------------------------|---------------|
| POST   | `/auth/register`        | Register new user         | No            |
| POST   | `/auth/login`           | Login and get JWT token   | No            |
| POST   | `/auth/forgot-password` | Request password reset    | No            |
| POST   | `/auth/reset-password`  | Reset password with token | No            |

### Products

| Method | Endpoint         | Description         | Auth Required | Role         |
|--------|------------------|---------------------|---------------|--------------|
| GET    | `/products/`     | Get all products    | No            | -            |
| GET    | `/products/{id}` | Get single product  | No            | -            |
| POST   | `/products/`     | Create product      | Yes           | Seller/Admin |
| PUT    | `/products/{id}` | Update product      | Yes           | Owner/Admin  |
| DELETE | `/products/{id}` | Soft delete product | Yes           | Owner/Admin  |

### Admin

| Method | Endpoint                       | Description         | Auth Required | Role  |
|--------|--------------------------------|---------------------|---------------|-------|
| GET    | `/admin/users`                 | Get all users       | Yes           | Admin |
| GET    | `/admin/users/{id}`            | Get user by ID      | Yes           | Admin |
| PUT    | `/admin/users/{id}/activate`   | Activate user       | Yes           | Admin |
| PUT    | `/admin/users/{id}/deactivate` | Deactivate user     | Yes           | Admin |
| GET    | `/admin/products/all`          | Get all products    | Yes           | Admin |
| DELETE | `/admin/products/{id}`         | Hard delete product | Yes           | Admin |

### System

| Method | Endpoint       | Description       |
|--------|----------------|-------------------|
| GET    | `/health`      | Health check      |
| GET    | `/api/metrics` | Real-time metrics |

## User Roles

### Buyer

- View products
- Search and filter products
- View own profile

### Seller

- All Buyer permissions
- Create products
- Update own products
- Delete own products

### Admin

- All Seller permissions
- Manage all users
- Manage all products
- View system metrics
- Hard delete products

## Testing

Run the comprehensive test suite:

```bash
python tests.py
```

The test suite covers:

- User registration and authentication
- Product CRUD operations
- Role-based access control
- Password reset flow
- Admin operations
- Error handling

## Project Structure

```
ecommerce-api/
│
├── routers/
│   ├── auth.py              # Authentication endpoints
│   ├── product.py           # Product endpoints
│   └── admin.py             # Admin endpoints
│
├── models/
│   ├── user.py              # User model
│   └── product.py           # Product model
│
├── schemas/
│   ├── user.py              # User schemas
│   └── product.py           # Product schemas
│
├── core/
│   └── security.py          # Security utilities
│
├── dependencies/
│   ├── auth.py              # Authentication dependencies
│   └── roles.py             # Role checking dependencies
│
├── static/
│   ├── index.html           # Landing page
│   ├── status.html          # Status dashboard
│   ├── incidents.html       # Incident management
│   ├── docs-landing.html    # Documentation landing
│   └── swagger.html         # Custom Swagger UI
│
├── database.py              # Database configuration
├── main.py                  # Application entry point
├── tests.py                 # Test suite
├── requirements.txt         # Python dependencies
├── database_setup.sql       # Database initialization
└── .env                     # Environment variables
```

## Configuration

### Database Connection

Modify `DATABASE_URL` in `.env`:

```env
# Local MySQL
DATABASE_URL=mysql+pymysql://root:password@localhost/ecommerce_db

# Remote MySQL
DATABASE_URL=mysql+pymysql://user:pass@host:3306/dbname

# MySQL with custom port
DATABASE_URL=mysql+pymysql://user:pass@localhost:3307/dbname
```

### JWT Configuration

```env
# Token expiration time (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Secret keys (use strong random strings in production)
SECRET_KEY=your-secret-key-here
RESET_SECRET_KEY=your-reset-secret-here
```

### Generate Secure Secret Keys

```python
import secrets

print(secrets.token_urlsafe(32))
```

## Production Deployment

### Security Checklist

1. [ ] Change default secret keys
2. [ ] Use strong database passwords
3. [ ] Enable HTTPS/TLS
4. [ ] Set `echo=False` in database.py
5. [ ] Configure CORS properly
6. [ ] Set up rate limiting
7. [ ] Enable database backups
8. [ ] Use environment variables for all secrets
9. [ ] Remove debug endpoints
10. [ ] Implement logging
11. [ ] Set up monitoring

### Environment Variables for Production

```env
DATABASE_URL=mysql+pymysql://prod_user:secure_pass@prod_host/prod_db
SECRET_KEY=production-secret-key-very-long-and-random
RESET_SECRET_KEY=production-reset-key-also-very-random
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
```

### Running with Gunicorn

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## Troubleshooting

### Database Connection Issues

```bash
# Test MySQL connection
mysql -u root -p -e "SELECT 1"

# Check if database exists
mysql -u root -p -e "SHOW DATABASES LIKE 'ecommerce_db'"
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :8000

# Linux/macOS
lsof -i :8000
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
> This doesn't 100% Guarantee your Idea will be Implemented!.

## License

This project is licensed under the MIT License - see
the [LICENSE](https://github.com/ShadowAmitendu/eCommerceApis/blob/master/LICENSE) file for details.

## Support

For issues and questions:

- Issues: [Create a GitHub Issues Ticket!](https://github.com/ShadowAmitendu/eCommerceApis/issues)

## Acknowledgments

- FastAPI framework
- SQLAlchemy ORM
- The Python community

---

**Made with ❤️ using FastAPI**
