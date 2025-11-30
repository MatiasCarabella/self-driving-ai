"""
Fast training script - runs in headless mode for maximum speed.

This is now just a convenience wrapper. You can also use:
    python main.py --headless --episodes 10000

Usage:
    python train_fast.py              # 10k episodes on current circuit
    python train_fast.py --circuit circuit_1 --episodes 5000
"""
import sys
import time
from config import SESSION_CONFIG

# Override config for fast training
SESSION_CONFIG["HEADLESS"] = True
SESSION_CONFIG["TRAINING_MODE"] = True
SESSION_CONFIG["NUM_EPISODES"] = 10000

# Import and run main
from main import main

if __name__ == "__main__":
    circuit = SESSION_CONFIG.get("CIRCUIT", "circuit_2")
    episodes = SESSION_CONFIG["NUM_EPISODES"]
    
    print("=" * 60)
    print(f"  FAST TRAINING: {episodes:,} EPISODES")
    print("=" * 60)
    print(f"Circuit: {circuit}")
    print(f"Episodes: {episodes:,}")
    print(f"Mode: Headless (no rendering)")
    print(f"Estimated time: {episodes / 1000 * 1.5:.0f}-{episodes / 1000 * 2:.0f} minutes")
    print("=" * 60)
    print()
    
    start = time.time()
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user!")
        elapsed = time.time() - start
        print(f"Elapsed time: {elapsed / 60:.1f} minutes")
    
    elapsed = time.time() - start
    print("\n" + "=" * 60)
    print(f"Training complete! Time: {elapsed / 60:.1f} minutes")
    print("=" * 60)
