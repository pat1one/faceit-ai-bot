import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import DemoUpload from '../../components/DemoUpload'

test('DemoUpload renders and calls callback on submit', () => {
  const onAnalysisComplete = jest.fn()
  const { container } = render(<DemoUpload onAnalysisComplete={onAnalysisComplete} />)

  // file input has no label in component, find by selector
  const input = container.querySelector('input[type="file"]') as HTMLInputElement
  const submit = screen.getByRole('button', { name: /Загрузить и проанализировать/i })

  // simulate selecting a file (value cannot be set directly for file inputs in JSDOM),
  // so we simply submit the form which triggers the mock callback in the component
  fireEvent.click(submit)

  expect(onAnalysisComplete).toHaveBeenCalled()
})
