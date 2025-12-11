import axios from 'axios';
import { useState, useEffect } from 'react';
import estilo from './Ambientes.module.css';

export function Ambientes() {
    const [ambientes, setAmbientes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            setError("Usuário não autenticado");
            setLoading(false);
            return;
        }

        axios.get('http://127.0.0.1:8000/api/ambientes/', {
            headers: { 'Authorization': `Bearer ${token}` }
        })
            .then(response => {
                setAmbientes(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error("Erro ao buscar os ambientes", error);
                setError("Erro ao carregar ambientes");
                setLoading(false);
            });
    }, []);

    if (loading) {
        return (
            <div className={estilo.container}>
                <div className={estilo.loading}>Carregando ambientes...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className={estilo.container}>
                <div className={estilo.error}>{error}</div>
            </div>
        );
    }

    return (
        <div className={estilo.container}>
            <div className={estilo.tableWrapper}>
                <h2 className={estilo.title}>Ambientes Monitorados</h2>
                <div className={estilo.tableContainer}>
                    <table className={estilo.table}>
                        <thead>
                            <tr>
                                <th>SIG</th>
                                <th>Descrição</th>
                                <th>Responsável</th>
                            </tr>
                        </thead>
                        <tbody>
                            {ambientes.map(ambiente => (
                                <tr key={ambiente.id}>
                                    <td className={estilo.sigCell}>{ambiente.local}</td>
                                    <td>{ambiente.descricao}</td>
                                    <td>{ambiente.nome}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    {ambientes.length === 0 && (
                        <div className={estilo.emptyMessage}>
                            Nenhum ambiente cadastrado
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}