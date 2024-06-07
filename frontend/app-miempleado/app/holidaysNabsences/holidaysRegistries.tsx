import styles from './holidays.module.css'; // Importa el archivo CSS

export default function HolidaysRegistries({json} : any) {


  return (
      <tr key={json.id} className={styles.tr}>
        <td>{json.subject}</td>
        <td>{json.type}</td>
        <td>{json.start_date}</td>
        <td>{json.finish_date}</td>
        <td>{json.comments}</td>
      </tr>
  )
}