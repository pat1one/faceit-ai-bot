const { setCache, getCache } = require('../../src/server/cache');
const redis = require('redis');

jest.mock('redis', () => redis);

describe('Cache Module', () => {
  beforeAll(async () => {
    const client = redis.createClient();
    await client.connect();
    await client.flushAll();
    await client.disconnect();
  });

  test('should set and get cache values', async () => {
    const key = 'testKey';
    const value = { data: 'testValue' };

    await setCache(key, value, 10);
    const cachedValue = await getCache(key);

    expect(cachedValue).toEqual(value);
  });

  test('should return null for non-existent keys', async () => {
    const cachedValue = await getCache('nonExistentKey');
    expect(cachedValue).toBeNull();
  });
});