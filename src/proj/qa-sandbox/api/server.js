const express = require("express");
const cors = require("cors");
const { v4: uuidv4 } = require("uuid");

const app = express();
app.use(cors());
app.use(express.json());

// ─── SEED DATA ────────────────────────────────────────────────────────────────

let users = [
  { id: "u1", email: "alice@example.com", password: "pass123", name: "Alice Martin", role: "customer" },
  { id: "u2", email: "bob@example.com",   password: "pass456", name: "Bob Chen",    role: "customer" },
  { id: "admin1", email: "admin@shop.com", password: "admin999", name: "Shop Admin", role: "admin" },
];

let products = [
  { id: "p1", name: "Wireless Headphones", price: 79.99,  stock: 15, category: "electronics" },
  { id: "p2", name: "Running Shoes",        price: 129.00, stock: 8,  category: "footwear"    },
  { id: "p3", name: "Coffee Maker",         price: 49.99,  stock: 3,  category: "appliances"  },
  { id: "p4", name: "Yoga Mat",             price: 25.00,  stock: 20, category: "fitness"     },
  { id: "p5", name: "Desk Lamp",            price: 34.99,  stock: 0,  category: "home"        },
  { id: "p6", name: "Bluetooth Speaker",   price: 59.99,  stock: 12, category: "electronics" },
  { id: "p7", name: "Water Bottle",         price: 18.00,  stock: 50, category: "fitness"     },
  { id: "p8", name: "Notebook Set",         price: 12.99,  stock: 30, category: "stationery"  },
];

let orders = [
  {
    id: "ord-001",
    userId: "u1",
    items: [{ productId: "p1", quantity: 1, price: 79.99 }],
    total: 79.99,
    status: "delivered",
    paymentStatus: "paid",
    createdAt: "2024-03-01T10:00:00Z",  // BUG #3: inconsistent date format (some use Z, some don't)
    updatedAt: "2024-03-02T14:30:00Z",
  },
  {
    id: "ord-002",
    userId: "u2",
    items: [{ productId: "p2", quantity: 2, price: 129.00 }],
    total: 258.00,
    status: "processing",
    paymentStatus: "paid",
    createdAt: "2024-03-10T09:15:00",   // BUG #3: missing Z timezone designator
    updatedAt: "2024-03-10T09:15:00",
  },
];

let sessions = {}; // token -> userId

// ─── HELPERS ──────────────────────────────────────────────────────────────────

function requireAuth(req, res, next) {
  const token = req.headers["authorization"]?.replace("Bearer ", "");
  if (!token || !sessions[token]) {
    return res.status(401).json({ error: "Unauthorized" });
  }
  req.userId = sessions[token];
  req.userRole = users.find(u => u.id === req.userId)?.role;
  next();
}

function requireAdmin(req, res, next) {
  requireAuth(req, res, () => {
    if (req.userRole !== "admin") {
      return res.status(403).json({ error: "Forbidden: admin only" });
    }
    next();
  });
}

// ─── HEALTH ───────────────────────────────────────────────────────────────────

app.get("/health", (req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

// ─── AUTH ─────────────────────────────────────────────────────────────────────

// POST /auth/login
app.post("/auth/login", (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: "email and password are required" });
  }

  const user = users.find(u => u.email === email && u.password === password);
  if (!user) {
    return res.status(401).json({ error: "Invalid credentials" });
  }

  const token = uuidv4();
  sessions[token] = user.id;

  res.json({
    token,
    user: { id: user.id, email: user.email, name: user.name, role: user.role },
  });
});

// POST /auth/logout
app.post("/auth/logout", requireAuth, (req, res) => {
  const token = req.headers["authorization"]?.replace("Bearer ", "");
  delete sessions[token];
  res.json({ message: "Logged out" });
});

// GET /auth/me
app.get("/auth/me", requireAuth, (req, res) => {
  const user = users.find(u => u.id === req.userId);
  res.json({ id: user.id, email: user.email, name: user.name, role: user.role });
});

// ─── PRODUCTS ─────────────────────────────────────────────────────────────────

// GET /products  (supports ?category=&search=&page=&limit=)
app.get("/products", (req, res) => {
  let result = [...products];
  const { category, search, page, limit, sort } = req.query;

  if (category) result = result.filter(p => p.category === category);
  if (search)   result = result.filter(p => p.name.toLowerCase().includes(search.toLowerCase()));

  // BUG #4: sort=price_asc sorts DESCENDING instead of ascending (logic inverted)
  if (sort === "price_asc")  result.sort((a, b) => b.price - a.price);
  if (sort === "price_desc") result.sort((a, b) => a.price - b.price);

  const total = result.length;
  const pageNum  = parseInt(page)  || 1;
  const limitNum = parseInt(limit) || 10;
  const start = (pageNum - 1) * limitNum;
  const end   = start + limitNum;
  result = result.slice(start, end);

  // BUG #5: X-Total-Count header is missing — pagination metadata only in body
  // Candidates should notice the header is absent and document it
  res.json({
    data: result,
    pagination: {
      page: pageNum,
      limit: limitNum,
      total,
      // BUG #6: totalPages is always rounded DOWN — off-by-one when total % limit !== 0
      totalPages: Math.floor(total / limitNum),
    },
  });
});

// GET /products/:id
app.get("/products/:id", (req, res) => {
  const product = products.find(p => p.id === req.params.id);
  if (!product) return res.status(404).json({ error: "Product not found" });
  res.json(product);
});

// ─── ORDERS ───────────────────────────────────────────────────────────────────

// GET /orders  (auth required; admin sees all, customer sees own)
// Supports ?status=&page=&limit=&sort=createdAt_asc|createdAt_desc
app.get("/orders", requireAuth, (req, res) => {
  let result = req.userRole === "admin"
    ? [...orders]
    : orders.filter(o => o.userId === req.userId);

  const { status, page, limit, sort } = req.query;
  if (status) result = result.filter(o => o.status === status);

  if (sort === "createdAt_asc")  result.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
  if (sort === "createdAt_desc") result.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

  const total    = result.length;
  const pageNum  = parseInt(page)  || 1;
  const limitNum = parseInt(limit) || 10;
  result = result.slice((pageNum - 1) * limitNum, pageNum * limitNum);

  res.json({ data: result, pagination: { page: pageNum, limit: limitNum, total } });
});

// GET /orders/:id
app.get("/orders/:id", requireAuth, (req, res) => {
  const order = orders.find(o => o.id === req.params.id);
  if (!order) return res.status(404).json({ error: "Order not found" });

  // Non-admin can only see their own orders
  if (req.userRole !== "admin" && order.userId !== req.userId) {
    return res.status(403).json({ error: "Forbidden" });
  }
  res.json(order);
});

// POST /orders  — create a new order
app.post("/orders", requireAuth, (req, res) => {
  const { items, paymentMethod } = req.body;

  if (!items || !Array.isArray(items) || items.length === 0) {
    return res.status(400).json({ error: "items array is required and must not be empty" });
  }

  // Validate products and stock
  for (const item of items) {
    const product = products.find(p => p.id === item.productId);
    if (!product) {
      return res.status(422).json({ error: `Product ${item.productId} not found` });
    }
    if (product.stock < item.quantity) {
      return res.status(422).json({ error: `Insufficient stock for product ${item.productId}` });
    }
  }

  // BUG #1: FAILED PAYMENT returns HTTP 200 instead of 402
  // A candidate should catch that paymentMethod "invalid_card" succeeds with status 200
  // and paymentStatus "failed" — this is the most critical bug to find
  let paymentStatus = "paid";
  if (paymentMethod === "invalid_card") {
    paymentStatus = "failed";
    // Should return 402, but we return 200 — intentional bug
  }

  // Calculate total
  let total = 0;
  const enrichedItems = items.map(item => {
    const product = products.find(p => p.id === item.productId);
    const lineTotal = product.price * item.quantity;
    total += lineTotal;
    return { productId: item.productId, quantity: item.quantity, price: product.price };
  });

  // BUG #2: Stock is decremented even when payment fails
  if (paymentStatus === "paid") {
    items.forEach(item => {
      const product = products.find(p => p.id === item.productId);
      product.stock -= item.quantity;
    });
  }
  // Note: when paymentStatus === "failed", we still deduct stock — BUG #2

  const newOrder = {
    id: `ord-${uuidv4().slice(0, 6)}`,
    userId: req.userId,
    items: enrichedItems,
    total: parseFloat(total.toFixed(2)),
    status: paymentStatus === "paid" ? "processing" : "payment_failed",
    paymentStatus,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  orders.push(newOrder);
  res.status(200).json(newOrder); // BUG #1 continuation: should be 201 on success too
});

// PATCH /orders/:id  — update status (admin) or cancel (customer)
app.patch("/orders/:id", requireAuth, (req, res) => {
  const order = orders.find(o => o.id === req.params.id);
  if (!order) return res.status(404).json({ error: "Order not found" });

  if (req.userRole !== "admin" && order.userId !== req.userId) {
    return res.status(403).json({ error: "Forbidden" });
  }

  const { status } = req.body;
  const allowedCustomerStatuses = ["cancelled"];
  const allowedAdminStatuses    = ["processing", "shipped", "delivered", "cancelled", "refunded"];

  if (req.userRole !== "admin" && !allowedCustomerStatuses.includes(status)) {
    return res.status(403).json({ error: "Customers can only cancel orders" });
  }
  if (!allowedAdminStatuses.includes(status)) {
    return res.status(400).json({ error: `Invalid status. Allowed: ${allowedAdminStatuses.join(", ")}` });
  }

  // Cannot cancel a delivered order
  if (order.status === "delivered" && status === "cancelled") {
    return res.status(422).json({ error: "Cannot cancel a delivered order" });
  }

  order.status    = status;
  order.updatedAt = new Date().toISOString();
  res.json(order);
});

// DELETE /orders/:id  — admin only hard delete
app.delete("/orders/:id", requireAdmin, (req, res) => {
  const idx = orders.findIndex(o => o.id === req.params.id);
  if (idx === -1) return res.status(404).json({ error: "Order not found" });
  orders.splice(idx, 1);
  res.status(204).send();
});

// ─── USERS (admin only) ───────────────────────────────────────────────────────

app.get("/users", requireAdmin, (req, res) => {
  res.json(users.map(u => ({ id: u.id, email: u.email, name: u.name, role: u.role })));
});

// ─── START ────────────────────────────────────────────────────────────────────

app.listen(3001, () => {
  console.log("QA Sandbox API running on http://localhost:3001");
  console.log("NOTE: This API contains intentional bugs for QA assessment purposes.");
});
