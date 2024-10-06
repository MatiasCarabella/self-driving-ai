import os
import matplotlib.pyplot as plt

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
    
    plt.xticks(episodes)  # Mostrar todos los episodios en el eje X
    
    # Establecer ticks equidistantes en el eje Y
    y_min = min(scores)  # Mínimo puntaje
    y_max = max(scores)  # Máximo puntaje
    tick_spacing = 5  # Espaciado entre ticks en el eje Y
    y_ticks = range(int(y_min // tick_spacing) * tick_spacing, int(y_max // tick_spacing + 1) * tick_spacing, tick_spacing)
    
    plt.yticks(y_ticks)  # Establecer los ticks en el eje Y

    plt.show()

def main():
    # Obtener la ruta absoluta del directorio donde se está ejecutando el archivo .py
    current_directory = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(current_directory, "training_log.txt")
    episodes, scores = read_log(log_file)
    plot_progress(episodes, scores)

if __name__ == "__main__":
    main()