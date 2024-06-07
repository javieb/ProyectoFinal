import styles from './registries.module.css'; // Importa el archivo CSS

export default function Registries({json} : any) {


  return (
      <tr className={styles.tr}>
        <td>{json.type}</td>
        <td>{json.hour}</td>
        <td>{json.date}</td>
        <td>{json.comments}</td>
      </tr>
  )
}