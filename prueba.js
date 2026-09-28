// Asumiendo que tienes un botón llamado 'guardar' y datos que enviar
guardar.addEventListener("click", async () => {
  guardar.disabled = true;
  resultado.textContent = "Guardando datos…";

  // Aquí defines los datos que quieres enviar a la API
  const datosNuevaLiga = {
    nombre: "LaLiga",
    pais: "España",
  };

  try {
    const respuesta = await fetch("http://127.0.0.1:8000/ligas/", {
      method: "POST", // 1. Cambiamos el método a POST
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json", // 2. Indicamos que enviamos un JSON
      },
      body: JSON.stringify(datosNuevaLiga), // 3. Convertimos el objeto JS a texto JSON
    });

    const cuerpo = await respuesta.text();
    resultado.textContent = `HTTP ${respuesta.status}\n${cuerpo}`;
  } catch (error) {
    resultado.textContent = `Error de conexión: ${error.message}`;
  } finally {
    guardar.disabled = false;
  }
});
