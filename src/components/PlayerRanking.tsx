import React from 'react';

const mockRankings = [
  { id: 1, name: 'Алексей', score: 1500 },
  { id: 2, name: 'Мария', score: 1450 },
  { id: 3, name: 'Иван', score: 1400 },
  { id: 4, name: 'Денис', score: 1350 },
];

const PlayerRanking = () => {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Рейтинг игроков</h1>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Место</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Имя</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Очки</th>
          </tr>
        </thead>
        <tbody>
          {mockRankings.map((player, index) => (
            <tr key={player.id}>
              <td style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'center' }}>{index + 1}</td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>{player.name}</td>
              <td style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'center' }}>{player.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PlayerRanking;