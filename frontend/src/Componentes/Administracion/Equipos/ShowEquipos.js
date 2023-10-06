import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import CompNavBarAdmin from "../../Navbar/NavbarAdmin";

const URI = 'http://127.0.0.1:8000/olimpic/equipos/';

const CompShowEquipos = () => {
  const [Equipos, setEquipos] = useState([]);

  useEffect(() => {
    getEquipos();
  }, []);

  const getEquipos = async () => {
    try {
      const res = await axios.get(URI);
      const EquiposArray = res.data ? Object.values(res.data) : [];
      setEquipos(EquiposArray);
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
                {Equipos.map((Equipo) => (
                  <tr key={Equipo.name}>
                    <td>{Equipo.name}</td>
                    
                    <td>
                      <Link to={`/editEquipo/${Equipo.name}`} className="btn btn-info">
                        <i className="fa-solid fa-pen-to-square"></i>
                      </Link>
                      <button onClick={() => deleteEquipo (Equipo.name)} className="btn btn-danger">
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

export default CompShowEquipos;