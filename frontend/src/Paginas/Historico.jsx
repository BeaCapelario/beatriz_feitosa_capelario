import axios from 'axios';
import { useState, useEffect } from 'react';
import estilo from './Historico.module.css';

export function Historico() {
    const [historico, setHistorico] = useState([]);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (!token) return;

        axios.get('http://127.0.0.1:8000/api/historico/', {
            headers: { 'Authorization': `Bearer ${token}` }
        })
            .then(response => setHistorico(response.data))
            .catch(error => console.error("Erro ao buscar os ambientes", error));
    }, []);

    return (
        <div className={estilo.container}>
            <table className={estilo.historico}>
                <thead>
                    <tr>
                        <th>Sensor</th>
                        <th>Valor</th>
                        <th>Horario</th>
                    </tr>
                </thead>

                <tbody>
                    {historico.map(sensor => {
                        <tr key={sensor.id}>
                            <td>{historico.sensor}</td>
                            <td>{historico.valor}</td>
                            <td>{historico.timestamp}</td>
                        </tr>
                    })}
                </tbody>
            </table>
        </div>
    )
}