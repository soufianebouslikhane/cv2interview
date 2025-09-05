// lib/api.ts

export async function processFile(file: File): Promise<string> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://localhost:8000/agent/upload", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to process file");
  }

  const data = await response.json();
  return data.text;  // correspond au champ "text" renvoyé par le backend
}

export async function extractProfile(text: string) {
  const response = await fetch('http://localhost:8000/agent/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      instruction: "Extract the candidate's key skills, experiences, and education from this CV text:\n\n" + text,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to extract profile');
  }

  const data = await response.json();
  return data.response; // renvoie la réponse brute LLM, pas de parsing ici
}


export async function generateQuestions(text: string) {
  const response = await fetch("http://localhost:8000/agent/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      instruction: `Generate 5 technical interview questions based on this resume:\n\n${text}`,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to generate questions");
  }

  const data = await response.json();
  return data.response;
}

export async function getCareerRecommendation(text: string) {
  const response = await fetch("http://localhost:8000/agent/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      instruction: `Based on this resume, suggest three suitable career paths and justify your choices:\n\n${text}`,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to get recommendation");
  }

  const data = await response.json();
  return data.response;
}
