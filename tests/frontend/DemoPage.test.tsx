import React from "react";
import { render, screen, fireEvent, act } from "@testing-library/react";
import DemoPage from "../../app/page";
import { rest } from 'msw';
import { setupServer } from 'msw/node';

global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

const server = setupServer(
  rest.post(
    'http://localhost:8000/analyze-demo',
    (req: any, res: any, ctx: any) => {
      return res(ctx.json({ analysis: 'Demo analysis result' }));
    }
  ),
  rest.post(
    'http://localhost:8000/payments/yookassa',
    (req: any, res: any, ctx: any) => {
      return res(ctx.json({ payment_url: 'http://payment-link.com' }));
    }
  ),
  rest.post(
    'http://localhost:8000/payments/sbp',
    (req: any, res: any, ctx: any) => {
      return res(ctx.json({ payment_url: 'http://sbp-payment-link.com' }));
    }
  )
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

console.log('Test file loaded:', typeof expect !== 'undefined');
console.log('TextEncoder in DemoPage test:', typeof global.TextEncoder);

describe("DemoPage Component", () => {
  test("renders the page header", () => {
    render(<DemoPage />);
    const header = screen.getByText(/AI-Анализ демок/i);
    expect(header).toBeInTheDocument();
  });

  test("renders the upload component", () => {
    render(<DemoPage />);
    const uploadText = screen.getByText(/Загрузите свою демку CS2/i);
    expect(uploadText).toBeInTheDocument();
  });

  test("handles payment button click for YooKassa", async () => {
    render(<DemoPage />);

    // Simулирую завершение анализа
    await act(async () => {
      const fileInput = screen.getByLabelText(/Загрузить демо файл/i);
      fireEvent.change(fileInput, { target: { files: [new File([], "demo.dem")] } });
      const submitButton = screen.getByText(/Загрузить и проанализировать/i);
      fireEvent.click(submitButton);
    });

    const analysisResultElement = await screen.findByText(/Результаты анализа/i);
    expect(analysisResultElement).toBeInTheDocument();

    const paymentButton = screen.getByText(/Оплатить через YooKassa/i);
    fireEvent.click(paymentButton);

    const paymentLink = await screen.findByText(/Перейдите по ссылке для оплаты:/i);
    expect(paymentLink).toBeInTheDocument();
  });

  test("handles payment button click for SBP", async () => {
    render(<DemoPage />);

    // Simулирую завершение анализа
    await act(async () => {
      const fileInput = screen.getByLabelText(/Загрузить демо файл/i);
      fireEvent.change(fileInput, { target: { files: [new File([], "demo.dem")] } });
      const submitButton = screen.getByText(/Загрузить и проанализировать/i);
      fireEvent.click(submitButton);
    });

    const analysisResultElement = await screen.findByText(/Результаты анализа/i);
    expect(analysisResultElement).toBeInTheDocument();

    const paymentButton = screen.getByText(/Оплатить через СБП/i);
    fireEvent.click(paymentButton);

    const paymentLink = await screen.findByText(/Перейдите по ссылке для оплаты:/i);
    expect(paymentLink).toBeInTheDocument();
  });
});