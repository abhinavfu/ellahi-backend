# Django REST API - Blog with Authentication

A Django REST API with user registration, login, and blog post management.

## Features

- User registration and login with JWT authentication (supports email or username login)
- User profile updates
- Password reset with email OTP
- Blog post CRUD operations with optional image uploads
- User logout functionality
- CORS enabled for frontend integration
- Token-based authentication

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Start the server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication

- `POST /api/register/` - Register a new user
- `POST /api/login/` - Login user (accepts username or email)
- `POST /api/logout/` - Logout user (authenticated)
- `POST /api/token/refresh/` - Refresh JWT token
- `PUT /api/profile/update/` - Update user profile (authenticated)
- `POST /api/password/reset/` - Request password reset OTP
- `POST /api/password/reset/confirm/` - Confirm password reset with OTP

### Blog Posts

- `GET /api/posts/` - List all posts with categories and tags (public)
- `POST /api/posts/` - Create a new post with optional image, category, and tags (authenticated)
- `GET /api/posts/{id}/` - Get specific post
- `PUT /api/posts/{id}/` - Update post with optional image, category, and tags (author only)
- `DELETE /api/posts/{id}/` - Delete post (author only)

## Post Model Fields

Each blog post contains the following fields:

- **title** - Post title (required)
- **slug** - URL-friendly identifier (auto-generated from title, required)
- **excerpt** - Short summary of the post (optional)
- **content** - Full HTML content of the post (required)
- **image** - Featured image for the post (optional)
- **category** - Post category (optional, related to Category model)
- **tags** - Tags for the post (optional, many-to-many relationship with Tag model)
- **author** - Author of the post (linked to User model)
- **meta_description** - SEO meta description (optional, max 160 characters)
- **created_at** - Post creation timestamp (auto-generated)
- **updated_at** - Last update timestamp (auto-updated)

## Usage Examples

### Register User
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
```

### Login (with username or email)
```bash
# Login with username
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'

# Login with email
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test@example.com", "password": "password123"}'
```

### Logout
```bash
curl -X POST http://127.0.0.1:8000/api/logout/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Update Profile
```bash
curl -X PUT http://127.0.0.1:8000/api/profile/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"username": "newusername", "email": "newemail@example.com", "current_password": "password123"}'
```

### Request Password Reset
```bash
curl -X POST http://127.0.0.1:8000/api/password/reset/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

### Confirm Password Reset
```bash
curl -X POST http://127.0.0.1:8000/api/password/reset/confirm/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "otp": "123456", "new_password": "newpassword123"}'
```

### Create Post (include JWT token in header)
```bash
# With all fields (JSON)
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Understanding Land Transfer Tax in Ontario",
    "slug": "understanding-land-transfer-tax-ontario",
    "excerpt": "A comprehensive guide to Ontario land transfer taxes",
    "content": "<h2>What is Land Transfer Tax?</h2><p>When you purchase a property...</p>",
    "category_id": 1,
    "tag_ids": [1, 2],
    "meta_description": "Learn about Ontario and Toronto land transfer taxes, current rates, and rebates."
  }'

# With image and all fields (multipart/form-data)
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "title=My First Post" \
  -F "slug=my-first-post" \
  -F "excerpt=This is a short excerpt" \
  -F "content=<p>This is the full HTML content of my post.</p>" \
  -F "image=@path/to/your/image.jpg" \
  -F "category_id=1" \
  -F "tag_ids=1" \
  -F "tag_ids=2" \
  -F "meta_description=Short description for SEO"

# Minimal post (only required fields)
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "My Post",
    "slug": "my-post",
    "content": "<p>My content here</p>"
  }'
```

### Update Post
```bash
curl -X PUT http://127.0.0.1:8000/api/posts/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Updated Title",
    "excerpt": "Updated excerpt",
    "content": "<p>Updated content</p>",
    "category_id": 2
  }'
```

### Get Posts
```bash
curl http://127.0.0.1:8000/api/posts/

# Get specific post
curl http://127.0.0.1:8000/api/posts/1/
```

## Database Models

### Post Model
The main model for blog posts with the following relationships:
- **author**: ForeignKey to Django User model (required)
- **category**: ForeignKey to Category model (optional)
- **tags**: ManyToMany relationship with Tag model (optional)

### Category Model
Used to organize blog posts into categories:
- **name**: Category name (unique)
- **slug**: URL-friendly identifier (auto-generated)
- **description**: Category description (optional)

### Tag Model
Used to tag blog posts:
- **name**: Tag name (unique)
- **slug**: URL-friendly identifier (auto-generated)

## Admin Panel

Access the Django admin panel at `http://127.0.0.1:8000/admin/` with your superuser credentials.

Create a superuser if you haven't already:
```bash
python manage.py createsuperuser
```

The admin panel provides full management for:
- Blog Posts (with organized fieldsets for content, media, and metadata)
- Categories (with auto-slug generation)
- Tags (with auto-slug generation)

### Using Slugs
When creating posts, categories, or tags, the slug field is auto-generated from the name/title in the admin panel. You can also provide a custom slug. The slug must be unique and URL-friendly (lowercase, hyphens only).

### Working with Categories and Tags
1. Create categories first via the admin panel
2. Create tags that will be referenced in your posts
3. When creating a post via the API, use `category_id` and `tag_ids` (array of IDs)

## Response Examples

### List Posts Response
```json
{
  "count": 6,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Understanding Land Transfer Tax in Ontario",
      "slug": "understanding-land-transfer-tax-ontario",
      "excerpt": "A comprehensive guide to Ontario and Toronto land transfer taxes...",
      "content": "<h2>What is Land Transfer Tax?</h2>...",
      "image": "http://127.0.0.1:8000/media/blog_images/image.jpg",
      "category": {
        "id": 1,
        "name": "Real Estate Law",
        "slug": "real-estate-law",
        "description": "Posts about real estate law..."
      },
      "tags": [
        {
          "id": 1,
          "name": "land transfer tax",
          "slug": "land-transfer-tax"
        },
        {
          "id": 2,
          "name": "real estate",
          "slug": "real-estate"
        }
      ],
      "author": "admin",
      "meta_description": "Learn about Ontario and Toronto land transfer taxes...",
      "created_at": "2026-01-15T10:00:00Z",
      "updated_at": "2026-01-15T10:00:00Z"
    }
  ]
}
```

## Notes

- All timestamps are in UTC (ISO 8601 format)
- Image uploads are stored in the `media/blog_images/` directory
- The `slug` field must be unique across all posts
- Categories and tags can be managed through the admin panel or via direct API calls (if endpoints are created)
- For production, properly configure media file storage (cloud storage, CDN, etc.)