const { Configuration, OpenAIApi } = require('openai');

// Настройка OpenAI API
const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY, // Убедитесь, что ключ API установлен в переменных окружения
});
const openai = new OpenAIApi(configuration);

// Функция для отправки запроса к GPT
async function generateResponse(prompt) {
  try {
    const response = await openai.createChatCompletion({
      model: 'gpt-4',
      messages: [
        { role: 'system', content: 'Вы помощник для анализа данных пользователей.' },
        { role: 'user', content: prompt },
      ],
    });

    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('Ошибка при запросе к OpenAI API:', error);
    return 'Произошла ошибка при обработке запроса.';
  }
}

module.exports = { generateResponse };