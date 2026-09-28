const consultar = document.querySelector("#consultar");
const resultado = document.querySelector("#resultado");

consultar.addEventListener("click", async () => {
  consultar.disabled = true;
  resultado.textContent = "Consultando…";

  try {
    const respuesta = await fetch("http://127.0.0.1:8000/ligas/", {
      method: "GET",
      headers: { Accept: "application/json" },
    });

    const cuerpo = await respuesta.text();
    resultado.textContent = `HTTP ${respuesta.status}\n${cuerpo}`;
  } catch (error) {
    resultado.textContent = `Error de conexión: ${error.message}`;
  } finally {
    consultar.disabled = false;
  }
});

const enviar = document.querySelector("#enviar");
const nombre_liga = document.querySelector("#nombre_liga");
const pais_liga = document.querySelector("#pais_liga");

enviar.addEventListener("click", async () => {
  enviar.disabled = true;
  resultado.textContent = "Guardando datos…";
  const raw = JSON.stringify({
    nombre_liga: nombre_liga.value,
    pais: pais_liga.value,
  });
  try {
    const respuesta = await fetch("http://127.0.0.1:8000/ligas/", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: raw,
      redirect: "follow",
    });

    const cuerpo = await respuesta.text();
    resultado.textContent = `HTTP ${respuesta.status}\n${cuerpo}`;
  } catch (error) {
    resultado.textContent = `Error de conexión: ${error.message}`;
  } finally {
    enviar.disabled = false;
  }
});

const id = document.querySelector("#id_liga");
const actualizar = document.querySelector("#actualizar");

actualizar.addEventListener("click", async () => {
  actualizar.disabled = true;
  resultado.textContent = "Guardando datos…";
  const raw = JSON.stringify({
    nombre_liga: nombre_liga.value,
    pais: pais_liga.value,
  });
  try {
    const respuesta = await fetch(`http://127.0.0.1:8000/ligas/${id.value}`, {
      method: "PUT",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: raw,
      redirect: "follow",
    });

    const cuerpo = await respuesta.text();
    resultado.textContent = `HTTP ${respuesta.status}\n${cuerpo}`;
  } catch (error) {
    resultado.textContent = `Error de conexión: ${error.message}`;
  } finally {
    actualizar.disabled = false;
  }
});

const eliminar = document.querySelector("#eliminar");

eliminar.addEventListener("click", async () => {
  eliminar.disabled = true;
  resultado.textContent = "Guardando datos…";
  const raw = JSON.stringify({
    nombre_liga: nombre_liga.value,
    pais: pais_liga.value,
  });
  try {
    const respuesta = await fetch(`http://127.0.0.1:8000/ligas/${id.value}`, {
      method: "DELETE",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: raw,
      redirect: "follow",
    });

    const cuerpo = await respuesta.text();
    resultado.textContent = `HTTP ${respuesta.status}\n${cuerpo}`;
  } catch (error) {
    resultado.textContent = `Error de conexión: ${error.message}`;
  } finally {
    eliminar.disabled = false;
  }
});
