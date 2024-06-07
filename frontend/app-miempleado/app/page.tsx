
import HolidaysRegistries from './holidaysNabsences/holidaysRegistries';
import styles from './holidaysNabsences/holidays.module.css';
import styles2 from './app.module.css';

async function getHolidays() {

  const token: string = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTk1NjUyMDAsImlhdCI6MTcxNjk3MzIwMCwiaWQiOiIxMjM0NTY3OEUifQ.Q-u6xUcy_lrqQphaX86kA8XXBaCe_dwQ4VFi58yRhCg';

  try {

    const response = await fetch('http://127.0.0.1:8000/holidays-absences/', {
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

async function getlastAccess() {

  const token: string = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTk1NjUyMDAsImlhdCI6MTcxNjk3MzIwMCwiaWQiOiIxMjM0NTY3OEUifQ.Q-u6xUcy_lrqQphaX86kA8XXBaCe_dwQ4VFi58yRhCg';

  try {

    const response = await fetch('http://127.0.0.1:8000/lastAccess/', {
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

export default async function Page() {

  const getTable = await getHolidays();
  const lastAccess = await getlastAccess();

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
        <p>Inicio</p>
      </div>

      <section className={styles2.primaryFunctions}>
        <div id="buttonRegistries">
          <button>
            In pause
          </button>
        </div>
        <div id="lastAccess">
          {lastAccess.data.type}: {lastAccess.data.date} a las {lastAccess.data.time}
        </div>
        <div className={styles2.holidays}>
          Te quedan 20 días de vacaciones
        </div>
      </section>

      <section id="holidaysNAbsences">

        <div id="tableHolidays">

          <table className={styles.table}>
            <thead>
              <tr>
                <th>
                  Asunto
                </th>
                <th>
                  Tipo
                </th>
                <th>
                  Fecha inicio
                </th>
                <th>
                  Fecha fin
                </th>
                <th>
                  Comentarios
                </th>
              </tr>
            </thead>
            <tbody>
              {
                getTable["data"].map((json: any) => (
                  <HolidaysRegistries json={json} />
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
