const redis = require('redis');

const client = redis.createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379'
});

client.on('error', (err) => {
  console.error('Redis error:', err);
});

async function setCache(key, value, ttl = 3600) {
  await client.connect();
  await client.set(key, JSON.stringify(value), { EX: ttl });
  await client.disconnect();
}

async function getCache(key) {
  await client.connect();
  const value = await client.get(key);
  await client.disconnect();
  return value ? JSON.parse(value) : null;
}

module.exports = { setCache, getCache };
