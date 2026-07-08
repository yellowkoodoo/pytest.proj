import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useCart } from "../CartContext";
import { useAuth } from "../AuthContext";
import { api } from "../api";

export default function CheckoutPage() {
  const { items, total, clearCart } = useCart();
  const { user } = useAuth();
  const navigate  = useNavigate();

  const [paymentMethod, setPaymentMethod] = useState("credit_card");
  const [loading, setLoading]             = useState(false);
  const [result, setResult]               = useState(null); // { success, order, error }

  if (!user) {
    return (
      <div className="page" style={{ maxWidth: 500, margin: "60px auto", textAlign: "center" }}>
        <p style={{ marginBottom: 16, color: "#6b7280" }}>You need to be logged in to checkout.</p>
        <Link to="/login"><button className="btn btn-primary">Login</button></Link>
      </div>
    );
  }

  if (items.length === 0 && !result) {
    return (
      <div className="page" style={{ textAlign: "center", paddingTop: 60 }}>
        <p style={{ color: "#6b7280", marginBottom: 16 }}>Your cart is empty.</p>
        <Link to="/"><button className="btn btn-primary">Shop Now</button></Link>
      </div>
    );
  }

  // BUG #7 (UI): The "Place Order" button is NOT disabled while the request is in flight.
  // A fast double-click submits the order twice. A good candidate will write a test
  // that clicks the button twice rapidly and assert only one order is created.
  async function handlePlaceOrder() {
    setLoading(true);
    try {
      const order = await api.post("/orders", {
        items: items.map(i => ({ productId: i.product.id, quantity: i.quantity })),
        paymentMethod,
      });

      // BUG #8 (UI): The UI shows "Order placed successfully!" even when
      // paymentStatus === "failed". It should show an error message instead.
      clearCart();
      setResult({ success: true, order });
    } catch (err) {
      setResult({ success: false, error: err.message });
    } finally {
      setLoading(false);
    }
  }

  if (result?.success) {
    return (
      <div className="page" style={{ maxWidth: 500, margin: "40px auto", textAlign: "center" }}>
        <div className="card">
          <p style={{ fontSize: "3rem" }}>✅</p>
          <h2 style={{ fontSize: "1.2rem", fontWeight: 700, margin: "12px 0 6px" }} data-testid="success-msg">
            Order placed successfully!
          </h2>
          <p style={{ color: "#6b7280", fontSize: "0.88rem", marginBottom: 20 }}>
            Order ID: <strong data-testid="order-id">{result.order.id}</strong><br />
            Payment: <strong data-testid="payment-status">{result.order.paymentStatus}</strong>
          </p>
          <div style={{ display: "flex", gap: 10, justifyContent: "center" }}>
            <Link to="/orders"><button className="btn btn-primary">View My Orders</button></Link>
            <Link to="/"><button className="btn btn-outline">Continue Shopping</button></Link>
          </div>
        </div>
      </div>
    );
  }

  if (result?.success === false) {
    return (
      <div className="page" style={{ maxWidth: 500, margin: "40px auto", textAlign: "center" }}>
        <div className="card">
          <p style={{ fontSize: "3rem" }}>❌</p>
          <h2 style={{ fontSize: "1.2rem", fontWeight: 700, margin: "12px 0 6px", color: "#dc2626" }}>
            Something went wrong
          </h2>
          <p className="error-msg" data-testid="checkout-error">{result.error}</p>
          <button className="btn btn-outline" style={{ marginTop: 16 }} onClick={() => setResult(null)}>Try Again</button>
        </div>
      </div>
    );
  }

  return (
    <div className="page" style={{ maxWidth: 700 }}>
      <h1 style={{ fontSize: "1.4rem", fontWeight: 700, marginBottom: 20 }}>Checkout</h1>

      <div className="grid-2" style={{ alignItems: "start" }}>
        {/* Order summary */}
        <div className="card">
          <h2 style={{ fontSize: "1rem", fontWeight: 700, marginBottom: 14 }}>Order Summary</h2>
          {items.map(({ product, quantity }) => (
            <div key={product.id} style={{ display: "flex", justifyContent: "space-between", marginBottom: 8, fontSize: "0.88rem" }}>
              <span>{product.name} × {quantity}</span>
              <span>${(product.price * quantity).toFixed(2)}</span>
            </div>
          ))}
          <hr style={{ margin: "12px 0", border: "none", borderTop: "1px solid #e5e7eb" }} />
          <div style={{ display: "flex", justifyContent: "space-between", fontWeight: 700 }}>
            <span>Total</span>
            <span data-testid="checkout-total">${total.toFixed(2)}</span>
          </div>
        </div>

        {/* Payment */}
        <div className="card">
          <h2 style={{ fontSize: "1rem", fontWeight: 700, marginBottom: 14 }}>Payment</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {[
              { value: "credit_card", label: "💳 Credit Card (Visa ending 4242)" },
              { value: "paypal",      label: "🅿️ PayPal" },
              { value: "invalid_card", label: "💳 Test: Declined Card" },
            ].map(opt => (
              <label key={opt.value} style={{ display: "flex", alignItems: "center", gap: 10, cursor: "pointer", fontSize: "0.9rem" }}>
                <input
                  type="radio"
                  name="payment"
                  value={opt.value}
                  checked={paymentMethod === opt.value}
                  onChange={() => setPaymentMethod(opt.value)}
                  data-testid={`payment-${opt.value}`}
                  style={{ width: "auto" }}
                />
                {opt.label}
              </label>
            ))}
          </div>

          <button
            className="btn btn-primary"
            data-testid="place-order-btn"
            onClick={handlePlaceOrder}
            // BUG #7: intentionally NOT using `disabled={loading}` — race condition
            style={{ marginTop: 20, width: "100%" }}
          >
            {loading ? "Processing…" : `Place Order · $${total.toFixed(2)}`}
          </button>
        </div>
      </div>
    </div>
  );
}
