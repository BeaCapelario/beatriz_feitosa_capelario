import axios from 'axios';
import { useState, useEffect } from 'react';
import estilo from './Ambientes.module.css';

export function Ambientes() {
    const [ambientes, setAmbientes] = useState([]);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (!token) return ;

        axios.get('http://127.0.0.1:8000/api/ambientes/', {
            headers: {'Authorization' : `Bearer ${token}` }
        })
        .then(response => setAmbientes(response.data))
        .catch(error => console.error("Erro ao buscar os ambientes", error));
    } , []);

    return (
        <div className={estilo["table-container"]}>
            <table className={estilo["table.ambientes"]}>
                <thead>
                    <tr>
                        <th>SIG</th>
                        <th>Descrição</th>
                        <th>Responsável</th>
                    </tr>
                </thead>

                <tbody>
                    {ambientes.map(ambientes => (
                        <tr key={ambientes.id}>
                            <td>{ambientes.sig}</td>
                            <td>{ambientes.description}</td>
                            <td>{ambientes.responsible_person}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}