import { useState, useEffect } from "react";
import { api } from "../api";
import { useCart } from "../CartContext";

export default function ProductsPage() {
  const [products, setProducts]   = useState([]);
  const [loading, setLoading]     = useState(true);
  const [search, setSearch]       = useState("");
  const [category, setCategory]   = useState("");
  const [sort, setSort]           = useState("");
  const [added, setAdded]         = useState({});
  const { addItem } = useCart();

  useEffect(() => {
    setLoading(true);
    const params = new URLSearchParams();
    if (search)   params.set("search",   search);
    if (category) params.set("category", category);
    if (sort)     params.set("sort",     sort);

    api.get(`/products?${params}`)
      .then(res => setProducts(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [search, category, sort]);

  function handleAdd(product) {
    if (product.stock === 0) return;
    addItem(product);
    setAdded(a => ({ ...a, [product.id]: true }));
    setTimeout(() => setAdded(a => ({ ...a, [product.id]: false })), 1200);
  }

  return (
    <div className="page">
      <h1 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: 20 }}>Products</h1>

      {/* Filters */}
      <div style={{ display: "flex", gap: 12, marginBottom: 24, flexWrap: "wrap" }}>
        <input
          data-testid="search-input"
          placeholder="Search products…"
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{ maxWidth: 260 }}
        />
        <select
          data-testid="category-filter"
          value={category}
          onChange={e => setCategory(e.target.value)}
          style={{ maxWidth: 180 }}
        >
          <option value="">All categories</option>
          <option value="electronics">Electronics</option>
          <option value="footwear">Footwear</option>
          <option value="appliances">Appliances</option>
          <option value="fitness">Fitness</option>
          <option value="home">Home</option>
          <option value="stationery">Stationery</option>
        </select>
        <select
          data-testid="sort-select"
          value={sort}
          onChange={e => setSort(e.target.value)}
          style={{ maxWidth: 180 }}
        >
          <option value="">Sort: Default</option>
          <option value="price_asc">Price: Low → High</option>
          <option value="price_desc">Price: High → Low</option>
        </select>
      </div>

      {loading ? (
        <p style={{ color: "#6b7280" }}>Loading products…</p>
      ) : products.length === 0 ? (
        <p data-testid="no-results" style={{ color: "#6b7280" }}>No products found.</p>
      ) : (
        <div className="grid-3">
          {products.map(p => (
            <div key={p.id} className="card" data-testid={`product-${p.id}`} style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              <div style={{ fontSize: "2rem", textAlign: "center", background: "#f8fafc", borderRadius: 8, padding: "20px 0" }}>
                {categoryEmoji(p.category)}
              </div>
              <span className="tag">{p.category}</span>
              <h3 style={{ fontSize: "0.95rem", fontWeight: 600 }} data-testid={`name-${p.id}`}>{p.name}</h3>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ fontSize: "1.1rem", fontWeight: 700, color: "#2563eb" }} data-testid={`price-${p.id}`}>
                  ${p.price.toFixed(2)}
                </span>
                <span style={{ fontSize: "0.78rem", color: p.stock === 0 ? "#dc2626" : "#6b7280" }} data-testid={`stock-${p.id}`}>
                  {p.stock === 0 ? "Out of stock" : `${p.stock} left`}
                </span>
              </div>
              <button
                className="btn btn-primary"
                data-testid={`add-to-cart-${p.id}`}
                disabled={p.stock === 0}
                onClick={() => handleAdd(p)}
                style={{ marginTop: "auto" }}
              >
                {added[p.id] ? "✓ Added!" : p.stock === 0 ? "Out of Stock" : "Add to Cart"}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function categoryEmoji(cat) {
  const map = { electronics: "🎧", footwear: "👟", appliances: "☕", fitness: "🏋️", home: "🏠", stationery: "📓" };
  return map[cat] || "📦";
}
