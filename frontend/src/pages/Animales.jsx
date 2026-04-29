import { useEffect, useState } from "react";
import { api } from "../services/api.js";
import AnimalCard from "../components/AnimalCard.jsx";

export default function Animales() {
  const [animales, setAnimales] = useState([]);
  const [estado, setEstado] = useState("disponible");
  const [error, setError] = useState(null);

  useEffect(() => {
    setError(null);
    api
      .listarAnimales(estado)
      .then(setAnimales)
      .catch((e) => setError(e.message));
  }, [estado]);

  return (
    <section>
      <h1>Animales en adopción</h1>
      <label>
        Filtrar por estado:{" "}
        <select value={estado} onChange={(e) => setEstado(e.target.value)}>
          <option value="">Todos</option>
          <option value="disponible">Disponibles</option>
          <option value="en_proceso">En proceso</option>
          <option value="adoptado">Adoptados</option>
        </select>
      </label>
      {error && <p className="error">{error}</p>}
      <div className="grid" style={{ marginTop: "1rem" }}>
        {animales.map((a) => (
          <AnimalCard key={a.id} animal={a} />
        ))}
      </div>
      {animales.length === 0 && !error && <p>No hay animales para mostrar.</p>}
    </section>
  );
}
