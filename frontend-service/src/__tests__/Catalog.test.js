import { render, screen } from '@testing-library/react';
import Catalog from '../components/Catalog';

test('renders a product card', () => {
  const product = {
    id: "1",
    name: "Test Product",
    price: 99,
    brand: "BrandX",
    category: "Gadgets",
    description: "Test description"
  };

  render(<Catalog products={[product]} onProductClick={() => {}} browsingHistory={[]} />);
  expect(screen.getByText(/Test Product/i)).toBeInTheDocument();
});
