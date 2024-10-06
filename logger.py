import os

class Logger:
    def __init__(self, log_file="training_log.txt"):
        self.log_file = log_file

    def get_last_episode(self):
        """Lee el último número de episodio desde el archivo de logs."""
        try:
            with open(self.log_file, "r") as log_file:
                lines = log_file.readlines()
                if lines:
                    last_line = lines[-1]  # Obtener la última línea
                    last_episode = int(last_line.split(',')[0])  # Leer el número de episodio
                    return last_episode
        except FileNotFoundError:
            return 0  # Si el archivo no existe, devolver 0

    def log_episode(self, episode_number, score):
        """Guarda el número del episodio y el puntaje en el archivo de logs."""
        with open(self.log_file, "a") as log_file:
            log_file.write(f"{episode_number}, {score}\n")  # Formato simple