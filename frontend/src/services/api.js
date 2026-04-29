const API_URL = "/api/v1";

async function request(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`Error ${res.status}: ${await res.text()}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  listarAnimales: (estado) =>
    request(`/animales${estado ? `?estado=${estado}` : ""}`),
  crearAnimal: (data) =>
    request("/animales", { method: "POST", body: JSON.stringify(data) }),
  listarNoticias: () => request("/noticias"),
  listarEventos: () => request("/eventos"),
  crearRegistro: (data) =>
    request("/registros", { method: "POST", body: JSON.stringify(data) }),
};
