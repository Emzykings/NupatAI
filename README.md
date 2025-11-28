# NupatAI Backend API

> **Intelligent. Fast. Helpful.** 🌍  
> Proudly Made in Africa for Africans by Nupat Technologies

NupatAI is a custom AI assistant built for Africa; smart, secure, and deeply aware of the realities, languages, and business environments across the continent.

---

## 🚀 Features

- ✅ **User Authentication** - JWT-based secure authentication
- ✅ **Multi-Chat Support** - Users can have multiple independent chat sessions
- ✅ **AI-Powered Responses** - Integration with NupatAI Model v1
- ✅ **Auto-Title Generation** - Automatic chat titling from first message
- ✅ **Chat History** - Complete conversation persistence
- ✅ **African Context** - AI trained with African-focused data.
- ✅ **RESTful API** - Clean, documented API endpoints
- ✅ **Auto-Generated Docs** - Swagger/OpenAPI documentation

---

## 🏗️ Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL (via Neon/Railway)
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (python-jose)
- **AI**: NupatAI Model v1
- **Migrations**: Alembic
- **Deployment**: Railway/Render

---

## 📁 Project Structure

```
nupat-ai-backend/
├── app/
│   ├── api/
│   │   ├── deps.py              # Shared dependencies
│   │   └── v1/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── chats.py         # Chat management endpoints
│   │       └── messages.py      # Message endpoints
│   ├── core/
│   │   ├── config.py            # Configuration & settings
│   │   ├── security.py          # JWT & password hashing
│   │   └── prompts.py           # AI system prompts
│   ├── db/
│   │   ├── base.py              # SQLAlchemy base
│   │   ├── session.py           # Database session
│   │   └── models.py            # Database models
│   ├── schemas/
│   │   ├── auth.py              # Authentication schemas
│   │   ├── chat.py              # Chat schemas
│   │   └── message.py           # Message schemas
│   ├── services/
│   │   ├── auth_service.py      # Auth business logic
│   │   ├── chat_service.py      # Chat business logic
│   │   ├── message_service.py   # Message business logic
│   │   └── ai_service.py        # NupatAI Model v1 integration
│   └── main.py                  # FastAPI application
├── alembic/                     # Database migrations
├── requirements.txt
├── .env
└── README.md
```

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.11+
- PostgreSQL database
- NupatAI Model v1 API key

### 1. Clone Repository

```bash
git clone https://github.com/Emzykings/NupatAI.git
cd NupatAI
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/nupatai_db
JWT_SECRET_KEY=your-super-secret-key-here
NupatAI_API_KEY=your-NupatAI-api-key
CORS_ORIGINS=http://localhost:3000
```

### 5. Run Database Migrations

```bash
alembic upgrade head
```

### 6. Start Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: `http://localhost:8000`  
Docs available at: `http://localhost:8000/docs`

---

## 🌐 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/signup` | Register new user | No |
| POST | `/api/v1/auth/login` | Login user | No |
| POST | `/api/v1/auth/logout` | Logout user | Yes |
| GET | `/api/v1/auth/me` | Get current user | Yes |

### Chats

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/chats` | Create new chat | Yes |
| GET | `/api/v1/chats` | Get user's chats | Yes |
| GET | `/api/v1/chats/{chat_id}` | Get chat with messages | Yes |
| PATCH | `/api/v1/chats/{chat_id}` | Update chat title | Yes |
| DELETE | `/api/v1/chats/{chat_id}` | Delete chat | Yes |

### Messages

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/chats/{chat_id}/messages` | Send message & get AI response | Yes |
| GET | `/api/v1/chats/{chat_id}/messages` | Get chat messages | Yes |

---

## 📖 API Usage Examples

### 1. User Signup

```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "phone": "+2348012345678",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "phone": "+2348012345678",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

### 2. Create Chat

```bash
curl -X POST "http://localhost:8000/api/v1/chats" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Chat"
  }'
```

### 3. Send Message

```bash
curl -X POST "http://localhost:8000/api/v1/chats/{chat_id}/messages" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "How do I start a tech business in Lagos?"
  }'
```

**Response:**
```json
{
  "user_message": {
    "id": "uuid",
    "role": "user",
    "content": "How do I start a tech business in Lagos?",
    "created_at": "2024-01-15T10:35:00"
  },
  "assistant_message": {
    "id": "uuid",
    "role": "assistant",
    "content": "Starting a tech business in Lagos...",
    "created_at": "2024-01-15T10:35:02"
  },
  "chat": {
    "id": "chat-uuid",
    "title": "Starting Tech Business Lagos",
    "message_count": 2,
    "title_generated": true
  }
}
```

---

## 🚀 Deployment

### Deploy to Railway

1. **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

2. **Login to Railway**:
```bash
railway login
```

3. **Initialize Project**:
```bash
railway init
```

4. **Add PostgreSQL**:
```bash
railway add postgresql
```

5. **Set Environment Variables**:
```bash
railway variables set JWT_SECRET_KEY=your-secret-key
railway variables set NupatAI_API_KEY=your-NupatAI-key
```

6. **Deploy**:
```bash
railway up
```

### Deploy to Render

1. Connect your GitHub repository
2. Create new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add PostgreSQL database
6. Set environment variables
7. Deploy

---

## 📝 Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | Yes | - |
| `NupatAI_API_KEY` | NupatAI API key | Yes | - |
| `JWT_ALGORITHM` | JWT algorithm | No | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time | No | 10080 (7 days) |
| `NupatAI_MODEL` | NupatAI model v1 | No |
| `CORS_ORIGINS` | Allowed CORS origins | No | http://localhost:3000 |
| `ENVIRONMENT` | Environment name | No | development |

---

## 🧪 Testing

### Manual Testing with Swagger UI

1. Start server
2. Open `http://localhost:8000/docs`
3. Test endpoints interactively

### Testing with cURL

See [API Usage Examples](#-api-usage-examples) above

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the Nupat Technologies.

---

## 👥 Contact

**Nupat Technologies**  
Building the future of African AI

- Website: [Your website]
- Email: [Your email]
- GitHub: [Your GitHub]

---

## 🌟 Acknowledgments

- Powered by NupatAI
- Built with FastAPI
- Inspired by African innovation

---

**Made with ❤️ in Africa for Africans and the World 🌍**