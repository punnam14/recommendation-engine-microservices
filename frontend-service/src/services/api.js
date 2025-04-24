const PRODUCT_API = process.env.REACT_APP_PRODUCT_API;
const RECOMMENDATION_API = process.env.REACT_APP_RECOMMENDATION_API;

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