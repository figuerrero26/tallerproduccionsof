export default function NewsItem({ noticia }) {
  return (
    <article className="card">
      <h3>{noticia.titulo}</h3>
      <p className="meta">
        {noticia.autor || "Fundación"} ·{" "}
        {new Date(noticia.fecha_publicacion).toLocaleDateString()}
      </p>
      <p>{noticia.contenido}</p>
    </article>
  );
}
