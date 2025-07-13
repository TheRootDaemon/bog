# Bog - FastAPI Micro-Blogging API

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

**A modern, secure micro-blogging API built with FastAPI**

🚀 [The API is LIVE here, you are more than welcome to test it out] 🚀(https://bog-d62w.onrender.com/docs)<br>
📖 [Here's the Swagger Documentations by the way.] 📖(https://bog-d62w.onrender.com/docs)

</div>

## 🌟 What is Bog?

Bog is a straightforward yet powerful FastAPI backend for a micro-blogging social media platform. It provides all the essential features you'd expect from a modern social platform: user registration, secure authentication, post creation and management, social following, post likes, and personalized feeds.

### ✨ Key Features

- 🔐 **Secure JWT Authentication** - Token-based auth with bcrypt password hashing
- 👥 **User Management** - Registration, profiles, and user discovery
- 📝 **Post System** - Create, update, delete, and manage blog posts
- ❤️ **Social Interactions** - Like/unlike posts and follow/unfollow users
- 📱 **Feed System** - Discover users and view user-specific post feeds
- 🚀 **Fast & Modern** - Built with FastAPI for high performance
- 🐳 **Docker Ready** - Containerized for easy deployment
- 📚 **Auto-Generated Docs** - Interactive API documentation with Swagger UI

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens with passlib (bcrypt)
- **Validation**: Pydantic models
- **Containerization**: Docker & Docker Compose
- **Documentation**: Automatic OpenAPI/Swagger docs

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ 
- Git

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/TheRootDaemon/bog.git
   cd bog
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API**
   - API Server: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

### 🐳 Docker Deployment

#### Using Docker Compose (Recommended)

```bash
# Clone and navigate to project
git clone https://github.com/TheRootDaemon/bog.git
cd bog

# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

#### Using Docker directly

```bash
# Build the image
docker build -t bog-api .

# Run the container
docker run -d -p 10000:10000 --name bog bog-api
```

The API will be available at http://localhost:10000

## 📋 API Reference

### 🔑 Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/auth/token` | Login and get JWT token | ❌ |

### 👤 Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/users` | Register a new user | ❌ |
| `POST` | `/users/{user_id}/follow` | Follow a user | ✅ |
| `DELETE` | `/users/{user_id}/unfollow` | Unfollow a user | ✅ |

### 📝 Posts

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/posts` | Create a new post | ✅ |
| `PUT` | `/posts/{post_id}` | Update your post | ✅ |
| `DELETE` | `/posts/{post_id}` | Delete your post | ✅ |
| `POST` | `/posts/{post_id}/like` | Like a post | ✅ |
| `DELETE` | `/posts/{post_id}/like` | Unlike a post | ✅ |

### 📱 Feed

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/feed` | Get random users for discovery | ❌ |
| `GET` | `/feed/{username}` | Get posts by username | ❌ |

### 🏠 General

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/` | API health check | ❌ |
| `GET` | `/user` | Get current user info | ✅ |

## 🔧 Usage Examples

### Register a New User

```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "gender": "male",
    "password": "securepassword123"
  }'
```

### Login and Get Token

```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=securepassword123"
```

### Create a Post

```bash
curl -X POST "http://localhost:8000/posts" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "My First Post",
    "content": "Hello, Bog community! This is my first post."
  }'
```

### Follow a User

```bash
curl -X POST "http://localhost:8000/users/2/follow" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Like a Post

```bash
curl -X POST "http://localhost:8000/posts/1/like" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get User Feed

```bash
curl -X GET "http://localhost:8000/feed/johndoe"
```

## 📁 Project Structure

```
bog/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic request/response models
│   └── routes/
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       ├── registerUser.py  # User registration
│       ├── follow.py        # Follow/unfollow functionality
│       ├── posts.py         # Post management
│       └── feed.py          # Feed endpoints
├── blog.db                  # SQLite database file
├── requirements.txt         # Python dependencies
├── dockerfile              # Docker configuration
├── compose.yml             # Docker Compose configuration
└── README.md               # This file
```

## 🔐 Authentication Flow

1. **Register**: Create a new user account via `/users`
2. **Login**: Get JWT token via `/auth/token`
3. **Authenticate**: Include token in `Authorization: Bearer <token>` header
4. **Access**: Use token to access protected endpoints

## 🌐 Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email`
- `gender`
- `password` (Hashed)

### Posts Table
- `id` (Primary Key)
- `author` (Foreign Key to Users)
- `title`
- `content`

### Relationships
- **Follow**: Many-to-many relationship between users
- **Likes**: Many-to-many relationship between users and posts

## 🚦 Response Codes

| Code | Description |
|------|-------------|
| `200` | Success |
| `201` | Created |
| `400` | Bad Request |
| `401` | Unauthorized |
| `404` | Not Found |
| `422` | Validation Error |

## 🧪 Testing the API

Visit the interactive API documentation at:
- **Live Demo**: https://bog-d62w.onrender.com/docs
- **Local**: http://localhost:8000/docs (when running locally)

The Swagger UI provides a complete interface to test all endpoints with proper authentication.

## 🔧 Configuration

### Environment Variables

Currently, the application uses default configurations. For production deployment, consider setting:

- `SECRET_KEY`: JWT signing secret (currently hardcoded)
- `DATABASE_URL`: Database connection string
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### Database

The application uses SQLite by default with the database file `blog.db`. The database is automatically created when you first run the application.

## 🚀 Deployment

### Production Considerations

1. **Security**: 
   - Change the hardcoded `SECRET_KEY` in `auth.py`
   - Use environment variables for sensitive data
   - Enable HTTPS in production

2. **Database**: 
   - Consider PostgreSQL for production
   - Set up proper backups

3. **Performance**:
   - Use a production ASGI server like Gunicorn with Uvicorn workers
   - Set up proper logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🔗 Links

- **Live API**: https://bog-d62w.onrender.com/docs
- **Repository**: https://github.com/TheRootDaemon/bog
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/

---

<div align="center">
Made with ❤️ using FastAPI
</div>
