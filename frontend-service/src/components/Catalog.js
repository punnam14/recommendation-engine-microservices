import React, { useState } from 'react';

const ITEMS_PER_PAGE = 6;

const Catalog = ({ products, onProductClick, browsingHistory }) => {
  // TODO: Implement a product catalog display
  // This component should display a grid of products from the catalog
  // Each product should be clickable to add to browsing history
  
  const [page, setPage] = useState(0);

  const startIndex = page * ITEMS_PER_PAGE;
  const endIndex = startIndex + ITEMS_PER_PAGE;
  const currentItems = products.slice(startIndex, endIndex);

  const handleNext = () => {
    if (endIndex < products.length) {
      setPage(prev => prev + 1);
    }
  };

  const handlePrev = () => {
    if (page > 0) {
      setPage(prev => prev - 1);
    }
  };

  return (
    <div>
      <div className="catalog-grid">
        {currentItems.map(product => (
          <div 
            key={product.id} 
            className={`product-card ${browsingHistory.includes(product.id) ? 'viewed' : ''}`} 
            onClick={() => onProductClick(product.id)}
          >
            <h4>{product.name}</h4>
            <p><strong>Brand:</strong> {product.brand}</p>
            <p><strong>Price:</strong> ${product.price}</p>
            <p><strong>Category:</strong> {product.category}</p>
            <p className="description">{product.description}</p>
          </div>
        ))}
      </div>

      <div className="pagination-controls">
        <button onClick={handlePrev} disabled={page === 0}>
          ⬅ Prev
        </button>
        <span> Page {page + 1} of {Math.ceil(products.length / ITEMS_PER_PAGE)} </span>
        <button onClick={handleNext} disabled={endIndex >= products.length}>
          Next ➡
        </button>
      </div>
    </div>
  );
};

export default Catalog;
