import { render, screen } from '@testing-library/react';
import App from './App';

test('renders nav with Contacts', () => {
  render(<App />);
  expect(screen.getByText(/Contacts/i)).toBeInTheDocument();
});
