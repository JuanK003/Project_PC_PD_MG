import './App.css';
import { BrowserRouter,Route,Routes } from 'react-router-dom';


import CompIniciosinlogin from './Componentes/Login/iniciosinlogin';
import CompIniciarSesion from './Componentes/Login/IniciarSesion';




function App() {
  return (
    <>
    <BrowserRouter>
        <Routes>

        <Route path='/' element={<CompIniciosinlogin></CompIniciosinlogin>}></Route>
        <Route path='/iniciarsesion' element={<CompIniciarSesion></CompIniciarSesion>}></Route>

        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;