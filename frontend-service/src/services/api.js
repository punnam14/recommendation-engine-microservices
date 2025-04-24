const PRODUCT_API = 'http://localhost:5001/products';
const RECOMMENDATION_API = 'http://localhost:5002/recommendations';

// const API_BASE_URL = 'http://localhost:4000/api';
// const API_BASE_URL = 'https://product-recommendation-engine.onrender.com/api';

// Fetch all products from the API
export const fetchProducts = async () => {
  try {
    const response = await fetch(PRODUCT_API);
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching products:', error);
    throw error;
  }
};

// Get recommendations based on user preferences and browsing history
export const getRecommendations = async (preferences, browsingHistory, allProducts) => {
  try {
    const response = await fetch(RECOMMENDATION_API, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        preferences: preferences,
        browsing_history: browsingHistory,
        all_products: allProducts,
      }),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error getting recommendations:', error);
    throw error;
  }
};