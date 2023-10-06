import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import CompNavBarAdmin from "../../Navbar/NavbarAdmin";

const URI = 'http://127.0.0.1:8000/olimpic/equipos/';

const CompShowEquipos = () => {
  const [equipos, setEquipos] = useState([]);
  const [expandedEquipo, setExpandedEquipo] = useState(null);

  useEffect(() => {
    getEquipos();
  }, []);

  const getEquipos = async () => {
    try {
      const res = await axios.get(URI);
      const equiposArray = res.data ? Object.values(res.data) : [];
      setEquipos(equiposArray);
    } catch (error) {
      console.error("Error al obtener Equipos:", error);
    }
  };

  const deleteEquipo = async (id) => {
    try {
      await axios.delete(`${URI}${id}`);
      getEquipos();
    } catch (error) {
      console.error("Error al eliminar Equipo:", error);
    }
  };

  const toggleDetails = (equipo) => {
    if (expandedEquipo === equipo) {
      setExpandedEquipo(null);
    } else {
      setExpandedEquipo(equipo);
    }
  };

  return (
    <>
      <CompNavBarAdmin></CompNavBarAdmin>
      <div className="container">
        <div className="row">
          <div className="col">
            <Link to="/createEquipos" className="btn btn-success">
              Crear Jugador <i className="fa-solid fa-plus"></i>
            </Link>
            <br></br>
            <br></br>
            <table className="table">
              <thead className="table-dark">
                <tr>
                  <th>Nombre</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {equipos.map((equipo) => (
                  <React.Fragment key={equipo.name}>
                    <tr>
                      <td>{equipo.name}</td>
                      <td>
                        <button onClick={() => toggleDetails(equipo)} className="btn btn-primary">
                          Ver Detalles
                        </button>
                      </td>
                    </tr>
                    {expandedEquipo === equipo && (
                      <tr>
                        <td colSpan="2">
                          <div>
                            <h3>Detalles del Equipo:</h3>
                            <p>Nombre: {equipo.name}</p>
                            <p>Jugadores:</p>
                            <ul>
                              {equipo.players.map((jugador, index) => (
                                <li key={index}>
                                  <strong>Nombre del Jugador:</strong> {jugador.player_name}<br />
                                  <strong>Número:</strong> {jugador.number}<br />
                                  <strong>Posición:</strong> {jugador.position}<br />
                                </li>
                              ))}
                            </ul>
                          </div>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
};

export default CompShowEquipos;
