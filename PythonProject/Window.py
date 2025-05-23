﻿import tkinter as tk

# --- MODIF DEBUT ---
import Freenove_DHT as DHT11  # Module pour le capteur
import time
import threading  # Pour lire le capteur sans bloquer l'interface

# --- MODIF FIN ---

# --- MODIF DEBUT ---
# Variable pour stocker la température lue depuis le DHT11
current_temp = 0.0
# --- MODIF FIN ---

door = "Fermé"
mode = "Désactivé"
mode_value = "disabled"


def change_mode():
    global mode
    global mode_value
    if mode == "Désactivé":
        mode = "Activé"
        mode_value = "normal"
    else:
        mode = "Désactivé"
        mode_value = "disabled"
    test_mode.configure(text=f"Mode test : {mode}")
    change_state()


def change_state():
    plus_btn.configure(state=mode_value)
    minus_btn.configure(state=mode_value)
    open_btn.configure(state=mode_value)
    close_btn.configure(state=mode_value)
    start_btn.configure(state=mode_value)
    end_btn.configure(state=mode_value)


def plus_temp():
    # --- MODIF DEBUT ---
    # On incrémente la température "virtuelle" (utile si on veut simuler en mode test)
    global current_temp
    current_temp += 1
    temp_value_label.config(text=f"{current_temp:.1f} °C")
    # --- MODIF FIN ---


# --- MODIF DEBUT ---
def minus_temp():
    # Permet de diminuer la température "virtuelle" en mode test
    global current_temp
    current_temp -= 1
    temp_value_label.config(text=f"{current_temp:.1f} °C")


# --- MODIF FIN ---

# --- MODIF DEBUT ---
# Configuration du capteur DHT11 sur GPIO 4 (selon le montage sur la photo)
sensor = DHT11.DHT(pin=4)


def read_temp_loop():
    """
    Lit périodiquement la température et met à jour l'interface.
    Cette fonction tourne dans un thread pour ne pas bloquer Tkinter.
    """

    def loop():
        global current_temp
        while True:
            # Lecture du capteur
            result = sensor.readDHT11()
            # Vérifie si la lecture est valide
            if result.isValid():
                current_temp = result.temperature
                # Mise à jour de l'affichage
                temp_value_label.config(text=f"{current_temp:.1f} °C")
            # Attendre 2 secondes avant la prochaine lecture
            time.sleep(2)

    # On lance la boucle dans un thread "daemon"
    t = threading.Thread(target=loop, daemon=True)
    t.start()


# --- MODIF FIN ---

window = tk.Tk()
window.geometry('400x450')

title = tk.Label(window, text="Système de surveillance", font=("Arial", 15, "bold"), pady=10)

temp = tk.Label(window, text="Température:")
temp2 = tk.Label(window, text="Température:")

# --- MODIF DEBUT ---
# Renommage du label pour afficher la température lue par le capteur
temp_value_label = tk.Label(window, text="0.0", fg="red")
# --- MODIF FIN ---

door_status = tk.Label(window, text=f"État de la trappe : {door}", pady=10)

test_mode = tk.Label(window, text=f"Mode test : {mode}", fg="blue", pady=10, font=("Arial", 10, "bold"))

mode_btn = tk.Button(window, text="Basculer mode test", command=change_mode)

frame1 = tk.Frame(window)
# --- MODIF DEBUT ---
plus_btn = tk.Button(frame1, text="+", command=plus_temp, background="lightgreen", padx=8, pady=5, state=tk.DISABLED)
minus_btn = tk.Button(frame1, text="-", command=minus_temp, background="red", padx=8, pady=5, state=tk.DISABLED)
# --- MODIF FIN ---

door_text = tk.Label(window, text="Trappe :")
frame2 = tk.Frame(window)
open_btn = tk.Button(frame2, text="Ouvrir", command=change_mode, background="lightgreen", pady=5, state=tk.DISABLED)
close_btn = tk.Button(frame2, text="Fermer", command=change_mode, background="red", pady=5, state=tk.DISABLED)

alarm_text = tk.Label(window, text="Alarme :")
frame3 = tk.Frame(window)
start_btn = tk.Button(frame3, text="Activer", command=change_mode, background="lightgreen", pady=5, state=tk.DISABLED)
end_btn = tk.Button(frame3, text="Arreter", command=change_mode, background="red", pady=5, state="disabled")

title.pack()
temp.pack()

# --- MODIF DEBUT ---
# On affiche le label qui montre la température
temp_value_label.pack()
# --- MODIF FIN ---

door_status.pack()
test_mode.pack()
mode_btn.pack(pady=10)
temp2.pack()
frame1.pack(pady=5)
plus_btn.pack(side=tk.LEFT, padx=5, pady=5)
minus_btn.pack(side=tk.LEFT, padx=5, pady=5)
door_text.pack()
frame2.pack(pady=5)
open_btn.pack(side=tk.LEFT, padx=5, pady=5)
close_btn.pack(side=tk.LEFT, padx=5, pady=5)
alarm_text.pack()
frame3.pack(pady=5)
start_btn.pack(side=tk.LEFT, padx=5, pady=5)
end_btn.pack(side=tk.LEFT, padx=5, pady=5)

# --- MODIF DEBUT ---
# On lance le thread de lecture de la température
read_temp_loop()
# --- MODIF FIN ---

window.mainloop()
