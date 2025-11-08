import { rest } from 'msw';

export const handlers = [
  rest.post('http://localhost:8000/analyze-demo', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        analysis: 'Demo analysis result',
      })
    );
  }),

  rest.post('http://localhost:8000/payments/yookassa', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        payment_url: 'http://payment-link.com',
      })
    );
  }),

  rest.post('http://localhost:8000/payments/sbp', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        payment_url: 'http://sbp-payment-link.com',
      })
    );
  }),
];