import { useEffect, useState } from "react";
import { api } from "../services/api.js";

export default function Eventos() {
  const [eventos, setEventos] = useState([]);

  useEffect(() => {
    api.listarEventos().then(setEventos).catch(() => {});
  }, []);

  return (
    <section>
      <h1>Próximos eventos</h1>
      {eventos.length === 0 && <p>No hay eventos programados.</p>}
      <ul>
        {eventos.map((e) => (
          <li key={e.id}>
            <strong>{e.nombre}</strong> — {e.lugar}
            {e.fecha && ` (${new Date(e.fecha).toLocaleDateString()})`}
          </li>
        ))}
      </ul>
    </section>
  );
}
