
export default function LogIn() {

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
                <p id="welcome">¡¡ Bienvenido a "Mi empleado" !!</p>
                <div id="login">
                        <input type="text" id="#dniInput"/>
                        <input type="text" id="passwordInput"/>
                </div>
            </main>
        </>
    )
}