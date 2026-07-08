import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import { api } from "../api";

export default function OrdersPage() {
  const { user } = useAuth();
  const navigate  = useNavigate();
  const [orders, setOrders]   = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState("");

  useEffect(() => {
    if (!user) { navigate("/login"); return; }
    const params = statusFilter ? `?status=${statusFilter}` : "";
    api.get(`/orders${params}`)
      .then(res => setOrders(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [user, statusFilter]);

  async function handleCancel(orderId) {
    try {
      await api.patch(`/orders/${orderId}`, { status: "cancelled" });
      setOrders(prev => prev.map(o => o.id === orderId ? { ...o, status: "cancelled" } : o));
    } catch (err) {
      alert(err.message);
    }
  }

  return (
    <div className="page">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
        <h1 style={{ fontSize: "1.4rem", fontWeight: 700 }}>My Orders</h1>
        <select
          data-testid="status-filter"
          value={statusFilter}
          onChange={e => setStatusFilter(e.target.value)}
          style={{ maxWidth: 180 }}
        >
          <option value="">All statuses</option>
          <option value="processing">Processing</option>
          <option value="shipped">Shipped</option>
          <option value="delivered">Delivered</option>
          <option value="cancelled">Cancelled</option>
          <option value="payment_failed">Payment Failed</option>
        </select>
      </div>

      {loading ? (
        <p style={{ color: "#6b7280" }}>Loading orders…</p>
      ) : orders.length === 0 ? (
        <div style={{ textAlign: "center", paddingTop: 40 }}>
          <p style={{ color: "#6b7280", marginBottom: 16 }} data-testid="no-orders">No orders found.</p>
          <Link to="/"><button className="btn btn-primary">Start Shopping</button></Link>
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {orders.map(order => (
            <div key={order.id} className="card" data-testid={`order-${order.id}`}
              style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 12 }}>
              <div>
                <p style={{ fontWeight: 700, fontSize: "0.95rem" }}>{order.id}</p>
                <p style={{ color: "#6b7280", fontSize: "0.82rem" }}>
                  {order.items.length} item{order.items.length !== 1 ? "s" : ""} · {new Date(order.createdAt).toLocaleDateString()}
                </p>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                <span style={{ fontWeight: 700 }}>${order.total.toFixed(2)}</span>
                <span className={`badge badge-${order.status}`} data-testid={`status-${order.id}`}>{order.status}</span>
                <Link to={`/orders/${order.id}`}>
                  <button className="btn btn-outline" style={{ padding: "5px 12px", fontSize: "0.82rem" }}>View</button>
                </Link>
                {["processing", "payment_failed"].includes(order.status) && (
                  <button
                    className="btn btn-danger"
                    style={{ padding: "5px 12px", fontSize: "0.82rem" }}
                    data-testid={`cancel-${order.id}`}
                    onClick={() => handleCancel(order.id)}
                  >
                    Cancel
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
