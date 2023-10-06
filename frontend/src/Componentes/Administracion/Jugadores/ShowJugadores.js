import axios from "axios";
import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import CompInicioAdmin from "../inicioAdministracion";





const URI='http://127.0.0.1:8000/olimpic/jugadores/'

const CompShowJugadores = () => {
    const [Jugadores,setJugadores]= useState([])
    useEffect(()=>{
        getJugadores()
    },[])

    
    //procedimiento para mostrar todos los componentes
    const getJugadores = async() =>{
        const res = await axios.get(URI)
        setJugadores(res.data)

    }
    
   const componetRef = useRef();

    //procedimiento para eleminar un registro
    const  deleteJugadores  =async (id) => {
        await axios.delete(`${URI}${id}`)
        getJugadores()
    }
    return(
        <>
       <CompInicioAdmin></CompInicioAdmin>
        <div className="container">
        <div className="row">
        
            <div className="col" >
                
            <Link to="/createjugador" className="btn btn-success">Crear Jugador <i class="fa-solid fa-plus"></i></Link>
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
                        {Jugadores.map((jugador)=>(
                            <tr key={jugador.id}>
                                <td>{jugador.identifier_number}</td>
                                <td>{jugador.number}</td>
                                <td>{jugador.player_name}</td>
                                <td>{jugador.position}</td>
                        
                                <td>
                                    <Link to={`/editJugador/${jugador.id}`} className="btn btn-info"><i class="fa-solid fa-pen-to-square"></i></Link>
                                    <button onClick={()=>deleteJugadores(jugador.id)} className="btn btn-danger"><i class="fa-solid fa-trash"></i></button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                
            </div>
            
        </div>
        
        
         </div>
    </>
    ) 
   
}

export default CompShowJugadores