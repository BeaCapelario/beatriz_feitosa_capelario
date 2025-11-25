import estilo from './Menu.module.css';

export function Menu() {
  return (
    
    <nav className={estilo.menuGrid}>
      <a href="#" className={estilo.menuItem}>Home</a>
      <a href="#" className={estilo.menuItem}>Ambientes</a>
      <a href="#" className={estilo.menuItem}>Sensores</a>
      <a href="#" className={estilo.menuItem}>Histórico</a>
    </nav>

  );
}
