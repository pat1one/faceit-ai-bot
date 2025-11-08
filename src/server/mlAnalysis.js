const tf = require('@tensorflow/tfjs-node');

// Загрузка обученной модели
async function loadTrainedModel() {
  const model = await tf.loadLayersModel('file://./model/model.json');
  return model;
}

// Анализ данных с использованием модели
async function analyzeDemoData(inputData) {
  const model = await loadTrainedModel();

  // Преобразование входных данных в тензор
  const tensor = tf.tensor2d(inputData, [1, inputData.length]);

  // Получение предсказания
  const prediction = model.predict(tensor);
  const result = prediction.dataSync();

  return result;
}

module.exports = { analyzeDemoData };