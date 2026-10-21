#!/usr/bin/env python3
"""Genera la coleccion de escenas de OBS (obs/escenas/Twitch_Chris.json).

Pistas de audio:
  Pista 1 = directo (todo, incluida la musica)
  Pista 2 = VOD de Twitch (todo MENOS la musica)
mixers es una mascara de bits: 1 = solo pista 1, 3 = pistas 1 y 2.
"""
import json
from pathlib import Path

SALIDA = Path(__file__).resolve().parent.parent / "obs" / "escenas" / "Twitch_Chris.json"

DIRECTO = 1          # solo pista 1
DIRECTO_Y_VOD = 3    # pistas 1 + 2
SIN_AUDIO = 0


def db(valor):
    return round(10 ** (valor / 20), 4)


def fuente(nombre, tipo, ajustes=None, mixers=SIN_AUDIO, volumen=1.0,
           filtros=None, versioned_id=None, monitoreo=0):
    return {
        "name": nombre,
        "id": tipo,
        "versioned_id": versioned_id or tipo,
        "settings": ajustes or {},
        "mixers": mixers,
        "volume": volumen,
        "balance": 0.5,
        "muted": False,
        "enabled": True,
        "flags": 0,
        "sync": 0,
        "monitoring_type": monitoreo,
        "push-to-mute": False,
        "push-to-talk": False,
        "filters": filtros or [],
        "hotkeys": {},
    }


def filtro(nombre, tipo, ajustes, versioned_id=None):
    return {"name": nombre, "id": tipo, "versioned_id": versioned_id or tipo,
            "settings": ajustes, "enabled": True, "mixers": 0, "volume": 1.0,
            "muted": False, "flags": 0, "sync": 0, "balance": 0.5,
            "hotkeys": {}, "monitoring_type": 0}


def item(nombre, x=0, y=0, ancho=None, alto=None, visible=True, bloqueado=False):
    datos = {
        "name": nombre, "visible": visible, "locked": bloqueado, "rot": 0.0,
        "pos": {"x": float(x), "y": float(y)}, "scale": {"x": 1.0, "y": 1.0},
        "align": 5, "bounds_type": 0, "bounds_align": 0,
        "bounds": {"x": 0.0, "y": 0.0},
        "crop_left": 0, "crop_top": 0, "crop_right": 0, "crop_bottom": 0,
        "scale_filter": "disable", "blend_method": "default",
        "blend_type": "normal", "group_item_backup": False,
    }
    if ancho and alto:
        # Ajustar a un recuadro manteniendo la proporcion
        datos["bounds_type"] = 2
        datos["bounds"] = {"x": float(ancho), "y": float(alto)}
    return datos


def escena(nombre, items):
    for i, it in enumerate(items, start=1):
        it["id"] = i
    return fuente(nombre, "scene", {"id_counter": len(items), "custom_size": False, "items": items})


def texto(nombre, contenido, tamano=110):
    return fuente(nombre, "text_gdiplus", {
        "text": contenido,
        "font": {"face": "Arial", "style": "Bold", "size": tamano, "flags": 1},
        "color": 4294967295, "outline": True, "outline_size": 6,
        "outline_color": 4278190080, "align": "center", "valign": "center",
    }, versioned_id="text_gdiplus_v3")


def color(nombre, abgr):
    return fuente(nombre, "color_source", {"color": abgr, "width": 1920, "height": 1080},
                  versioned_id="color_source_v3")


filtros_mic = [
    filtro("1 Supresion de ruido", "noise_suppress_filter", {"method": "rnnoise"},
           versioned_id="noise_suppress_filter_v2"),
    filtro("2 Puerta de ruido", "noise_gate_filter",
           {"open_threshold": -26.0, "close_threshold": -32.0,
            "attack_time": 25, "hold_time": 200, "release_time": 150}),
    filtro("3 Compresor", "compressor_filter",
           {"ratio": 4.0, "threshold": -18.0, "attack_time": 6,
            "release_time": 60, "output_gain": 0.0}),
    filtro("4 Limitador", "limiter_filter", {"threshold": -6.0, "release_time": 60}),
]

fuentes = [
    # --- Audio ---
    fuente("Microfono", "wasapi_input_capture", {"device_id": "default"},
           mixers=DIRECTO_Y_VOD, filtros=filtros_mic),
    fuente("Musica (solo directo)", "wasapi_process_output_capture",
           {"window": "Spotify:Chrome_WidgetWin_1:Spotify.exe", "priority": 2},
           mixers=DIRECTO, volumen=db(-18)),
    fuente("Audio Discord", "wasapi_process_output_capture",
           {"window": "Discord:Chrome_WidgetWin_1:Discord.exe", "priority": 2},
           mixers=DIRECTO_Y_VOD),
    # --- Video ---
    fuente("Captura de juego", "game_capture",
           {"capture_mode": "any_fullscreen", "capture_audio": True,
            "capture_cursor": True, "allow_transparency": False},
           mixers=DIRECTO_Y_VOD),
    fuente("Captura de pantalla", "monitor_capture", {"monitor": 0, "capture_cursor": True}),
    fuente("Camara", "dshow_input", {"res_type": 0, "active": True}),
    fuente("Alertas", "browser_source",
           {"url": "", "width": 1920, "height": 1080, "fps": 30,
            "reroute_audio": True, "shutdown": False, "restart_when_active": False},
           mixers=DIRECTO_Y_VOD),
    fuente("Chat", "browser_source",
           {"url": "", "width": 420, "height": 700, "fps": 30, "shutdown": True}),
    color("Fondo", 4280163856),
    texto("Texto Empezando", "EMPEZAMOS EN BREVE"),
    texto("Texto Pausa", "VUELVO ENSEGUIDA"),
    texto("Texto Final", "GRACIAS POR VER\nNOS VEMOS EN EL PROXIMO DIRECTO", 80),
]

# Escena anidada con lo que se repite en todas las escenas
comun = escena("[Comun] Alertas", [item("Alertas")])

escenas = [
    escena("1 - Empezando", [
        item("Fondo", bloqueado=True), item("Texto Empezando", 460, 470),
        item("Musica (solo directo)"), item("[Comun] Alertas"),
    ]),
    escena("2 - Juego", [
        item("Captura de juego", 0, 0, 1920, 1080),
        item("Camara", 1440, 790, 460, 270),
        item("Microfono"), item("Audio Discord"),
        item("Musica (solo directo)", visible=False),
        item("[Comun] Alertas"),
    ]),
    escena("3 - Pantalla / Charla", [
        item("Fondo", bloqueado=True),
        item("Captura de pantalla", 40, 40, 1400, 788),
        item("Camara", 1460, 40, 420, 236),
        item("Chat", 1460, 300, 420, 740),
        item("Microfono"), item("Audio Discord"),
        item("Musica (solo directo)", visible=False),
        item("[Comun] Alertas"),
    ]),
    escena("4 - Pausa", [
        item("Fondo", bloqueado=True), item("Texto Pausa", 520, 470),
        item("Musica (solo directo)"), item("[Comun] Alertas"),
    ]),
    escena("5 - Final", [
        item("Fondo", bloqueado=True), item("Texto Final", 260, 440),
        item("Musica (solo directo)"), item("[Comun] Alertas"),
    ]),
]

coleccion = {
    "name": "Twitch_Chris",
    "current_scene": "1 - Empezando",
    "current_program_scene": "1 - Empezando",
    "scene_order": [{"name": e["name"]} for e in escenas],
    "sources": fuentes + [comun] + escenas,
    "groups": [],
    "quick_transitions": [],
    "transitions": [],
    "current_transition": "Fade",
    "transition_duration": 300,
    "preview_locked": False,
    "scaling_enabled": False,
    "modules": {},
}

SALIDA.write_text(json.dumps(coleccion, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Generado {SALIDA}")
