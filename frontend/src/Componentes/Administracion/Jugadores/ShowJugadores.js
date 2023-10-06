import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import CompNavBarAdmin from "../../Navbar/NavbarAdmin";

const URI = 'http://127.0.0.1:8000/olimpic/jugadores/';

const CompShowJugadores = () => {
  const [Jugadores, setJugadores] = useState([]);

  useEffect(() => {
    getJugadores();
  }, []);

  const getJugadores = async () => {
    try {
      const res = await axios.get(URI);
      const jugadoresArray = res.data ? Object.values(res.data) : [];
      setJugadores(jugadoresArray);
    } catch (error) {
      console.error("Error al obtener jugadores:", error);
    }
  };

  const deleteJugador = async (id) => {
    try {
      await axios.delete(`${URI}${id}`);
      getJugadores();
    } catch (error) {
      console.error("Error al eliminar jugador:", error);
    }
  };

  return (
    <>
    <CompNavBarAdmin></CompNavBarAdmin>
      <div className="container">
        <div className="row">
          <div className="col">
            <Link to="/createjugador" className="btn btn-success">
              Crear Jugador <i className="fa-solid fa-plus"></i>
            </Link>
            <br></br>
            <br></br>
            <table className="table">
              <thead className="table-dark">
                <tr>
                  <th>Carnet</th>
                  <th>Numero</th>
                  <th>Nombre</th>
                  <th>Posicion</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {Jugadores.map((jugador) => (
                  <tr key={jugador.identifier_number}>
                    <td>{jugador.identifier_number}</td>
                    <td>{jugador.number}</td>
                    <td>{jugador.player_name}</td>
                    <td>{jugador.position}</td>
                    <td>
                      <Link to={`/editJugador/${jugador.identifier_number}`} className="btn btn-info">
                        <i className="fa-solid fa-pen-to-square"></i>
                      </Link>
                      <button onClick={() => deleteJugador(jugador.identifier_number)} className="btn btn-danger">
                        <i className="fa-solid fa-trash"></i>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
};

export default CompShowJugadores;