/**
 * Load testing с k6
 * 
 * Запуск: k6 run tests/load/basic_load.js
 */

import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },  // Разогрев до 20 пользователей
    { duration: '1m', target: 50 },   // Рост до 50 пользователей
    { duration: '2m', target: 50 },   // Удержание 50 пользователей
    { duration: '30s', target: 0 },   // Спад до 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% запросов быстрее 500ms
    http_req_failed: ['rate<0.01'],   // Меньше 1% ошибок
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
