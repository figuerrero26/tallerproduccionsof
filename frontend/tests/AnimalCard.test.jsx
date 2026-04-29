import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import AnimalCard from "../src/components/AnimalCard.jsx";

describe("AnimalCard", () => {
  it("muestra el nombre, especie, edad y estado del animal", () => {
    const animal = {
      id: 1,
      nombre: "Luna",
      especie: "perro",
      edad: 3,
      estado: "disponible",
      descripcion: "Mestiza vacunada",
    };

    render(<AnimalCard animal={animal} />);

    expect(screen.getByText("Luna")).toBeInTheDocument();
    expect(screen.getByText(/perro/i)).toBeInTheDocument();
    expect(screen.getByText(/3/)).toBeInTheDocument();
    expect(screen.getByText(/disponible/i)).toBeInTheDocument();
    expect(screen.getByText("Mestiza vacunada")).toBeInTheDocument();
  });

  it("muestra '—' cuando el animal no tiene edad registrada", () => {
    const animal = {
      id: 2,
      nombre: "Sin edad",
      especie: "gato",
      estado: "disponible",
    };

    render(<AnimalCard animal={animal} />);

    expect(screen.getByText(/—/)).toBeInTheDocument();
  });
});
