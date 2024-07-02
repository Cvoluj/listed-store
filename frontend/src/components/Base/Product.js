import { useState } from "react";

const Product = ({ product, index }) => {
  const [quantity, setQuantity] = useState(1);

  const handleQuantity = (event) => {
    const value = Math.min(event.target.value, product.stock);
    setQuantity(value);
  };

  // TODO: make a real buy
  const handleBuyNow = () => {
    if (quantity > product.stock) {
      alert(`Cannot buy more than ${product.stock} items.`);
    } else {
      alert(`You have bought ${quantity} ${product.name}(s).`);
    }
  };

    return (
      <tr key={index}>
        <th scope="row">{index + 1}</th>
        <td>{product.name}</td>
        <td>{product.description}</td>
        <td>{product.price}</td>
        <td>{product.stock}</td>
        <td>{product.user}</td>
        <td>
        <input
          type="number"
          value={quantity}
          min="1"
          max={product.stock}
          onChange={handleQuantity}
          className="form-control"
          style={{ width: '100px', display: 'inline-block', marginRight: '10px' }}
        /></td>
        <td>
        <button onClick={handleBuyNow} className="btn btn-primary btn-sm">
          Buy Now
        </button>
      </td>
      </tr>
    );
  };
  
  const Products = ({ products }) => {
    return (
      <div className="container">
        <h2 className="mb-4">Our Products</h2>
        <table className="table table-striped">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Name</th>
              <th scope="col">Description</th>
              <th scope="col">Price</th>
              <th scope="col">Stock</th>
              <th scope="col">User</th>
              <th scope="col">Much</th>
              <th scope="col">Action</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product, index) => (
              <Product key={index} product={product} index={index} />
            ))}
          </tbody>
        </table>
        {/* Pagination */}
        <nav aria-label="Page navigation example">
          <ul className="pagination">
            {/* Pagination content here */}
          </ul>
        </nav>
      </div>
    );
  };

export default Products;