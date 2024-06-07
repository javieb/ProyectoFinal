import Image from 'next/image';

import altasButton from '../img/altasButton.png';
import Registries from './registries';
import styles from './registries.module.css'; // Importa el archivo CSS

async function getRegistries() {

  const token: string = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTk1NjUyMDAsImlhdCI6MTcxNjk3MzIwMCwiaWQiOiIxMjM0NTY3OEUifQ.Q-u6xUcy_lrqQphaX86kA8XXBaCe_dwQ4VFi58yRhCg';

  try {

    const response = await fetch('http://127.0.0.1:8000/trackday/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      }
    });
    return response.json();

  } catch (error) {
    console.error('Error fetching holidays:', error);
    throw error;
  }
}


export default async function Page(props: any) {

  let getTable = await getRegistries();

  return (
    <>
      <header>
        <nav>
          <div id="Banner">
            <div id="BannerButtons">
              <div id="Inicio">
                <p>Inicio</p>
              </div>
              <div id="Personal">
                <p>Personal</p>
              </div>
            </div>
          </div>
        </nav>
      </header>
      <main>
        <div id="breadcrum">
          <p>Personal / Registro horario</p>
        </div>

        <button id="altasButton">
          <p>Altas</p>
          <Image src={altasButton} alt="plusButton" width={25} height={25} />
        </button>

        <section id="holidaysNAbsences">
          <div id="title">
            <p>Tu registro horario </p>
          </div>

          <div id="tableHolidays">

            <table className={styles.table}>
              <thead>
                <tr>
                  <th>
                    Tipo
                  </th>
                  <th>
                    Hora
                  </th>
                  <th>
                    Fecha
                  </th>
                  <th>
                    Comentarios
                  </th>
                </tr>
              </thead>
              <tbody>
                {
                  getTable["data"]["trackdays"].map((json: any) => (
                    <Registries json={json} />
                  ))
                }
              </tbody>
            </table>

            <div className={styles.divPage}>

              <label htmlFor="Page">Page:</label>
              <input type="number" id="Page" style={{ width: '50px', textAlign: 'center' }} />
            </div>
          </div>
        </section>
      </main>
    </>)
}
