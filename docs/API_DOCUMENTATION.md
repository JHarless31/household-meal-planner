# API Documentation

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Authentication Endpoints](#authentication-endpoints)
4. [Recipe Endpoints](#recipe-endpoints)
5. [Inventory Endpoints](#inventory-endpoints)
6. [Rating Endpoints](#rating-endpoints)
7. [Menu Planning Endpoints](#menu-planning-endpoints)
8. [Shopping List Endpoints](#shopping-list-endpoints)
9. [Notification Endpoints](#notification-endpoints)
10. [Admin Endpoints](#admin-endpoints)
11. [Error Handling](#error-handling)

---

## Overview

### Base URL

```
Development: http://localhost:8000/api
Production:  https://meal-planner.local/api
```

### Authentication

Most endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

Alternatively, the token is stored in an httpOnly cookie after login.

### Response Formats

All responses are in JSON format.

**Success Response:**
```json
{
  "data": { ... },
  "message": "Success"
}
```

**Error Response:**
```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE"
}
```

### Pagination

List endpoints support pagination with the following query parameters:

- `page` (integer, default: 1): Page number
- `limit` (integer, default: 20, max: 100): Items per page

**Paginated Response:**
```json
{
  "recipes": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total_pages": 5,
    "total_items": 98
  }
}
```

### Rate Limiting

- Login attempts: 5 per 15 minutes
- Recipe scraping: 1 per 5 seconds per domain
- Other endpoints: No rate limit

---

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

**Authentication Flow:**

1. User logs in with username and password
2. Server validates credentials
3. Server generates JWT token
4. Token is returned in response and stored in httpOnly cookie
5. Client includes token in subsequent requests
6. Server validates token on protected endpoints

**Token Expiration:** 24 hours (configurable)

**Refresh:** Tokens are not automatically refreshed. User must log in again after expiration.

---

## Authentication Endpoints

### POST /auth/register

Create a new user account.

**Authorization:** None (public endpoint)

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Request Parameters:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| username | string | Yes | 3-50 chars, alphanumeric + underscore | Unique username |
| email | string | Yes | Valid email format | Unique email address |
| password | string | Yes | Min 8 chars | User password (will be hashed) |

**Success Response (201 Created):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "username": "john_doe",
  "email": "john@example.com",
  "role": "user",
  "is_active": true,
  "created_at": "2025-10-01T12:00:00Z"
}
```

**Error Responses:**

- **400 Bad Request**: Invalid input (e.g., username too short)
```json
{
  "detail": "Username must be at least 3 characters"
}
```

- **409 Conflict**: Username or email already exists
```json
{
  "detail": "Username already registered"
}
```

---

### POST /auth/login

Authenticate a user and create a session.

**Authorization:** None (public endpoint)

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123"
}
```

**Request Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| username | string | Yes | Username |
| password | string | Yes | User password |

**Success Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "username": "john_doe",
    "email": "john@example.com",
    "role": "user",
    "is_active": true
  }
}
```

**Headers:**
```
Set-Cookie: session=abc123; Path=/; HttpOnly; Secure; SameSite=Strict
```

**Error Responses:**

- **401 Unauthorized**: Invalid credentials
```json
{
  "detail": "Incorrect username or password"
}
```

- **400 Bad Request**: Inactive account
```json
{
  "detail": "Inactive user"
}
```

- **429 Too Many Requests**: Rate limit exceeded (5 attempts per 15 min)
```json
{
  "detail": "Too many login attempts. Please try again later."
}
```

---

### POST /auth/logout

End the current user session.

**Authorization:** Required

**Request Body:** None

**Success Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

---

### GET /auth/me

Get information about the currently authenticated user.

**Authorization:** Required

**Request Body:** None

**Success Response (200 OK):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "username": "john_doe",
  "email": "john@example.com",
  "role": "user",
  "is_active": true,
  "created_at": "2025-10-01T12:00:00Z",
  "last_login": "2025-10-01T14:30:00Z"
}
```

**Error Responses:**

- **401 Unauthorized**: Invalid or expired token
```json
{
  "detail": "Could not validate credentials"
}
```

---

## Recipe Endpoints

### GET /recipes

List recipes with pagination and filters.

**Authorization:** Required

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| page | integer | No | 1 | Page number |
| limit | integer | No | 20 | Items per page (max 100) |
| search | string | No | - | Search in title/description |
| tags | string | No | - | Comma-separated tags |
| difficulty | string | No | - | Filter by difficulty (easy/medium/hard) |
| filter | string | No | - | Special filters (favorites/never_tried/not_recent) |

**Example Request:**
```
GET /recipes?page=1&limit=20&search=chicken&tags=italian,easy&difficulty=easy
```

**Success Response (200 OK):**
```json
{
  "recipes": [
    {
      "id": "abc123...",
      "title": "Chicken Parmesan",
      "description": "Classic Italian dish",
      "servings": 4,
      "prep_time_minutes": 20,
      "cook_time_minutes": 30,
      "difficulty": "easy",
      "current_version": 2,
      "times_cooked": 5,
      "last_cooked_date": "2025-09-15",
      "is_favorite": true,
      "created_at": "2025-01-01T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total_pages": 3,
    "total_items": 54
  }
}
```

---

### POST /recipes

Create a new recipe.

**Authorization:** Required

**Request Body:**
```json
{
  "title": "Spaghetti Carbonara",
  "description": "Traditional Italian pasta dish",
  "servings": 4,
  "prep_time_minutes": 10,
  "cook_time_minutes": 15,
  "difficulty": "medium",
  "ingredients": [
    {
      "quantity": 1,
      "unit": "pound",
      "name": "spaghetti",
      "notes": null
    },
    {
      "quantity": 4,
      "unit": "whole",
      "name": "eggs",
      "notes": "room temperature"
    },
    {
      "quantity": 1,
      "unit": "cup",
      "name": "parmesan cheese",
      "notes": "grated"
    }
  ],
  "instructions": [
    "Boil pasta in salted water until al dente",
    "Beat eggs and mix with cheese",
    "Drain pasta and toss with egg mixture",
    "Serve immediately with black pepper"
  ],
  "tags": ["italian", "pasta", "quick-meal"],
  "source_url": null
}
```

**Request Parameters:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| title | string | Yes | 1-200 chars | Recipe title |
| description | string | No | Max 500 chars | Recipe description |
| servings | integer | Yes | > 0 | Number of servings |
| prep_time_minutes | integer | Yes | >= 0 | Preparation time |
| cook_time_minutes | integer | Yes | >= 0 | Cooking time |
| difficulty | string | Yes | easy/medium/hard | Difficulty level |
| ingredients | array | Yes | At least 1 | List of ingredients |
| instructions | array | Yes | At least 1 | Step-by-step instructions |
| tags | array | No | - | Recipe tags |
| source_url | string | No | Valid URL | Source URL if scraped |

**Ingredient Object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| quantity | number | Yes | Amount (e.g., 2.5) |
| unit | string | Yes | Unit of measurement |
| name | string | Yes | Ingredient name |
| notes | string | No | Additional notes |

**Success Response (201 Created):**
```json
{
  "id": "def456...",
  "title": "Spaghetti Carbonara",
  "description": "Traditional Italian pasta dish",
  "servings": 4,
  "prep_time_minutes": 10,
  "cook_time_minutes": 15,
  "difficulty": "medium",
  "current_version": 1,
  "times_cooked": 0,
  "last_cooked_date": null,
  "is_deleted": false,
  "created_at": "2025-10-01T15:00:00Z",
  "updated_at": "2025-10-01T15:00:00Z"
}
```

**Error Responses:**

- **400 Bad Request**: Invalid input
```json
{
  "detail": "At least one instruction is required"
}
```

---

### GET /recipes/{recipeId}

Get a specific recipe by ID.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| recipeId | UUID | Yes | Recipe ID |

**Success Response (200 OK):**
```json
{
  "id": "abc123...",
  "title": "Chicken Parmesan",
  "description": "Classic Italian dish",
  "servings": 4,
  "prep_time_minutes": 20,
  "cook_time_minutes": 30,
  "difficulty": "easy",
  "current_version": 2,
  "times_cooked": 5,
  "last_cooked_date": "2025-09-15",
  "ingredients": [
    {
      "id": "ing1...",
      "quantity": 2,
      "unit": "pieces",
      "name": "chicken breast",
      "notes": "pounded thin"
    }
  ],
  "instructions": [
    "Preheat oven to 400°F",
    "Bread chicken breasts",
    "..."
  ],
  "tags": ["italian", "chicken", "easy"],
  "source_url": null,
  "created_at": "2025-01-01T12:00:00Z",
  "updated_at": "2025-03-15T10:30:00Z"
}
```

**Error Responses:**

- **404 Not Found**: Recipe doesn't exist
```json
{
  "detail": "Recipe not found"
}
```

---

### PUT /recipes/{recipeId}

Update a recipe (creates a new version).

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| recipeId | UUID | Yes | Recipe ID |

**Request Body:**
Same as POST /recipes (all fields required)

**Success Response (200 OK):**
```json
{
  "id": "abc123...",
  "title": "Chicken Parmesan (Updated)",
  "current_version": 3,
  "updated_at": "2025-10-01T16:00:00Z",
  ...
}
```

**Notes:**
- Updating a recipe creates a new version
- Old versions are preserved
- `current_version` is incremented

**Error Responses:**

- **404 Not Found**: Recipe doesn't exist

---

### DELETE /recipes/{recipeId}

Delete a recipe (soft delete).

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| recipeId | UUID | Yes | Recipe ID |

**Success Response (204 No Content):**
No response body.

**Notes:**
- This is a soft delete (recipe is marked as deleted, not removed from database)
- Deleted recipes are hidden from lists but can be recovered by admin

**Error Responses:**

- **404 Not Found**: Recipe doesn't exist

---

### POST /recipes/scrape

Scrape a recipe from a URL.

**Authorization:** Required

**Request Body:**
```json
{
  "url": "https://www.allrecipes.com/recipe/12345/chicken-parmesan/"
}
```

**Request Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| url | string | Yes | Recipe URL to scrape |

**Success Response (200 OK):**
```json
{
  "scraped_data": {
    "title": "Chicken Parmesan",
    "description": "Classic Italian-American dish",
    "servings": 4,
    "prep_time_minutes": 20,
    "cook_time_minutes": 30,
    "difficulty": "medium",
    "ingredients": [...],
    "instructions": [...]
  },
  "source_url": "https://www.allrecipes.com/recipe/12345/chicken-parmesan/",
  "warnings": [
    "Unable to extract image"
  ]
}
```

**Notes:**
- Scraped data is returned but not saved
- User can review and edit before creating recipe
- Not all websites are supported
- Rate limited to 1 request per 5 seconds per domain

**Error Responses:**

- **400 Bad Request**: Invalid URL or scraping failed
```json
{
  "detail": "Could not scrape recipe from this URL"
}
```

- **429 Too Many Requests**: Rate limit exceeded
```json
{
  "detail": "Rate limit exceeded. Please wait before scraping again."
}
```

---

### GET /recipes/suggestions

Get recipe suggestions based on various strategies.

**Authorization:** Required

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| strategy | string | No | rotation | Suggestion strategy |
| limit | integer | No | 10 | Number of suggestions (max 50) |

**Strategies:**
- `rotation`: Recipes not cooked recently or never tried
- `favorites`: Household favorites based on ratings
- `never_tried`: Recipes never cooked (times_cooked = 0)
- `available_inventory`: Recipes with most ingredients in stock
- `seasonal`: Recipes tagged for current season
- `quick_meals`: Recipes under 30 minutes total time

**Example Request:**
```
GET /recipes/suggestions?strategy=available_inventory&limit=5
```

**Success Response (200 OK):**
```json
{
  "suggestions": [
    {
      "recipe_id": "abc123...",
      "title": "Chicken Stir Fry",
      "description": "Quick and easy stir fry",
      "prep_time_minutes": 10,
      "cook_time_minutes": 12,
      "difficulty": "easy",
      "reason": "8/10 ingredients available",
      "match_percentage": 80.0,
      "days_since_cooked": null
    }
  ],
  "strategy": "available_inventory",
  "count": 5
}
```

**Suggestion Fields:**

| Field | Type | Description |
|-------|------|-------------|
| recipe_id | UUID | Recipe ID |
| title | string | Recipe title |
| reason | string | Why this recipe is suggested |
| match_percentage | number | Percentage of ingredients available (inventory strategy only) |
| days_since_cooked | integer | Days since last cooked (rotation strategy only) |

---

### GET /recipes/{recipeId}/versions

Get version history for a recipe.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| recipeId | UUID | Yes | Recipe ID |

**Success Response (200 OK):**
```json
{
  "versions": [
    {
      "version_number": 2,
      "created_at": "2025-03-15T10:30:00Z",
      "created_by": {
        "id": "user123...",
        "username": "john_doe"
      },
      "changes_summary": "Updated cooking instructions"
    },
    {
      "version_number": 1,
      "created_at": "2025-01-01T12:00:00Z",
      "created_by": {
        "id": "user123...",
        "username": "john_doe"
      },
      "changes_summary": "Initial version"
    }
  ]
}
```

---

## Inventory Endpoints

### GET /inventory

List all inventory items with filters.

**Authorization:** Required

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| category | string | No | - | Filter by category |
| location | string | No | - | Filter by location |

**Categories:** produce, dairy, meat, seafood, grains, pantry, condiments, spices, frozen, other

**Locations:** fridge, freezer, pantry, counter, cabinet, other

**Success Response (200 OK):**
```json
{
  "items": [
    {
      "id": "inv123...",
      "name": "Milk",
      "quantity": 2,
      "unit": "gallon",
      "category": "dairy",
      "location": "fridge",
      "expiration_date": "2025-10-15",
      "min_quantity_threshold": 1,
      "notes": "Whole milk",
      "created_at": "2025-09-01T10:00:00Z",
      "updated_at": "2025-10-01T08:00:00Z"
    }
  ]
}
```

---

### POST /inventory

Add a new inventory item.

**Authorization:** Required

**Request Body:**
```json
{
  "name": "Milk",
  "quantity": 2,
  "unit": "gallon",
  "category": "dairy",
  "location": "fridge",
  "expiration_date": "2025-10-15",
  "min_quantity_threshold": 1,
  "notes": "Whole milk"
}
```

**Request Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Item name |
| quantity | number | Yes | Current quantity |
| unit | string | Yes | Unit of measurement |
| category | string | No | Item category |
| location | string | No | Storage location |
| expiration_date | date | No | Expiration date (YYYY-MM-DD) |
| min_quantity_threshold | number | No | Low stock threshold |
| notes | string | No | Additional notes |

**Success Response (201 Created):**
```json
{
  "id": "inv123...",
  "name": "Milk",
  "quantity": 2,
  "unit": "gallon",
  "category": "dairy",
  "location": "fridge",
  "expiration_date": "2025-10-15",
  "min_quantity_threshold": 1,
  "notes": "Whole milk",
  "created_at": "2025-10-01T10:00:00Z",
  "updated_at": "2025-10-01T10:00:00Z"
}
```

---

### GET /inventory/{itemId}

Get a specific inventory item.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| itemId | UUID | Yes | Inventory item ID |

**Success Response (200 OK):**
Same as POST /inventory response

**Error Responses:**

- **404 Not Found**: Item doesn't exist

---

### PUT /inventory/{itemId}

Update an inventory item.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| itemId | UUID | Yes | Inventory item ID |

**Request Body:**
Same as POST /inventory

**Success Response (200 OK):**
Updated item object

**Notes:**
- Quantity changes are tracked in inventory history
- If quantity drops below `min_quantity_threshold`, a low stock notification is generated

---

### DELETE /inventory/{itemId}

Delete an inventory item.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| itemId | UUID | Yes | Inventory item ID |

**Success Response (204 No Content):**
No response body

**Notes:**
- This is a permanent delete (not soft delete)

---

### GET /inventory/low-stock

Get items below their minimum quantity threshold.

**Authorization:** Required

**Success Response (200 OK):**
```json
{
  "items": [
    {
      "id": "inv123...",
      "name": "Milk",
      "quantity": 0.5,
      "unit": "gallon",
      "min_quantity_threshold": 1,
      "deficit": 0.5,
      "message": "Below minimum threshold by 0.5 gallon"
    }
  ]
}
```

---

### GET /inventory/expiring

Get items expiring soon.

**Authorization:** Required

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| days | integer | No | 7 | Days ahead to check |

**Example Request:**
```
GET /inventory/expiring?days=3
```

**Success Response (200 OK):**
```json
{
  "items": [
    {
      "id": "inv123...",
      "name": "Milk",
      "quantity": 1,
      "unit": "gallon",
      "expiration_date": "2025-10-03",
      "days_until_expiration": 2,
      "urgency": "high"
    }
  ]
}
```

**Urgency Levels:**
- `critical`: Expires in 1 day or less
- `high`: Expires in 2-3 days
- `medium`: Expires in 4-7 days
- `low`: Expires in 8+ days

---

### GET /inventory/{itemId}/history

Get history of changes for an inventory item.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| itemId | UUID | Yes | Inventory item ID |

**Success Response (200 OK):**
```json
{
  "history": [
    {
      "id": "hist123...",
      "change_type": "deduction",
      "previous_quantity": 2,
      "new_quantity": 1,
      "change_amount": -1,
      "reason": "Used in recipe: Pancakes",
      "recipe_id": "recipe123...",
      "created_at": "2025-10-01T08:30:00Z"
    },
    {
      "id": "hist124...",
      "change_type": "addition",
      "previous_quantity": 1,
      "new_quantity": 2,
      "change_amount": 1,
      "reason": "Restocked",
      "recipe_id": null,
      "created_at": "2025-09-28T14:00:00Z"
    }
  ]
}
```

---

## Rating Endpoints

### GET /recipes/{recipeId}/ratings

Get all ratings for a recipe.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| recipeId | UUID | Yes | Recipe ID |

**Success Response (200 OK):**
```json
{
  "ratings": [
    {
      "id": "rating123...",
      "user_id": "user456...",
      "username": "john_doe",
      "rating_value": true,
      "created_at": "2025-09-15T12:00:00Z"
    }
  ],
  "summary": {
    "thumbs_up": 8,
    "thumbs_down": 2,
    "total": 10,
    "percentage_positive": 80.0,
    "is_favorite": true
  }
}
```

**Rating Value:**
- `true`: Thumbs up (liked)
- `false`: Thumbs down (didn't like)

---

### POST /recipes/{recipeId}/ratings

Create or update a rating for a recipe.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| recipeId | UUID | Yes | Recipe ID |

**Request Body:**
```json
{
  "rating_value": true
}
```

**Request Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| rating_value | boolean | Yes | true = thumbs up, false = thumbs down |

**Success Response (201 Created):**
```json
{
  "id": "rating123...",
  "user_id": "user456...",
  "recipe_id": "recipe789...",
  "rating_value": true,
  "created_at": "2025-10-01T15:00:00Z"
}
```

**Notes:**
- If user has already rated, the existing rating is updated
- Users can only have one rating per recipe

---

### DELETE /recipes/{recipeId}/ratings/{ratingId}

Delete a rating.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| recipeId | UUID | Yes | Recipe ID |
| ratingId | UUID | Yes | Rating ID |

**Success Response (204 No Content):**
No response body

**Authorization:**
- Users can only delete their own ratings
- Admins can delete any rating

---

## Menu Planning Endpoints

### GET /menu-plans

List all menu plans for the current user.

**Authorization:** Required

**Success Response (200 OK):**
```json
{
  "menu_plans": [
    {
      "id": "plan123...",
      "name": "Week of Oct 1",
      "week_start_date": "2025-09-30",
      "is_active": true,
      "meal_count": 14,
      "created_at": "2025-09-28T10:00:00Z"
    }
  ]
}
```

---

### POST /menu-plans

Create a new menu plan.

**Authorization:** Required

**Request Body:**
```json
{
  "name": "Week of Oct 1",
  "week_start_date": "2025-09-30",
  "is_active": true
}
```

**Request Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | No | Plan name (optional) |
| week_start_date | date | Yes | Monday of the week (YYYY-MM-DD) |
| is_active | boolean | No | Set as active plan (default: false) |

**Success Response (201 Created):**
```json
{
  "id": "plan123...",
  "user_id": "user456...",
  "name": "Week of Oct 1",
  "week_start_date": "2025-09-30",
  "is_active": true,
  "created_at": "2025-10-01T10:00:00Z",
  "updated_at": "2025-10-01T10:00:00Z"
}
```

**Notes:**
- `week_start_date` must be a Monday
- Only one plan can be active per user at a time

---

### GET /menu-plans/{planId}

Get a specific menu plan with all meals.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| planId | UUID | Yes | Menu plan ID |

**Success Response (200 OK):**
```json
{
  "id": "plan123...",
  "name": "Week of Oct 1",
  "week_start_date": "2025-09-30",
  "is_active": true,
  "meals": [
    {
      "id": "meal123...",
      "recipe_id": "recipe456...",
      "recipe_title": "Chicken Parmesan",
      "day_of_week": "monday",
      "meal_type": "dinner",
      "servings": 4,
      "is_cooked": false,
      "notes": null
    }
  ],
  "created_at": "2025-09-28T10:00:00Z"
}
```

**Day of Week Values:** monday, tuesday, wednesday, thursday, friday, saturday, sunday

**Meal Type Values:** breakfast, lunch, dinner, snack

---

### PUT /menu-plans/{planId}

Update a menu plan.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| planId | UUID | Yes | Menu plan ID |

**Request Body:**
```json
{
  "name": "Updated Week Name",
  "is_active": true
}
```

**Success Response (200 OK):**
Updated menu plan object

---

### DELETE /menu-plans/{planId}

Delete a menu plan and all its meals.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| planId | UUID | Yes | Menu plan ID |

**Success Response (204 No Content):**
No response body

---

### POST /menu-plans/{planId}/meals/{mealId}/cooked

Mark a meal as cooked.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| planId | UUID | Yes | Menu plan ID |
| mealId | UUID | Yes | Planned meal ID |

**Request Body:** None

**Success Response (200 OK):**
```json
{
  "message": "Meal marked as cooked",
  "meal": {
    "id": "meal123...",
    "is_cooked": true,
    "cooked_at": "2025-10-01T18:30:00Z"
  },
  "inventory_updated": true
}
```

**Side Effects:**
- Recipe's `times_cooked` is incremented
- Recipe's `last_cooked_date` is updated to today
- Inventory is auto-deducted for recipe ingredients
- Inventory history is created for each deduction

---

### POST /menu-plans/{planId}/copy

Copy a menu plan to a new week.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| planId | UUID | Yes | Menu plan ID to copy |

**Request Body:**
```json
{
  "new_week_start_date": "2025-10-07",
  "new_plan_name": "Week of Oct 7"
}
```

**Request Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| new_week_start_date | date | Yes | Monday of new week (YYYY-MM-DD) |
| new_plan_name | string | No | Name for new plan |

**Success Response (201 Created):**
```json
{
  "id": "newplan123...",
  "name": "Week of Oct 7",
  "week_start_date": "2025-10-07",
  "meal_count": 14,
  "copied_from": "plan123...",
  "created_at": "2025-10-01T16:00:00Z"
}
```

**Notes:**
- All meals are copied to new plan
- All meals are marked as "not cooked"
- Day assignments remain the same

---

### POST /menu-plans/suggest

Auto-generate a weekly menu plan using recipe suggestions.

**Authorization:** Required

**Request Body:**
```json
{
  "week_start_date": "2025-10-07",
  "plan_name": "Auto-Generated Week",
  "strategy": "rotation",
  "meal_types": ["lunch", "dinner"],
  "servings_per_meal": 4
}
```

**Request Parameters:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| week_start_date | date | Yes | - | Monday of the week |
| plan_name | string | No | Auto | Plan name |
| strategy | string | No | rotation | Suggestion strategy |
| meal_types | array | No | [lunch, dinner] | Meal types to generate |
| servings_per_meal | integer | No | 4 | Servings for each meal |

**Success Response (201 Created):**
```json
{
  "id": "plan123...",
  "name": "Auto-Generated Week",
  "week_start_date": "2025-10-07",
  "meals": [
    {
      "day_of_week": "monday",
      "meal_type": "lunch",
      "recipe_id": "recipe1...",
      "recipe_title": "Chicken Salad",
      "servings": 4
    },
    {
      "day_of_week": "monday",
      "meal_type": "dinner",
      "recipe_id": "recipe2...",
      "recipe_title": "Spaghetti Carbonara",
      "servings": 4
    }
  ],
  "total_meals": 14,
  "created_at": "2025-10-01T17:00:00Z"
}
```

**Notes:**
- Generates meals for all 7 days
- Ensures variety (no recipe used twice)
- Uses specified suggestion strategy

---

## Shopping List Endpoints

### GET /shopping-list/{planId}

Generate a shopping list for a menu plan.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| planId | UUID | Yes | Menu plan ID |

**Success Response (200 OK):**
```json
{
  "menu_plan_id": "plan123...",
  "menu_plan_name": "Week of Oct 1",
  "generated_at": "2025-10-01T10:00:00Z",
  "items": {
    "Produce": [
      {
        "name": "Tomatoes",
        "total_needed": 5,
        "current_stock": 2,
        "net_needed": 3,
        "unit": "whole",
        "status": "need_to_buy"
      }
    ],
    "Dairy": [
      {
        "name": "Milk",
        "total_needed": 4,
        "current_stock": 1,
        "net_needed": 3,
        "unit": "cup",
        "status": "need_to_buy"
      }
    ],
    "Meat": [],
    "Pantry": [
      {
        "name": "Flour",
        "total_needed": 2,
        "current_stock": 5,
        "net_needed": 0,
        "unit": "cup",
        "status": "sufficient_stock"
      }
    ]
  },
  "summary": {
    "total_items": 25,
    "items_to_buy": 18,
    "items_in_stock": 7
  }
}
```

**Status Values:**
- `need_to_buy`: Current stock < total needed
- `sufficient_stock`: Current stock >= total needed
- `not_in_inventory`: Item not tracked in inventory

**Notes:**
- Aggregates ingredients from all uncooked meals
- Checks current inventory
- Calculates net deficit
- Groups by category
- Only items with net_needed > 0 are shown in the main list

---

## Notification Endpoints

### GET /notifications

Get notifications for current user.

**Authorization:** Required

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| is_read | boolean | No | - | Filter by read status |
| type | string | No | - | Filter by notification type |
| limit | integer | No | 50 | Max notifications to return |

**Notification Types:** low_stock, expiring, meal_reminder, recipe_update, system

**Success Response (200 OK):**
```json
{
  "notifications": [
    {
      "id": "notif123...",
      "type": "low_stock",
      "title": "Low stock: Milk",
      "message": "Milk is running low (0.5 gallon remaining, minimum 1 gallon)",
      "link": "/inventory/inv123",
      "is_read": false,
      "created_at": "2025-10-01T08:00:00Z"
    }
  ]
}
```

---

### GET /notifications/unread-count

Get count of unread notifications.

**Authorization:** Required

**Success Response (200 OK):**
```json
{
  "unread_count": 5
}
```

---

### POST /notifications/{id}/mark-read

Mark a notification as read.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Notification ID |

**Success Response (200 OK):**
```json
{
  "message": "Notification marked as read"
}
```

---

### POST /notifications/mark-all-read

Mark all notifications as read.

**Authorization:** Required

**Success Response (200 OK):**
```json
{
  "message": "All notifications marked as read",
  "count": 5
}
```

---

### DELETE /notifications/{id}

Delete a notification.

**Authorization:** Required

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Notification ID |

**Success Response (204 No Content):**
No response body

---

## Admin Endpoints

**Note:** All admin endpoints require the `admin` role.

### GET /admin/users

List all users (admin only).

**Authorization:** Admin required

**Success Response (200 OK):**
```json
{
  "users": [
    {
      "id": "user123...",
      "username": "john_doe",
      "email": "john@example.com",
      "role": "user",
      "is_active": true,
      "created_at": "2025-01-01T12:00:00Z",
      "last_login": "2025-10-01T14:30:00Z"
    }
  ]
}
```

---

### POST /admin/users

Create a new user (admin only).

**Authorization:** Admin required

**Request Body:**
```json
{
  "username": "new_user",
  "email": "newuser@example.com",
  "password": "SecurePass123",
  "role": "user",
  "is_active": true
}
```

**Success Response (201 Created):**
User object

---

### GET /admin/settings

Get system settings (admin only).

**Authorization:** Admin required

**Success Response (200 OK):**
```json
{
  "favorites_threshold_percentage": 75,
  "favorites_min_raters": 2,
  "low_stock_threshold_days": 3,
  "expiration_warning_days": 7,
  "scraper_rate_limit_seconds": 5
}
```

---

### PUT /admin/settings

Update system settings (admin only).

**Authorization:** Admin required

**Request Body:**
```json
{
  "favorites_threshold_percentage": 80,
  "favorites_min_raters": 3,
  "expiration_warning_days": 5
}
```

**Success Response (200 OK):**
Updated settings object

---

### GET /admin/statistics

Get system usage statistics (admin only).

**Authorization:** Admin required

**Success Response (200 OK):**
```json
{
  "users": {
    "total": 8,
    "active": 6,
    "admins": 2
  },
  "recipes": {
    "total": 154,
    "most_cooked": [
      {
        "recipe_id": "recipe1...",
        "title": "Spaghetti Carbonara",
        "times_cooked": 25
      }
    ],
    "most_favorited": [
      {
        "recipe_id": "recipe2...",
        "title": "Chicken Parmesan",
        "thumbs_up": 8,
        "thumbs_down": 0
      }
    ]
  },
  "inventory": {
    "total_items": 45,
    "low_stock_items": 3,
    "expiring_soon": 2
  },
  "menu_plans": {
    "total": 12,
    "active": 2
  }
}
```

---

### POST /admin/notifications/generate/low-stock

Manually generate low stock notifications (admin only).

**Authorization:** Admin required

**Success Response (200 OK):**
```json
{
  "message": "Low stock notifications generated",
  "count": 3
}
```

---

### POST /admin/notifications/generate/expiring

Manually generate expiring item notifications (admin only).

**Authorization:** Admin required

**Success Response (200 OK):**
```json
{
  "message": "Expiring item notifications generated",
  "count": 2
}
```

---

### POST /admin/notifications/generate/meal-reminders

Manually generate meal reminder notifications (admin only).

**Authorization:** Admin required

**Success Response (200 OK):**
```json
{
  "message": "Meal reminder notifications generated",
  "count": 5
}
```

---

## Error Handling

### Standard Error Response

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong",
  "error_code": "ERROR_CODE"
}
```

### HTTP Status Codes

| Code | Name | Description |
|------|------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Request successful, no response body |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required or failed |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource already exists (e.g., duplicate username) |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

### Common Error Examples

**400 Bad Request:**
```json
{
  "detail": "At least one instruction is required"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Could not validate credentials"
}
```

**403 Forbidden:**
```json
{
  "detail": "Admin privileges required"
}
```

**404 Not Found:**
```json
{
  "detail": "Recipe not found"
}
```

**409 Conflict:**
```json
{
  "detail": "Username already registered"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**429 Rate Limit:**
```json
{
  "detail": "Too many login attempts. Please try again later.",
  "retry_after": 900
}
```

---

## Additional Resources

**Related Documentation:**
- [User Guide](USER_GUIDE.md) - End-user documentation
- [Developer Guide](DEVELOPER_GUIDE.md) - Development setup
- [Admin Guide](ADMIN_GUIDE.md) - System administration
- [OpenAPI Specification](API_SPEC.yaml) - Machine-readable API spec

**Interactive API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

**Support:**
- GitHub Issues: Report bugs, request features
- Documentation: Check guides for detailed information

---

**Document Version:** 1.0
**Last Updated:** October 1, 2025
**API Version:** 1.0.2
