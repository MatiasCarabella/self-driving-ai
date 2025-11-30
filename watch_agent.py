"""
Watch the trained agent perform without training/learning.
This is evaluation mode - the agent uses its learned knowledge deterministically.
"""
from config import SESSION_CONFIG

# Override config for evaluation mode
SESSION_CONFIG["TRAINING_MODE"] = False  # No learning
SESSION_CONFIG["NUM_EPISODES"] = 5       # Watch 5 episodes
SESSION_CONFIG["HEADLESS"] = False       # Show visualization
SESSION_CONFIG["MANUAL_CONTROL"] = False # Agent controls

# Import and run main
from main import main

if __name__ == "__main__":
    print("=" * 60)
    print("  EVALUATION MODE - Watching Trained Agent")
    print("=" * 60)
    print(f"Episodes to watch: {SESSION_CONFIG['NUM_EPISODES']}")
    print(f"Episode duration: {SESSION_CONFIG['EPISODE_DURATION']}s")
    print()
    print("The agent will use its learned knowledge without exploring.")
    print("No training or logging will occur.")
    print("=" * 60)
    print()
    
    main()
