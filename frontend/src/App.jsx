import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar.jsx";
import Home from "./pages/Home.jsx";
import Animales from "./pages/Animales.jsx";
import Noticias from "./pages/Noticias.jsx";
import RegistrarAnimal from "./pages/RegistrarAnimal.jsx";

export default function App() {
  return (
    <>
      <Navbar />
      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/animales" element={<Animales />} />
          <Route path="/noticias" element={<Noticias />} />
          <Route path="/registrar" element={<RegistrarAnimal />} />
        </Routes>
      </main>
    </>
  );
}
