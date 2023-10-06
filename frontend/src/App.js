import './App.css';
import { BrowserRouter,Route,Routes } from 'react-router-dom';


import CompIniciosinlogin from './Componentes/Login/iniciosinlogin';
import CompIniciarSesion from './Componentes/Login/IniciarSesion';
import CompInicioAdmin from './Componentes/Administracion/inicioAdministracion';
import CompShowJugadores from './Componentes/Administracion/Jugadores/ShowJugadores';
import CompShowEquipos from './Componentes/Administracion/Equipos/ShowEquipos';




function App() {
  return (
    <>
    <BrowserRouter>
        <Routes>

        <Route path='/' element={<CompIniciosinlogin></CompIniciosinlogin>}></Route>
        <Route path='/iniciarsesion' element={<CompIniciarSesion></CompIniciarSesion>}></Route>
        <Route path='/Administracion' element={<CompInicioAdmin></CompInicioAdmin>}></Route>

        <Route path='/Jugadores' element={<CompShowJugadores></CompShowJugadores>}></Route>

        <Route path='/Equipos' element={<CompShowEquipos></CompShowEquipos>}></Route>

        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;