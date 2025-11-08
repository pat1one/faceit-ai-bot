const axios = require('axios');

// Пример интеграции с внешним API игровой платформы
async function fetchPlayerData(playerId) {
  try {
    const response = await axios.get(`https://api.example.com/players/${playerId}`, {
      headers: {
        Authorization: `Bearer ${process.env.GAME_API_KEY}`,
      },
    });

    return response.data;
  } catch (error) {
    console.error('Ошибка при запросе данных игрока:', error);
    return null;
  }
}

async function fetchGameStats(gameId) {
  try {
    const response = await axios.get(`https://api.example.com/games/${gameId}`, {
      headers: {
        Authorization: `Bearer ${process.env.GAME_API_KEY}`,
      },
    });

    return response.data;
  } catch (error) {
    console.error('Ошибка при запросе статистики игры:', error);
    return null;
  }
}

module.exports = { fetchPlayerData, fetchGameStats };