# User Management API

A production-grade REST API built with FastAPI, PostgreSQL, and Docker.

## Features

- JWT Authentication (Access + Refresh Tokens)
- Role-Based Access Control (Admin / User)
- Bcrypt password hashing
- Rate limiting (brute-force protection)
- Audit logging
- Alembic database migrations
- Docker + Docker Compose
- Professional Swagger UI

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| Database | PostgreSQL 18 |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Auth | JWT / python-jose |
| Hashing | Bcrypt / Passlib |
| Rate Limiting | SlowAPI |
| Container | Docker + Docker Compose |

## API Endpoints

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | /users/ | Public | Create account |
| POST | /login/ | Public | Login (5/min limit) |
| GET | /users/ | Admin | List all users |
| GET | /users/me/ | Authenticated | Own profile |
| DELETE | /users/{id} | Admin | Delete user |
| POST | /refresh/ | Authenticated | Refresh token |
| POST | /logout/ | Authenticated | Logout |
| POST | /logout-all/ | Authenticated | Logout all devices |

## Getting Started

### Prerequisites
- Python 3.13+
- PostgreSQL 18
- Docker (optional)

### Local Setup

1. Clone the repository
```bash
   git clone https://github.com/Eng-SadatHasakya/user-management-api.git
   cd user-management-api
```

2. Create virtual environment
```bash
   python -m venv venv
   venv\Scripts\activate
```

3. Install dependencies
```bash
   pip install -r requirements.txt
```

4. Create `.env` file
```env
   DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/userdb
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
```

5. Run migrations
```bash
   alembic upgrade head
```

6. Start the server
```bash
   uvicorn app.main:app --reload
```

### Docker Setup

```bash
docker-compose up --build
```

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Author

**Eng. Sadat Hasakya**
- GitHub: [@Eng-SadatHasakya](https://github.com/Eng-SadatHasakya)

## License

MIT