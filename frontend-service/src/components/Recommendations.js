import React from 'react';

const Recommendations = ({ recommendations, isLoading }) => {
  // TODO: Implement a display for recommended products
  // This component should:
  // - Display recommended products with explanations
  // - Show a loading state when recommendations are being generated
  // - Handle cases where no recommendations are available
  
  return (
    <div className="recommendations-container">
      {isLoading ? (
        <p>Loading recommendations...</p>
      ) : recommendations.length > 0 ? (
        <div className="catalog-grid">
          {recommendations.map((rec, index) => (
            <div key={index} className="product-card">
              <h4>{rec.product.name}</h4>
              <p><strong>Brand:</strong> {rec.product.brand}</p>
              <p><strong>Price:</strong> ${rec.product.price}</p>
              <p><strong>Category:</strong> {rec.product.category}</p>
              <p className="description">{rec.product.description}</p>
              <p><em>Why we recommended this:</em> {rec.explanation}</p>
              <p><small>Confidence Score: {rec.confidence_score}/10</small></p>
            </div>
          ))}
        </div>
      ) : (
        <p>No recommendations yet. Set your preferences and browse some products!</p>
      )}
    </div>
  );
};

export default Recommendations;
