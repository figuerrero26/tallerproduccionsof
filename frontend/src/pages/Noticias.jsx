import { useEffect, useState } from "react";
import { api } from "../services/api.js";
import NewsItem from "../components/NewsItem.jsx";

export default function Noticias() {
  const [noticias, setNoticias] = useState([]);

  useEffect(() => {
    api.listarNoticias().then(setNoticias).catch(() => {});
  }, []);

  return (
    <section>
      <h1>Noticias</h1>
      {noticias.length === 0 && <p>No hay noticias publicadas todavía.</p>}
      {noticias.map((n) => (
        <NewsItem key={n.id} noticia={n} />
      ))}
    </section>
  );
}
