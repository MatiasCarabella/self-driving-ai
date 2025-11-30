"""
Unified training visualization tool.
Replaces plot_metrics.py, plot_distance.py, and plot_progress.py
"""
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def load_metrics(metrics_file):
    """Load metrics from JSON lines file."""
    metrics = []
    if not os.path.exists(metrics_file):
        print(f"Metrics file not found: {metrics_file}")
        return None
    
    with open(metrics_file, 'r') as f:
        for line in f:
            try:
                metrics.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    return metrics

def plot_all_metrics(metrics_file="logs/q_learning/circuit2_v1_metrics.json"):
    """Plot distance progress - the main training metric."""
    metrics = load_metrics(metrics_file)
    
    if not metrics:
        print("No metrics to plot")
        return
    
    # Renumber episodes sequentially to merge multiple training sessions
    for i, m in enumerate(metrics, 1):
        m['sequential_episode'] = i
    
    episodes = [m['sequential_episode'] for m in metrics]
    distances = [m['distance_traveled'] for m in metrics]
    
    # Create responsive plot - smaller default size
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    fig.canvas.manager.set_window_title('Training Progress - Self-Driving AI')
    
    # Make window resizable
    try:
        fig.canvas.manager.window.state('normal')  # Start in normal state, not maximized
    except:
        pass
    
    total_episodes = len(episodes)
    
    # Modern color palette - blue theme
    COLOR_RAW = '#3498db'      # Soft blue for raw data
    COLOR_AVG = '#2c5aa0'      # Darker blue for moving average (stands out)
    COLOR_MAX = '#27ae60'      # Green for max line
    
    # Plot distance with raw data
    ax.plot(episodes, distances, alpha=0.4, label='Raw Distance', 
            color=COLOR_RAW, linewidth=0.9)
    
    # Find and mark new records (personal bests)
    record_episodes = []
    record_distances = []
    current_record = 0
    for ep, dist in zip(episodes, distances):
        if dist > current_record:
            current_record = dist
            record_episodes.append(ep)
            record_distances.append(dist)
    
    # Plot record markers
    if record_episodes:
        ax.scatter(record_episodes, record_distances, color='#e74c3c', s=80, 
                  marker='*', zorder=5, label='New Records', edgecolors='#c0392b', linewidths=1.5)
    
    # Moving average - make it stand out with darker blue
    if len(distances) >= 100:
        window = min(100, len(distances))
        moving_avg = np.convolve(distances, np.ones(window)/window, mode='valid')
        ax.plot(episodes[window-1:], moving_avg, label=f'{window}-Episode Average', 
                linewidth=3.5, color=COLOR_AVG, alpha=0.9)
    
    # Min/max reference lines
    min_dist = min(distances)
    max_dist = max(distances)
    ax.axhline(max_dist, color=COLOR_MAX, linestyle='--', linewidth=2, 
               alpha=0.8, label=f'Peak: {max_dist:.0f}')
    
    # Styling
    ax.set_xlabel('Episode', fontsize=13, fontweight='bold', color='#2c3e50')
    ax.set_ylabel('Distance Traveled', fontsize=13, fontweight='bold', color='#2c3e50')
    ax.set_title(f'Training Progress - {total_episodes:,} Episodes', 
                fontsize=15, fontweight='bold', pad=20, color='#2c3e50')
    
    # Add simplified stats box
    avg_dist_100 = np.mean(distances[-100:]) if len(distances) >= 100 else np.mean(distances)
    
    stats_text = f'Episodes: {total_episodes:,}\n'
    stats_text += f'Peak: {max_dist:.0f}\n'
    stats_text += f'Avg (100): {avg_dist_100:.0f}'
    
    # Flat stats box (matching legend style) - bottom left
    # Using same positioning offset as legend for symmetry
    props = dict(boxstyle='square,pad=0.8', facecolor='white', alpha=1.0, 
                 edgecolor='#d0d0d0', linewidth=1)
    ax.text(0.025, 0.04, stats_text, transform=ax.transAxes, fontsize=11, 
            va='bottom', ha='left', bbox=props, color='#2c3e50', zorder=10)
    
    # Flat legend box - bottom right
    ax.legend(fontsize=11, loc='lower right', framealpha=1.0, 
             edgecolor='#d0d0d0', fancybox=False, shadow=False, 
             frameon=True, borderpad=0.8)
    
    ax.grid(True, alpha=0.4, linestyle='--', linewidth=0.6, color='#95a5a6')
    ax.tick_params(labelsize=10, colors='#34495e')
    
    # Set background color for a cleaner look
    ax.set_facecolor('#fafafa')
    fig.patch.set_facecolor('white')
    
    # Make graph reach edges - remove margins
    ax.margins(x=0, y=0.02)  # No x-margin, tiny y-margin for breathing room
    
    # Make window resizable
    manager = plt.get_current_fig_manager()
    try:
        manager.window.state('normal')
    except:
        pass
    
    plt.show()

def plot_single_metric(metrics_file, metric='distance'):
    """Plot a single metric in detail."""
    metrics = load_metrics(metrics_file)
    
    if not metrics:
        print("No metrics to plot")
        return
    
    # Renumber episodes sequentially
    for i, m in enumerate(metrics, 1):
        m['sequential_episode'] = i
    
    episodes = [m['sequential_episode'] for m in metrics]
    
    # Select metric
    if metric == 'distance':
        values = [m['distance_traveled'] for m in metrics]
        ylabel = 'Distance Traveled'
        title = 'Distance Progress'
    elif metric == 'score':
        values = [m['score'] for m in metrics]
        ylabel = 'Score'
        title = 'Score Progress'
    else:
        print(f"Unknown metric: {metric}")
        return
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    fig.canvas.manager.set_window_title(f'Agent Progress: {title}')
    
    # Plot raw data
    ax.plot(episodes, values, color='lightblue', alpha=0.4, linewidth=0.8, label=f'Raw {metric}')
    
    # Moving average
    window_size = min(100, len(values) // 20)
    if window_size > 0:
        moving_avg = np.convolve(values, np.ones(window_size)/window_size, mode='valid')
        ax.plot(episodes[window_size-1:], moving_avg, color='darkblue', linewidth=2.5,
                label=f'Moving Avg ({window_size})')
    
    # Min/max lines
    min_val = min(values)
    max_val = max(values)
    ax.axhline(min_val, color='red', linestyle='--', linewidth=1, alpha=0.7)
    ax.axhline(max_val, color='green', linestyle='--', linewidth=1, alpha=0.7)
    
    ax.set_xlabel("Episode Number", fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='lower right', fontsize=9, framealpha=0.9)
    
    # Statistics box
    avg_last_100 = np.mean(values[-100:]) if len(values) >= 100 else np.mean(values)
    stats_text = f"Episodes: {len(episodes):,}\n"
    stats_text += f"Avg (last 100): {avg_last_100:.1f}\n"
    stats_text += f"Min: {min_val:.1f}\n"
    stats_text += f"Max: {max_val:.1f}"
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
            bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray', linewidth=1), 
            fontsize=9, verticalalignment='top', family='monospace')
    
    # Set x-axis range
    if len(episodes) > 0:
        min_ep = min(episodes)
        max_ep = max(episodes)
        ax.set_xlim(min_ep, max_ep)
    
    # Tight layout for better spacing
    plt.tight_layout()
    plt.show()

def main():
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    metrics_file = os.path.join(parent_directory, "logs/q_learning/circuit2_v1_metrics.json")
    
    # Parse command line arguments
    mode = 'all'  # Default: show all metrics
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['distance', 'score']:
            mode = arg
        elif arg.endswith('.json'):
            metrics_file = os.path.join(parent_directory, f"logs/q_learning/{sys.argv[1]}")
        else:
            print("Usage: python plot_training.py [all|distance|score] [metrics_file.json]")
            print("  all      - Show 4-panel comprehensive view (default)")
            print("  distance - Show detailed distance plot")
            print("  score    - Show detailed score plot")
            return
    
    if not os.path.exists(metrics_file):
        print(f"Error: Metrics file not found: {metrics_file}")
        return
    
    if mode == 'all':
        plot_all_metrics(metrics_file)
    else:
        plot_single_metric(metrics_file, mode)

if __name__ == "__main__":
    main()
