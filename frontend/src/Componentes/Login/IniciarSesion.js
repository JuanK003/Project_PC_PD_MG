import axios from "axios";
import { useState, useEffect } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import CompNavBarClientes from "../Navbar/Navbar";

const URI = 'http://localhost:8000/users/usuarios';

const CompIniciarSesion = () => {
  const [clientes, setClientes] = useState([]);
  useEffect(() => {
    getClientes();
  }, []);

  // Procedimiento para mostrar todos los componentes
  const getClientes = async () => {
    try {
      const res = await axios.get(URI);
      if (Array.isArray(res.data)) {
        setClientes(res.data);
      } else {
        console.error("La respuesta de la API no es un array:", res.data);
      }
    } catch (error) {
      console.error("Error al obtener clientes:", error);
    }
  };

  const [correo, setCorreo] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const store = async (e) => {
    e.preventDefault();

    if (Array.isArray(clientes)) {
      clientes.map((cliente) => {
        if (correo === cliente.correo && password === cliente.password) {
          console.log(cliente.password);
          navigate(`/iniciocliente/${cliente.id}`);
        }
        return null;
      });
    } else {
      console.error("El estado 'clientes' no es un array válido:", clientes);
    }
  };

  return (
    <>
      <CompNavBarClientes />
      <div className="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-8">
          {/* <img
              className="mx-auto h-12 w-auto"
              src="https://www.google.com/url?sa=i&url=https%3A%2F%2Fes.vecteezy.com%2Ffotos-gratis%2Ffutbol&psig=AOvVaw05NOmxijpm6V2sKIRMlsKg&ust=1694267310134000&source=images&cd=vfe&opi=89978449&ved=0CA4QjRxqFwoTCNiu5NyTm4EDFQAAAAAdAAAAABAI"
              alt="Your Company"
            /> */}
            <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-red-900">
              OLIMPIC SHOWDOWN
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              
              <a href="https://www.facebook.com/profile.php?id=100004522368573" className="font-medium text-indigo-600 hover:text-indigo-500">
                Visitamos en Facebook
              </a>
            </p>
          </div>
          <form className="mt-8 space-y-6" onSubmit={store}>
            <input type="hidden" name="remember" defaultValue="true" />
            <div className="-space-y-px rounded-md shadow-sm">
              <div>
                <label htmlFor="email-address" className="sr-only">
                  Correo
                </label>
                <input
                value={correo}
                onChange={(e)=>setCorreo(e.target.value)}
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="relative block w-full appearance-none rounded-none rounded-t-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="Email"
                />
              </div>
              <div>
                <label htmlFor="password" className="sr-only">
                  Contraseña
                </label>
                <input
                value={password}
                onChange={(e)=>setPassword(e.target.value)}
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  className="relative block w-full appearance-none rounded-none rounded-b-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="Contraseña"
                />
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
                <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
                  Recordarme
                </label>
              </div>

              <div className="text-sm">
                <a href="#" className="font-medium text-red-600 hover:text-red-500">
                  Recuperar Contraseña
                </a>
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="group relative flex w-full justify-center rounded-md border border-transparent bg-red-600 py-2 px-4 text-sm font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
              >
                Iniciar Sesion
              </button>
            </div>
          </form>
      </div>
    </>
  );
};

export default CompIniciarSesion;
