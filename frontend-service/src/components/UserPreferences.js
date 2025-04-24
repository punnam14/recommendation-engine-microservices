import React, { useEffect, useState }  from 'react';

const UserPreferences = ({ preferences, products, onPreferencesChange }) => {
  // TODO: Implement a form for capturing user preferences
  // This component should include:
  // - Price range selection
  // - Category selection (checkboxes or multi-select)
  // - Brand selection
  // - Any other relevant preference options
  
  const [categories, setCategories] = useState([]);
  const [brands, setBrands] = useState([]);

  const [showCategories, setShowCategories] = useState(false);
  const [showBrands, setShowBrands] = useState(false);

  useEffect(() => {
    const uniqueCategories = [...new Set(products.map(p => p.category))];
    const uniqueBrands = [...new Set(products.map(p => p.brand))];
    setCategories(uniqueCategories);
    setBrands(uniqueBrands);
  }, [products]);

  const handleCheckboxChange = (type, value) => {
    const currentValues = preferences[type];
    const updatedValues = currentValues.includes(value)
      ? currentValues.filter(v => v !== value)
      : [...currentValues, value];

    onPreferencesChange({ [type]: updatedValues });
  };

  const handlePriceRangeChange = (e) => {
    onPreferencesChange({ priceRange: e.target.value });
  };

  return (
    <div className="preferences-container">
      <h3>Your Preferences</h3>
      <div className="pref-group">
        <label><strong>Price Range:</strong></label>
        <select value={preferences.priceRange} onChange={handlePriceRangeChange}>
          <option value="all">All</option>
          <option value="under50">Under $50</option>
          <option value="50to100">$50 - $100</option>
          <option value="over100">Over $100</option>
        </select>
      </div>

      <div className="pref-group">
        <div 
          className="toggle-header" 
          onClick={() => setShowCategories(!showCategories)}
        >
          <strong>Categories </strong> 
          <span className="arrow">{showCategories ? '▾' : '▸'}</span>
        </div>
        {showCategories && (
          <div className="checkbox-list">
            {categories.map(category => (
              <div key={category}>
                <input
                  type="checkbox"
                  checked={preferences.categories.includes(category)}
                  onChange={() => handleCheckboxChange("categories", category)}
                />
                <label>{category}</label>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="pref-group">
        <div 
          className="toggle-header" 
          onClick={() => setShowBrands(!showBrands)}
        >
          <strong>Brands </strong> 
          <span className="arrow">{showBrands ? '▾' : '▸'}</span>
        </div>
        {showBrands && (
          <div className="checkbox-list">
            {brands.map(brand => (
              <div key={brand}>
                <input
                  type="checkbox"
                  checked={preferences.brands.includes(brand)}
                  onChange={() => handleCheckboxChange("brands", brand)}
                />
                <label>{brand}</label>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default UserPreferences;