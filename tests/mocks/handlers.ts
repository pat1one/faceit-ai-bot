import { rest } from 'msw';

export const handlers = [
  rest.post('http://localhost:8000/analyze-demo', async (req, res, ctx) => {
    // Эмулируем обработку FormData
    return res(
      ctx.delay(100),
      ctx.json({ 
        analysis: 'Demo analysis result',
        error: null
      })
    );
  }),

  rest.post('http://localhost:8000/payments/yookassa', async (req, res, ctx) => {
    return res(
      ctx.delay(50),
      ctx.json({ payment_url: 'http://payment-link.com' })
    );
  }),

  rest.post('http://localhost:8000/payments/sbp', async (req, res, ctx) => {
    return res(
      ctx.delay(50),
      ctx.json({ payment_url: 'http://sbp-payment-link.com' })
    );
  })
];