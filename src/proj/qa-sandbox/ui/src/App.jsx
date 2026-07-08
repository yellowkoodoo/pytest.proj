import { Routes, Route, Link, useNavigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./AuthContext";
import { CartProvider, useCart } from "./CartContext";
import ProductsPage  from "./pages/Products.jsx";
import LoginPage     from "./pages/Login.jsx";
import CartPage      from "./pages/Cart.jsx";
import CheckoutPage  from "./pages/Checkout.jsx";
import OrdersPage    from "./pages/Orders.jsx";
import OrderDetail   from "./pages/OrderDetail.jsx";

function Nav() {
  const { user, logout } = useAuth();
  const { count } = useCart();
  const navigate = useNavigate();

  return (
    <nav>
      <Link to="/" className="logo">🛍 ShopQA</Link>
      <div className="nav-links">
        <Link to="/"><button className="btn btn-outline" style={{ padding: "6px 14px" }}>Products</button></Link>
        {user && (
          <Link to="/orders"><button className="btn btn-outline" style={{ padding: "6px 14px" }}>My Orders</button></Link>
        )}
        <Link to="/cart">
          <button className="btn btn-outline" style={{ padding: "6px 14px" }} data-testid="cart-btn">
            🛒 Cart {count > 0 && <span style={{ marginLeft: 4, background: "#2563eb", color: "white", borderRadius: "99px", padding: "1px 6px", fontSize: "0.75rem" }}>{count}</span>}
          </button>
        </Link>
        {user ? (
          <>
            <span style={{ fontSize: "0.85rem", color: "#6b7280" }}>Hi, {user.name.split(" ")[0]}</span>
            <button className="btn btn-outline" style={{ padding: "6px 14px" }} onClick={async () => { await logout(); navigate("/"); }}>
              Logout
            </button>
          </>
        ) : (
          <Link to="/login"><button className="btn btn-primary" style={{ padding: "6px 14px" }}>Login</button></Link>
        )}
      </div>
    </nav>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <Nav />
        <Routes>
          <Route path="/"           element={<ProductsPage />} />
          <Route path="/login"      element={<LoginPage />} />
          <Route path="/cart"       element={<CartPage />} />
          <Route path="/checkout"   element={<CheckoutPage />} />
          <Route path="/orders"     element={<OrdersPage />} />
          <Route path="/orders/:id" element={<OrderDetail />} />
        </Routes>
      </CartProvider>
    </AuthProvider>
  );
}
