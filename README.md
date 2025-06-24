# Bog - Simple FastAPI Social Media Backend

## What is Bog?
Bog is a straightforward FastAPI backend for a micro bloggin site. It lets users register, post content, follow others, like posts, and view feeds, with secure JWT authentication.

## Quick Setup

1. **Clone the Repo**
   ```bash
   git clone https://github.com/TheRootDaemon/bog.git
   cd bog
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the App**
   ```bash
   uvicorn main:app --reload
   ```
   Visit `http://localhost:8000/docs` for interactive API docs.

## Key API Endpoints

- **Auth**
  - `POST /auth/token`: Get a JWT token (login).

- **Users**
  - `POST /users/register`: Create a new user.
  - `POST /users/follow/{user_id}`: Follow a user.
  - `DELETE /users/unfollow/{user_id}`: Unfollow a user.

- **Posts**
  - `POST /posts/createPost`: Create a post.
  - `PUT /posts/updatePost/{post_id}`: Update a post.
  - `DELETE /posts/deletePost/{post_id}`: Delete a post.
  - `POST /posts/likePost/{post_id}`: Like a post.
  - `DELETE /posts/unlikePost/{post_id}`: Unlike a post.

- **Feed**
  - `GET /feed/getUsers`: Get users for feed.
  - `GET /feed/getPosts/{username}`: Get a user's posts.

- **Default**
  - `GET /`: Get authenticated user details.

## Example Usage

Register a user:
```bash
curl -X POST "http://localhost:8000/users/register" -H "Content-Type: application/json" -d '{"username": "testuser", "password": "password123"}'
```

Get a token:
```bash
curl -X POST "http://localhost:8000/auth/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=testuser&password=password123"
```

I might Dockerize it soon....
