import React, { useState } from 'react';

const mockTeammates = [
  { id: 1, name: 'Player1', skill: 'Sniper', rank: 'High' },
  { id: 2, name: 'Player2', skill: 'Rifler', rank: 'Medium' },
  { id: 3, name: 'Player3', skill: 'Support', rank: 'High' },
  { id: 4, name: 'Player4', skill: 'Leader', rank: 'Low' },
];

const TeammateSearch = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(mockTeammates);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    setResults(
      mockTeammates.filter(
        (t) =>
          t.name.toLowerCase().includes(value.toLowerCase()) ||
          t.skill.toLowerCase().includes(value.toLowerCase()) ||
          t.rank.toLowerCase().includes(value.toLowerCase())
      )
    );
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Teammate Search</h1>
      <input
        type="text"
        value={query}
        onChange={handleSearch}
        placeholder="Enter skill, name or rank"
        style={{ padding: '10px', width: '300px', marginBottom: '20px', borderRadius: '5px', border: '1px solid #ccc' }}
      />
      <div>
        {results.length === 0 ? (
          <p>No results found</p>
        ) : (
          results.map((t) => (
            <div key={t.id} className="card" style={{ marginBottom: '10px' }}>
              <strong>{t.name}</strong> — {t.skill} ({t.rank})
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default TeammateSearch;
