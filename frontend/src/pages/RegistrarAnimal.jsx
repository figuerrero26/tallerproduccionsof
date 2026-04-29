import { useState } from "react";
import { api } from "../services/api.js";

const initial = {
  nombre: "",
  especie: "perro",
  edad: "",
  estado: "disponible",
  descripcion: "",
};

export default function RegistrarAnimal() {
  const [form, setForm] = useState(initial);
  const [msg, setMsg] = useState(null);

  const onChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const onSubmit = async (e) => {
    e.preventDefault();
    setMsg(null);
    try {
      const payload = {
        ...form,
        edad: form.edad ? Number(form.edad) : null,
      };
      const created = await api.crearAnimal(payload);
      setMsg(`Animal "${created.nombre}" registrado con éxito (id ${created.id}).`);
      setForm(initial);
    } catch (err) {
      setMsg(`Error: ${err.message}`);
    }
  };

  return (
    <section>
      <h1>Registrar un animal</h1>
      <form onSubmit={onSubmit} className="form">
        <label>
          Nombre
          <input
            name="nombre"
            value={form.nombre}
            onChange={onChange}
            required
          />
        </label>
        <label>
          Especie
          <select name="especie" value={form.especie} onChange={onChange}>
            <option value="perro">Perro</option>
            <option value="gato">Gato</option>
            <option value="otro">Otro</option>
          </select>
        </label>
        <label>
          Edad (años)
          <input
            type="number"
            name="edad"
            value={form.edad}
            onChange={onChange}
            min="0"
          />
        </label>
        <label>
          Estado
          <select name="estado" value={form.estado} onChange={onChange}>
            <option value="disponible">Disponible</option>
            <option value="en_proceso">En proceso</option>
            <option value="adoptado">Adoptado</option>
          </select>
        </label>
        <label>
          Descripción
          <textarea
            name="descripcion"
            value={form.descripcion}
            onChange={onChange}
            rows="4"
          />
        </label>
        <button type="submit">Guardar</button>
      </form>
      {msg && <p className="msg">{msg}</p>}
    </section>
  );
}
