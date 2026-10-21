# Configuración de OBS para Twitch (escenas + audio sin copyright en VODs)

Todo lo necesario para stremear en Twitch desde OBS Studio (Windows, OBS 30 o superior):

| Archivo | Qué es |
|---|---|
| `obs/escenas/Twitch_Chris.json` | Colección de escenas lista para importar |
| `obs/perfil/Twitch_Chris/` | Perfil: video, codificador, Twitch y **pista de VOD** |
| `herramientas/generar_escenas.py` | Script que regenera el JSON de escenas si quieres cambiarlo |

---

## 1. Cómo funciona el truco anti‑copyright

OBS puede mandar a Twitch **dos pistas de audio**:

| Pista | Qué escucha | Contenido |
|---|---|---|
| **Pista 1 – Directo** | Tus viewers en vivo | Micrófono + juego + Discord + alertas + **música** |
| **Pista 2 – VOD** | Lo que se guarda en el VOD (y los destacados) | Micrófono + juego + Discord + alertas, **sin música** |

En vivo se escucha la música, pero el VOD se guarda sin ella. Así Twitch no te silencia ni te
borra los VODs por DMCA.

Enrutado de cada fuente (*Mezclador de audio → ⚙ → Propiedades avanzadas de audio*):

| Fuente | Pista 1 | Pista 2 |
|---|:-:|:-:|
| Micrófono | ✅ | ✅ |
| Captura de juego (audio del juego) | ✅ | ✅ |
| Audio Discord | ✅ | ✅ |
| Alertas | ✅ | ✅ |
| **Música (solo directo)** | ✅ | ❌ |

> ⚠️ **Muy importante:** en *Ajustes → Audio*, deja **"Audio del escritorio" en *Desactivado***.
> Si capturas todo el escritorio, la música de Spotify se cuela también en la pista 2. Por eso cada
> aplicación tiene su propia fuente (captura de audio de aplicación).

---

## 2. Instalación paso a paso

### 2.1 Importar el perfil
1. Descarga este repositorio (botón **Code → Download ZIP**) y descomprímelo.
2. En OBS: **Perfil → Importar** → selecciona la carpeta `obs/perfil/Twitch_Chris`.
3. **Perfil → Twitch_Chris** para activarlo.

### 2.2 Importar las escenas
1. **Colección de escenas → Importar** → selecciona `obs/escenas/Twitch_Chris.json`.
2. **Colección de escenas → Twitch_Chris**.
3. Si OBS avisa de archivos o dispositivos que faltan, pulsa **Continuar**; los ajustas en el paso 3.

### 2.3 Conectar Twitch
1. **Ajustes → Emisión** → Servicio: **Twitch** → **Conectar cuenta** (recomendado)
   o pega tu clave de transmisión de `dashboard.twitch.tv → Configuración → Transmisión`.
   **Nunca subas tu clave a GitHub ni la enseñes en el directo.**

### 2.4 Comprobar la pista de VOD (lo más importante)
1. **Ajustes → Salida** → Modo de salida: **Avanzado**.
2. Pestaña **Emisión**:
   - Pista de audio: **1**
   - ✅ **Pista de VOD de Twitch (usa la pista 2)**: marcada
     (esta casilla solo aparece si el servicio es Twitch y la salida está en modo Avanzado).
3. Pestaña **Audio**: Pista 1 = 160 kbps, Pista 2 = 160 kbps.
4. En **Twitch → Configuración → Transmisión**, activa **"Almacenar emisiones anteriores"**
   para que se guarden los VODs.

### 2.5 Codificador según tu tarjeta gráfica
El perfil viene con **NVIDIA NVENC H.264**. Si tu PC no tiene NVIDIA, cámbialo en
*Ajustes → Salida → Emisión → Codificador de video*:

| Tu hardware | Codificador | Ajustes |
|---|---|---|
| NVIDIA (GTX 16xx / RTX) | NVIDIA NVENC H.264 | CBR, 6000 kbps, keyframe 2 s, preset P5, Alta calidad |
| AMD | AMD HW H.264 (AVC) | CBR, 6000 kbps, keyframe 2 s, preset Calidad |
| Intel | QuickSync H.264 | CBR, 6000 kbps, keyframe 2 s |
| Solo CPU | x264 | CBR, 6000 kbps, keyframe 2 s, preset *veryfast* |

Video: base **1920×1080**, salida **1664×936**, **60 FPS**, filtro Lanczos.
Si tu subida (velocidad de upload, mídela en speedtest.net) es menor de 8 Mbps, baja a
**1280×720** y **4500 kbps**.

---

## 3. Ajustar las fuentes (una sola vez)

Doble clic sobre cada fuente:

| Fuente | Qué elegir |
|---|---|
| **Microfono** | Tu micrófono (no "Predeterminado" si tienes varios) |
| **Camara** | Tu webcam (1920×1080 o 1280×720, 30/60 fps) |
| **Captura de juego** | Modo "Capturar cualquier aplicación a pantalla completa" ya viene puesto, con **Capturar audio** activado |
| **Captura de pantalla** | Tu monitor principal |
| **Musica (solo directo)** | Ventana: `Spotify.exe` (o el reproductor que uses) |
| **Audio Discord** | Ventana: `Discord.exe` |
| **Alertas** | Pega la URL de alertas de StreamElements / Streamlabs |
| **Chat** | Pega la URL del chat overlay (o el pop‑out del chat de Twitch) |

### Filtros del micrófono (ya incluidos)
1. Supresión de ruido: RNNoise
2. Puerta de ruido: abre a −26 dB, cierra a −32 dB
3. Compresor: 4:1, umbral −18 dB
4. Limitador: −6 dB

Ajuste fino: habla normal y mira el medidor. La voz debería quedar entre **−15 y −10 dB**
(zona amarilla). Si la puerta te corta palabras, baja los dos umbrales 3–4 dB.

---

## 4. Escenas incluidas

| Escena | Contenido | Micrófono | Música |
|---|---|:-:|:-:|
| 1 - Empezando | Fondo + "EMPEZAMOS EN BREVE" | ❌ | ✅ |
| 2 - Juego | Juego a pantalla completa + cámara abajo a la derecha | ✅ | oculta (actívala con el 👁) |
| 3 - Pantalla / Charla | Pantalla + cámara + chat | ✅ | oculta (actívala con el 👁) |
| 4 - Pausa | Fondo + "VUELVO ENSEGUIDA" (micrófono fuera, nadie te oye) | ❌ | ✅ |
| 5 - Final | Fondo + "GRACIAS POR VER" | ❌ | ✅ |

`[Comun] Alertas` es una escena anidada metida en todas: si cambias las alertas, cambian en todas.

**Atajos recomendados** (*Ajustes → Atajos*): F1–F5 para cambiar de escena, una tecla para silenciar
el micrófono (*Microfono → Silenciar / Activar*).

---

## 5. Cosas que la pista de VOD **no** cubre

- **Clips:** los clips que hacen tus viewers salen de la pista del directo, **con música**.
  Twitch puede borrar clips por DMCA. Lo más seguro es usar música libre de derechos.
- **Música dentro del juego:** el audio del juego va al VOD. Si el juego tiene canciones con
  licencia (GTA, juegos de ritmo, radios…), baja la música en las opciones del juego o mueve
  "Captura de juego" a solo pista 1 mientras lo juegas.
- **Sonidos de alertas** con canciones comerciales: también llegan al VOD. Usa sonidos propios.
- **Cantar o poner canciones con micrófono abierto** también queda grabado.

### Música segura para directos (sin copyright)
- **StreamBeats** (gratis): YouTube, Spotify y Apple Music
- **Pretzel Rocks**
- **Epidemic Sound** / **Monstercat Gold** (de pago, con licencia para Twitch)

Con música de estas fuentes puedes incluso dejar la música en las dos pistas.

---

## 6. Checklist antes de cada directo
- [ ] Perfil **Twitch_Chris** y colección **Twitch_Chris** activos
- [ ] Ajustes → Audio → Audio del escritorio = **Desactivado**
- [ ] Ajustes → Salida → Emisión → **Pista de VOD de Twitch** marcada
- [ ] Graba 30 s de prueba (*Iniciar grabación*), ábrela en VLC → *Audio → Pista de audio* →
      la **pista 2 no debe tener música**
- [ ] Micrófono en zona amarilla, música baja (−18 dB de base)
- [ ] Empieza siempre en **1 - Empezando**
- [ ] Al terminar: **5 - Final** unos segundos → *Detener transmisión*

---

## Regenerar las escenas
Si quieres cambiar posiciones, textos o nombres, edita `herramientas/generar_escenas.py` y ejecuta:

```bash
python3 herramientas/generar_escenas.py
```

Luego vuelve a importar `obs/escenas/Twitch_Chris.json` en OBS.
