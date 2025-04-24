import React from 'react';

const BrowsingHistory = ({ history, products, onClearHistory }) => {
  // TODO: Implement a browsing history display
  // This component should:
  // - Show products the user has clicked on
  // - Allow clearing the browsing history
  
  const viewedProducts = history
    .map(id => products.find(p => p.id === id))
    .filter(p => p); 

  return (
    <div className="history-container">
      <h3>Your Browsing History</h3>
      {viewedProducts.length === 0 ? (
        <p>No browsing history yet.</p>
      ) : (
        <div>
          <ul className="history-list">
            {viewedProducts.map(product => (
              <li key={product.id} className="history-item">
                <strong>{product.name}</strong> – {product.category}, ${product.price}
              </li>
            ))}
          </ul>
          <button className="clear-history-btn" onClick={onClearHistory}>
            Clear History
          </button>
        </div>
      )}
    </div>
  );
};

export default BrowsingHistory;