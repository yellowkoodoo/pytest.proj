import { Link } from "react-router-dom";
import { useCart } from "../CartContext";

export default function CartPage() {
  const { items, removeItem, updateQty, total, clearCart } = useCart();

  if (items.length === 0) {
    return (
      <div className="page" style={{ textAlign: "center", paddingTop: 60 }}>
        <p style={{ fontSize: "3rem" }}>🛒</p>
        <p style={{ color: "#6b7280", margin: "12px 0 20px" }}>Your cart is empty.</p>
        <Link to="/"><button className="btn btn-primary">Browse Products</button></Link>
      </div>
    );
  }

  return (
    <div className="page" style={{ maxWidth: 700 }}>
      <h1 style={{ fontSize: "1.4rem", fontWeight: 700, marginBottom: 20 }}>Your Cart</h1>

      <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 24 }}>
        {items.map(({ product, quantity }) => (
          <div key={product.id} className="card" style={{ display: "flex", alignItems: "center", gap: 16 }} data-testid={`cart-item-${product.id}`}>
            <span style={{ fontSize: "2rem" }}>{categoryEmoji(product.category)}</span>
            <div style={{ flex: 1 }}>
              <p style={{ fontWeight: 600 }}>{product.name}</p>
              <p style={{ color: "#6b7280", fontSize: "0.85rem" }}>${product.price.toFixed(2)} each</p>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <button className="btn btn-outline" style={{ padding: "4px 10px" }} onClick={() => updateQty(product.id, quantity - 1)}>−</button>
              <span data-testid={`qty-${product.id}`} style={{ minWidth: 24, textAlign: "center" }}>{quantity}</span>
              <button className="btn btn-outline" style={{ padding: "4px 10px" }} onClick={() => updateQty(product.id, quantity + 1)}>+</button>
            </div>
            <span style={{ fontWeight: 700, minWidth: 70, textAlign: "right" }}>${(product.price * quantity).toFixed(2)}</span>
            <button className="btn btn-danger" style={{ padding: "6px 10px" }} data-testid={`remove-${product.id}`} onClick={() => removeItem(product.id)}>✕</button>
          </div>
        ))}
      </div>

      <div className="card" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <p style={{ color: "#6b7280", fontSize: "0.85rem" }}>Total</p>
          <p style={{ fontSize: "1.4rem", fontWeight: 700 }} data-testid="cart-total">${total.toFixed(2)}</p>
        </div>
        <div style={{ display: "flex", gap: 10 }}>
          <button className="btn btn-outline" onClick={clearCart}>Clear Cart</button>
          <Link to="/checkout"><button className="btn btn-primary" data-testid="checkout-btn">Proceed to Checkout</button></Link>
        </div>
      </div>
    </div>
  );
}

function categoryEmoji(cat) {
  const map = { electronics: "🎧", footwear: "👟", appliances: "☕", fitness: "🏋️", home: "🏠", stationery: "📓" };
  return map[cat] || "📦";
}
