import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useAuth } from "../AuthContext";
import { api } from "../api";

export default function OrderDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate  = useNavigate();
  const [order, setOrder]     = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState("");

  useEffect(() => {
    if (!user) { navigate("/login"); return; }
    api.get(`/orders/${id}`)
      .then(setOrder)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [id, user]);

  async function handleCancel() {
    try {
      const updated = await api.patch(`/orders/${id}`, { status: "cancelled" });
      setOrder(updated);
    } catch (err) {
      setError(err.message);
    }
  }

  if (loading) return <div className="page"><p style={{ color: "#6b7280" }}>Loading…</p></div>;
  if (error)   return <div className="page"><p className="error-msg" data-testid="order-error">{error}</p></div>;
  if (!order)  return null;

  return (
    <div className="page" style={{ maxWidth: 620 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
        <Link to="/orders"><button className="btn btn-outline" style={{ padding: "5px 10px" }}>← Back</button></Link>
        <h1 style={{ fontSize: "1.3rem", fontWeight: 700 }}>Order {order.id}</h1>
        <span className={`badge badge-${order.status}`} data-testid="order-status">{order.status}</span>
      </div>

      <div className="card" style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: "0.9rem", fontWeight: 700, marginBottom: 12, color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.05em" }}>Items</h2>
        {order.items.map((item, i) => (
          <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", borderBottom: i < order.items.length - 1 ? "1px solid #f1f5f9" : "none", fontSize: "0.9rem" }}>
            <span>{item.productId} × {item.quantity}</span>
            <span>${(item.price * item.quantity).toFixed(2)}</span>
          </div>
        ))}
        <div style={{ display: "flex", justifyContent: "space-between", fontWeight: 700, marginTop: 12 }}>
          <span>Total</span>
          <span data-testid="order-total">${order.total.toFixed(2)}</span>
        </div>
      </div>

      <div className="card" style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: "0.9rem", fontWeight: 700, marginBottom: 12, color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.05em" }}>Details</h2>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, fontSize: "0.88rem" }}>
          <div><p style={{ color: "#9ca3af", marginBottom: 2 }}>Payment</p><p data-testid="payment-status" style={{ fontWeight: 600 }}>{order.paymentStatus}</p></div>
          <div><p style={{ color: "#9ca3af", marginBottom: 2 }}>Status</p><p style={{ fontWeight: 600 }}>{order.status}</p></div>
          <div><p style={{ color: "#9ca3af", marginBottom: 2 }}>Created</p><p>{new Date(order.createdAt).toLocaleString()}</p></div>
          <div><p style={{ color: "#9ca3af", marginBottom: 2 }}>Updated</p><p>{new Date(order.updatedAt).toLocaleString()}</p></div>
        </div>
      </div>

      {["processing", "payment_failed"].includes(order.status) && (
        <button
          className="btn btn-danger"
          data-testid="cancel-order-btn"
          onClick={handleCancel}
        >
          Cancel Order
        </button>
      )}
      {error && <p className="error-msg" style={{ marginTop: 10 }}>{error}</p>}
    </div>
  );
}
