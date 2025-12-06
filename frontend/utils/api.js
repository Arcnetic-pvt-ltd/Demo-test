const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchAudits() {
  const res = await fetch(`${API_URL}/audits`, { cache: 'no-store' });
  return res.json();
}

export async function createAudit(url) {
  await fetch(`${API_URL}/audit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
}

export async function deleteAudit(id) {
    await fetch(`${API_URL}/audit/${id}`, {
        method: 'DELETE',
    });
}