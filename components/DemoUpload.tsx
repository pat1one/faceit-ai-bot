import React from 'react';

type Props = {
  onAnalysisComplete?: (result: any) => void;
};

export default function DemoUpload({ onAnalysisComplete }: Props) {
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Mock submit - call callback immediately
    const mock = { message: 'mock analysis', success: true };
    if (onAnalysisComplete) onAnalysisComplete(mock);
  };

  return (
    <form onSubmit={handleSubmit} style={{textAlign: 'center'}}>
      <input type="file" accept=".dem" aria-label="Загрузить демо файл" />
      <div style={{marginTop: 12}}>
        <button type="submit">Загрузить и проанализировать</button>
      </div>
    </form>
  );
}
