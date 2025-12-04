import { Routes, Route } from "react-router-dom";
import { Login } from "../Paginas/Login";
import { Inicial } from "../Paginas/Inicial";
import { Menu } from "../Componentes/Menu";
import { Ambientes } from "../Paginas/Ambientes";
import { Sensores } from "../Paginas/Sensores";

export function Rotas() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />

      <Route path="/inicial" element={<Inicial />}>
        <Route index element={<Menu />} />
        <Route path="ambientes" element={<Ambientes />} />
        <Route path="sensores" element={<Sensores />} />
      </Route>
    </Routes>
  );
}
