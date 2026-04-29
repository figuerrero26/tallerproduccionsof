import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="brand">Fundación Rescate Animal</div>
      <ul>
        <li><Link to="/">Inicio</Link></li>
        <li><Link to="/animales">Animales</Link></li>
        <li><Link to="/noticias">Noticias</Link></li>
        <li><Link to="/registrar">Registrar</Link></li>
      </ul>
    </nav>
  );
}
