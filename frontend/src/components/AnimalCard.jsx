export default function AnimalCard({ animal }) {
  return (
    <article className="card">
      <h3>{animal.nombre}</h3>
      <p><strong>Especie:</strong> {animal.especie}</p>
      <p><strong>Edad:</strong> {animal.edad ?? "—"} años</p>
      <p><strong>Estado:</strong> {animal.estado}</p>
      {animal.descripcion && <p>{animal.descripcion}</p>}
    </article>
  );
}
