# API Documentation

**Base URL:** `http://localhost:8000/api/`  
**Format:** JSON  
**Authentication:** Session auth or Basic auth (header: `Authorization: Basic <base64>`)

---

## Authentication

Most read endpoints are public. Write operations (POST / PUT / PATCH / DELETE) require a logged-in user.  
Unauthenticated write requests receive **401 Unauthorized**.  
Attempts to modify another user's product receive **403 Forbidden**.

---

## Pagination

All list endpoints return paginated results — **6 items per page**.

**Response envelope:**

```json
{
  "count": 24,
  "total_pages": 4,
  "current_page": 1,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

| Param | Type | Description |
|---|---|---|
| `page` | integer | Page number to retrieve |
| `page_size` | integer | Override page size (max 100) |

---

## Filtering, Search & Ordering

Available on `GET /api/products/`:

| Param | Example | Description |
|---|---|---|
| `category` | `?category=3` | Filter by category ID |
| `category_name` | `?category_name=electronics` | Filter by category name (case-insensitive) |
| `is_available` | `?is_available=true` | Filter by availability (`true` / `false`) |
| `min_price` | `?min_price=10` | Price greater than or equal to value |
| `max_price` | `?max_price=100` | Price less than or equal to value |
| `search` | `?search=shoes` | Search by product name |
| `ordering` | `?ordering=price` | Order by `price`, `name`, or `created_at`. Prefix `-` for descending: `?ordering=-price` |

Params can be combined: `?category=2&is_available=true&search=shirt&ordering=-price`

---

## Products

### List / Create Products

**`GET /api/products/`**

Returns a paginated list of all products. Supports filtering, search, and ordering (see above).

- **Auth required:** No
- **Request body:** None

**Response `200 OK`:**
```json
{
  "count": 12,
  "total_pages": 2,
  "current_page": 1,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Running Shoes",
      "price": "49.99",
      "is_available": true,
      "stock": 20,
      "created_at": "2024-01-15T10:00:00Z",
      "created_by": "john",
      "category": 2,
      "image": "http://localhost:8000/media/products/shoes.jpg"
    }
  ]
}
```

---

**`POST /api/products/`**

Create a new product. The `created_by` field is set automatically to the logged-in user.

- **Auth required:** Yes

**Request body:**
```json
{
  "name": "Running Shoes",
  "price": "49.99",
  "is_available": true,
  "stock": 20,
  "category": 2,
  "image": "<file upload — multipart/form-data>"
}
```

**Response `201 Created`:**
```json
{
  "id": 5,
  "name": "Running Shoes",
  "price": "49.99",
  "is_available": true,
  "stock": 20,
  "created_at": "2024-06-01T09:30:00Z",
  "created_by": "john",
  "category": 2,
  "image": null
}
```

**Error `400 Bad Request`** — validation failed:
```json
{ "name": ["This field is required."] }
```

---

### Retrieve / Update / Delete a Product

**`GET /api/products/<id>/`**

Retrieve a single product by ID.

- **Auth required:** No

**Response `200 OK`:**
```json
{
  "id": 1,
  "name": "Running Shoes",
  "price": "49.99",
  "is_available": true,
  "stock": 20,
  "created_at": "2024-01-15T10:00:00Z",
  "created_by": "john",
  "category": 2,
  "image": null
}
```

**Error `404 Not Found`:**
```json
{ "detail": "Not found." }
```

---

**`PUT /api/products/<id>/`**

Full update of a product. All fields required. Only the creator can update.

- **Auth required:** Yes (must be creator)

**Request body:** Same as POST (all fields required).

**Response `200 OK`:** Updated product object.

**Error `403 Forbidden`:**
```json
{ "detail": "You do not have permission to modify this product." }
```

---

**`PATCH /api/products/<id>/`**

Partial update. Send only the fields you want to change.

- **Auth required:** Yes (must be creator)

**Request body (example — change price only):**
```json
{ "price": "39.99" }
```

**Response `200 OK`:** Updated product object.

---

**`DELETE /api/products/<id>/`**

Delete a product. Only the creator can delete.

- **Auth required:** Yes (must be creator)

**Response `204 No Content`** — empty body on success.

**Error `403 Forbidden`:**
```json
{ "detail": "You do not have permission to modify this product." }
```

---

## Categories

### List / Create Categories

**`GET /api/categories/`**

Returns a paginated list of all categories.

- **Auth required:** No

**Response `200 OK`:**
```json
{
  "count": 4,
  "total_pages": 1,
  "current_page": 1,
  "next": null,
  "previous": null,
  "results": [
    { "id": 1, "name": "Footwear", "description": "Shoes, boots, sandals" },
    { "id": 2, "name": "Electronics", "description": "" }
  ]
}
```

---

**`POST /api/categories/`**

Create a new category.

- **Auth required:** Yes

**Request body:**
```json
{
  "name": "Footwear",
  "description": "Shoes, boots, sandals"
}
```

**Response `201 Created`:**
```json
{ "id": 3, "name": "Footwear", "description": "Shoes, boots, sandals" }
```

---

### Retrieve / Update / Delete a Category

**`GET /api/categories/<id>/`**

- **Auth required:** No

**Response `200 OK`:**
```json
{ "id": 1, "name": "Footwear", "description": "Shoes, boots, sandals" }
```

---

**`PUT /api/categories/<id>/`**

Full update of a category.

- **Auth required:** Yes

**Request body:**
```json
{ "name": "Footwear", "description": "Updated description" }
```

**Response `200 OK`:** Updated category object.

---

**`DELETE /api/categories/<id>/`**

Delete a category. This will also delete all products in this category (CASCADE).

- **Auth required:** Yes

**Response `204 No Content`** — empty body.

---

## Legacy JSON Endpoints

These views return plain `JsonResponse` without pagination or auth.

| Method | URL | Description |
|---|---|---|
| GET | `/products/json/` | All products (no pagination) |
| GET | `/products/json/<id>/` | Single product |
| GET | `/categories/json/` | All categories |
| GET | `/categories/json/<id>/` | Single category |

---

## Error Reference

| Status | Meaning |
|---|---|
| `200 OK` | Request succeeded |
| `201 Created` | Resource created |
| `204 No Content` | Deleted successfully |
| `400 Bad Request` | Validation error — check response body |
| `401 Unauthorized` | Not logged in |
| `403 Forbidden` | Logged in but not the resource owner |
| `404 Not Found` | Resource does not exist |