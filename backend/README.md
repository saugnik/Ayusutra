# AyurSutra Backend API

Comprehensive backend service for the digital Panchakarma management platform, integrating with the existing RAG service for AI functionality.

## 🏗️ Architecture

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **JWT Authentication** - Secure token-based authentication
- **Role-based Access Control** - Patient, Practitioner, Admin roles
- **RAG Integration** - Connected to existing RAG service for AI assistant
- **SQLite/PostgreSQL** - Database support

## 📦 Features

### ✅ Completed Features

1. **User Management**
   - Registration/Login for all user types
   - JWT-based authentication
   - Role-based access control
   - Profile management

2. **Appointment System**
   - Create, read, update appointments
   - Conflict checking
   - Status management

3. **AI Assistant Integration**
   - Connected to existing RAG service
   - Panchakarma knowledge base queries
   - Structured responses

4. **Dashboard APIs**
   - Patient dashboard statistics
   - Practitioner dashboard analytics
   - Admin system overview

5. **Feedback System**
   - Session feedback and ratings
   - Practitioner reviews

6. **Database Models**
   - Comprehensive data models
   - Relationships and constraints
   - Audit logging

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python start.py
```

The startup script will:
- Check dependencies
- Create `.env` file with defaults
- Initialize database tables
- Start the server on `http://localhost:8001`

### 3. Access API Documentation

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## 🔧 Configuration

### Environment Variables

Create a `.env` file or modify the auto-generated one:

```env
# Security
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///./ayursutra.db
# For PostgreSQL: postgresql://username:password@localhost/ayursutra

# RAG Service Integration
RAG_SERVICE_URL=http://localhost:8000

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8001
DEBUG=true

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Database Setup

#### SQLite (Default)
No additional setup required. Database file will be created automatically.

#### PostgreSQL (Production)
1. Install PostgreSQL
2. Create database: `createdb ayursutra`
3. Update `DATABASE_URL` in `.env`
4. Install psycopg2: `pip install psycopg2-binary`

## 🔐 Authentication

### Registration
```bash
POST /auth/register
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "role": "patient|practitioner|admin",
  "phone": "+1234567890"
}
```

### Login
```bash
POST /auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

Returns JWT token for authenticated requests.

## 🤖 AI Assistant Integration

The backend integrates with your existing RAG service:

```bash
POST /ai/ask
Headers: Authorization: Bearer <token>
{
  "query": "What are the benefits of Abhyanga therapy?",
  "top_k": 5
}
```

## 📊 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### Appointments
- `GET /appointments` - List appointments
- `POST /appointments` - Create appointment
- `PUT /appointments/{id}` - Update appointment
- `DELETE /appointments/{id}` - Cancel appointment

### Dashboards
- `GET /patient/dashboard` - Patient statistics
- `GET /practitioner/dashboard` - Practitioner analytics
- `GET /admin/dashboard` - System overview

### AI Assistant
- `POST /ai/ask` - Query AI assistant

### Feedback
- `POST /feedback` - Submit feedback
- `GET /feedback` - Get feedback history

### File Management
- `POST /upload` - Upload files (images, documents)

## 🛡️ Security Features

- **JWT Authentication** with configurable expiration
- **Password Hashing** using bcrypt
- **Role-based Access Control** (RBAC)
- **CORS Protection** with configurable origins
- **Input Validation** using Pydantic schemas
- **SQL Injection Protection** via SQLAlchemy ORM

## 🗄️ Database Schema

### Core Tables
- **users** - Base user information
- **patients** - Patient-specific data
- **practitioners** - Practitioner profiles
- **admins** - Admin accounts
- **appointments** - Appointment scheduling
- **therapy_sessions** - Session details
- **feedback** - User feedback and ratings

### Support Tables
- **notifications** - User notifications
- **therapy_templates** - Therapy procedures
- **system_settings** - Configuration
- **audit_logs** - Activity logging

## 🔄 RAG Service Integration

The backend connects to your existing RAG service (`rag_finetune_service.py`) for AI functionality:

1. **Knowledge Base Queries**: Forward user questions to RAG service
2. **Structured Responses**: Process and format RAG responses
3. **Context Management**: Handle conversation context
4. **Evidence Tracking**: Include source citations

## 📈 Development

### Adding New Endpoints

1. Define Pydantic schemas in `schemas.py`
2. Add database models in `models.py` 
3. Implement endpoints in `main.py`
4. Add authentication/authorization as needed

### Database Migrations

For schema changes:
```bash
# Install Alembic
pip install alembic

# Initialize migrations (first time)
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

## 🚀 Production Deployment

1. **Environment Variables**
   - Set secure `SECRET_KEY`
   - Configure production database
   - Update CORS origins

2. **Database**
   - Use PostgreSQL for production
   - Set up regular backups
   - Configure connection pooling

3. **Security**
   - Enable HTTPS
   - Configure firewall
   - Set up monitoring

4. **Scaling**
   - Use multiple workers: `uvicorn main:app --workers 4`
   - Consider using Gunicorn
   - Set up load balancing

## 📞 API Usage Examples

### Complete User Registration Flow
```python
import requests

# 1. Register a new patient
register_data = {
    "email": "patient@example.com",
    "password": "secure123",
    "full_name": "Jane Patient",
    "role": "patient",
    "phone": "+1234567890",
    "date_of_birth": "1990-01-01T00:00:00",
    "gender": "Female",
    "address": "123 Main St, City, State"
}
response = requests.post("http://localhost:8001/auth/register", json=register_data)
print(response.json())

# 2. Login to get token
login_data = {
    "email": "patient@example.com",
    "password": "secure123"
}
response = requests.post("http://localhost:8001/auth/login", json=login_data)
token = response.json()["access_token"]

# 3. Use token for authenticated requests
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8001/patient/dashboard", headers=headers)
print(response.json())
```

## 🤝 Integration with Frontend

The backend is designed to work seamlessly with your React frontend:

1. **Authentication**: JWT tokens for session management
2. **CORS**: Configured for `http://localhost:3000`
3. **API Structure**: RESTful endpoints matching frontend expectations
4. **Error Handling**: Consistent error responses
5. **Data Validation**: Comprehensive input validation

## 📝 Changelog

### v1.0.0
- ✅ Initial backend implementation
- ✅ User authentication system
- ✅ RAG service integration
- ✅ Database models and schemas
- ✅ Core API endpoints
- ✅ Dashboard statistics
- ✅ File upload support

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Connection Error**
   - Check DATABASE_URL in `.env`
   - Ensure database exists (for PostgreSQL)

3. **RAG Service Connection**
   - Ensure RAG service is running on port 8000
   - Check RAG_SERVICE_URL configuration

4. **CORS Errors**
   - Verify ALLOWED_ORIGINS includes your frontend URL
   - Check frontend is running on expected port

## 📧 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation at `/docs`
3. Verify all services are running
4. Check logs for detailed error messages

---

**Built with ❤️ for AyurSutra - Digital Panchakarma Management Platform**
