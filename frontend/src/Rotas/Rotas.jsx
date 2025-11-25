import { Routes, Route } from "react-router-dom";
import { Menu } from '../Componentes/Menu';
import { Inicial } from "../Paginas/Inicial";
import { Login } from "../Paginas/Login";

export function Rotas(){
    return(
         <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/inicial" element={<Inicial />} >
                <Route index element={<Menu />} /> 
            </Route>
        </Routes>
    )
}