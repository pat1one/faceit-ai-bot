import React from 'react'
import { render, screen } from '@testing-library/react'
import { expect } from '@jest/globals';
import Navigation from '../../components/Navigation'
import '@testing-library/jest-dom';

console.log('Navigation test loaded');
console.log(typeof expect);

test('Navigation renders site title', () => {
  render(<Navigation />)
  expect(screen.getByText(/Faceit AI Bot/i)).toBeInTheDocument()
})
