import os
import matplotlib.pyplot as plt
import numpy as np

def read_log(file_path):
    episodes = []
    scores = []

    with open(file_path, "r") as f:
        for line in f:
            episode, score = line.strip().split(", ")
            episodes.append(int(episode))
            scores.append(float(score))
    
    return episodes, scores

def plot_progress(episodes, scores):
    plt.figure(figsize=(10, 6))
    plt.plot(episodes, scores, marker='o', linestyle='-', color='b')
    plt.title("Progreso del Agente a lo Largo de los Episodios")
    plt.xlabel("Número de Episodio")
    plt.ylabel("Puntuación Final")
    plt.axhline(0, color='red', linestyle='--', label='Puntuación 0')  # Línea horizontal en 0
    plt.legend()
    plt.grid()

    # Número de ticks deseados
    num_ticks_x = 20  # Número de ticks en el eje X
    num_ticks_y = 15  # Número de ticks en el eje Y

    # Calcular el espaciado de los ticks en el eje X
    x_min = round_to_nearest_five(min(episodes))  # Redondear el mínimo al múltiplo de 5 más cercano
    x_max = round_to_nearest_five(max(episodes))  # Redondear el máximo al múltiplo de 5 más cercano
    tick_spacing_x = round_to_nearest_five((x_max - x_min) / num_ticks_x)  # Redondear al múltiplo de 5
    x_ticks = range(x_min, x_max + 1, tick_spacing_x)  # Generar ticks
    plt.xticks(x_ticks)  # Aplicar ticks al eje X

    # Calcular el espaciado de los ticks en el eje Y
    y_min = round_to_nearest_five(min(scores))  # Redondear el mínimo al múltiplo de 5 más cercano
    y_max = round_to_nearest_five(max(scores))  # Redondear el máximo al múltiplo de 5 más cercano
    tick_spacing_y = round_to_nearest_five((y_max - y_min) / num_ticks_y)  # Redondear al múltiplo de 5
    y_ticks = np.arange(y_min, y_max + tick_spacing_y, tick_spacing_y)  # Generar ticks
    plt.yticks(y_ticks)  # Aplicar ticks al eje Y

    plt.show()


def round_to_nearest_five(value):
    """Redondea el valor al múltiplo de 5 más cercano."""
    return int(np.round(value / 5) * 5)

def main():
    # Obtener la ruta absoluta del directorio donde se está ejecutando el archivo .py
    current_directory = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(current_directory, "training_log.txt")
    episodes, scores = read_log(log_file)
    plot_progress(episodes, scores)

if __name__ == "__main__":
    main()