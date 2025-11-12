/**
 * Load testing with k6
 * 
 * Run: k6 run tests/load/basic_load.js
 */

import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },  // Warm up to 20 users
    { duration: '1m', target: 50 },   // Ramp up to 50 users
    { duration: '2m', target: 50 },   // Hold 50 users
    { duration: '30s', target: 0 },   // Ramp down to 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests faster than 500ms
    http_req_failed: ['rate<0.01'],   // Less than 1% errors
  },
};

const BASE_URL = __ENV.API_URL || 'http://localhost:8000';

export default function () {
  // Health check
  let res = http.get(`${BASE_URL}/health`);
  check(res, {
    'health check status 200': (r) => r.status === 200,
    'health check healthy': (r) => JSON.parse(r.body).status === 'healthy',
  });

  sleep(1);

  // Player stats
  res = http.get(`${BASE_URL}/api/players/s1mple/stats`);
  check(res, {
    'player stats status 200': (r) => r.status === 200,
    'player stats has data': (r) => Object.keys(JSON.parse(r.body)).length > 0,
  });

  sleep(2);
}

export function handleSummary(data) {
  return {
    'tests/load/summary.html': htmlReport(data),
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
  };
}
