# QA Automation Sandbox — Candidate Guide

A realistic e-commerce system built specifically for QA automation assessment.
It has real functionality, real bugs, and real edge cases.

---

## Quick Start (2 commands)

**Prerequisites:** Docker Desktop installed and running.

```bash
git clone <repo-url> qa-sandbox
cd qa-sandbox
docker compose up --build
```

That's it. Open:

| Service | URL |
|---------|-----|
| 🛍 Storefront (UI) | http://localhost:3000 |
| ⚙️ REST API | http://localhost:3001 |
| ❤️ Health check | http://localhost:3001/health |

To stop: `Ctrl+C` then `docker compose down`

---

## Test Accounts

| Email | Password | Role |
|-------|----------|------|
| alice@example.com | pass123 | Customer |
| bob@example.com | pass456 | Customer |
| admin@shop.com | admin999 | Admin |

---

## API Reference

All endpoints return JSON. Auth endpoints require a Bearer token in the
`Authorization` header: `Authorization: Bearer <token>`

### Auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/login` | No | Login, returns token |
| POST | `/auth/logout` | Yes | Invalidate token |
| GET | `/auth/me` | Yes | Current user info |

**Login request body:**
```json
{ "email": "alice@example.com", "password": "pass123" }
```

**Login response:**
```json
{
  "token": "uuid-string",
  "user": { "id": "u1", "email": "...", "name": "...", "role": "customer" }
}
```

---

### Products

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/products` | No | List products |
| GET | `/products/:id` | No | Get single product |

**Query params for GET /products:**

| Param | Type | Example |
|-------|------|---------|
| search | string | `?search=shoes` |
| category | string | `?category=electronics` |
| sort | string | `?sort=price_asc` or `?sort=price_desc` |
| page | number | `?page=2` |
| limit | number | `?limit=5` |

**Product object:**
```json
{
  "id": "p1",
  "name": "Wireless Headphones",
  "price": 79.99,
  "stock": 15,
  "category": "electronics"
}
```

---

### Orders

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/orders` | Yes | List orders (own for customer, all for admin) |
| GET | `/orders/:id` | Yes | Get single order |
| POST | `/orders` | Yes | Create order |
| PATCH | `/orders/:id` | Yes | Update status |
| DELETE | `/orders/:id` | Admin | Hard delete order |

**GET /orders query params:** `?status=processing&page=1&limit=10&sort=createdAt_desc`

**POST /orders request body:**
```json
{
  "items": [
    { "productId": "p1", "quantity": 2 }
  ],
  "paymentMethod": "credit_card"
}
```

Valid paymentMethod values: `credit_card`, `paypal`, `invalid_card` (simulates declined card)

**PATCH /orders/:id request body:**
```json
{ "status": "cancelled" }
```

Valid statuses (admin): `processing`, `shipped`, `delivered`, `cancelled`, `refunded`
Valid statuses (customer): `cancelled` only

**Order object:**
```json
{
  "id": "ord-abc123",
  "userId": "u1",
  "items": [{ "productId": "p1", "quantity": 1, "price": 79.99 }],
  "total": 79.99,
  "status": "processing",
  "paymentStatus": "paid",
  "createdAt": "2024-03-10T09:00:00.000Z",
  "updatedAt": "2024-03-10T09:00:00.000Z"
}
```

---

### Users (Admin only)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/users` | Admin | List all users |

---

## What to Test

### API Test Suite
Cover the `/orders` endpoint fully:
- Create orders: happy path, empty items, invalid productId, out-of-stock items
- Pagination: page/limit combinations, edge cases (page beyond total)
- Filtering by status (valid values, invalid values)
- Sorting: ascending and descending
- Auth: unauthenticated requests, customer accessing another user's order
- PATCH transitions: valid transitions, invalid ones (e.g. cancel a delivered order)
- Admin vs customer permissions

### E2E UI Flows (minimum 3)
1. Browse products → Add to cart → Checkout → Order confirmation
2. Login / Logout flow including invalid credentials
3. Failed payment flow — what does the UI show?
4. Cancel an order from the orders list

### Data Strategy
- Use external test data files (JSON, YAML, or a fixtures file)
- Don't hardcode credentials or IDs in test code

### CI Setup
- Include a GitHub Actions workflow (`.github/workflows/test.yml`) that runs tests headlessly

---

## Known Seed Data

**Products available at startup:**

| ID | Name | Price | Stock | Category |
|----|------|-------|-------|----------|
| p1 | Wireless Headphones | $79.99 | 15 | electronics |
| p2 | Running Shoes | $129.00 | 8 | footwear |
| p3 | Coffee Maker | $49.99 | 3 | appliances |
| p4 | Yoga Mat | $25.00 | 20 | fitness |
| p5 | Desk Lamp | $34.99 | **0** | home |
| p6 | Bluetooth Speaker | $59.99 | 12 | electronics |
| p7 | Water Bottle | $18.00 | 50 | fitness |
| p8 | Notebook Set | $12.99 | 30 | stationery |

**Note:** Stock is in-memory and resets on container restart. Pre-existing orders are seeded for ord-001 (Alice) and ord-002 (Bob).

---

## Technical Notes

- API data is **in-memory** — all changes reset when the container restarts
- CORS is open — any origin can call the API
- There is no rate limiting
- The API has no persistent database — design your tests accordingly
- `data-testid` attributes are on all interactive UI elements

---

## Deliverables Expected

1. **API test suite** covering the orders endpoint (happy path + negative + edge cases)
2. **3+ E2E tests** for UI flows listed above
3. **Data-driven** approach: no hardcoded values in test code
4. **CI config** (GitHub Actions YAML) to run tests headlessly
5. **README** in your submission covering:
   - Framework choices and why
   - How to run your tests
   - Bugs you found (document them!)
   - What you'd add with more time
