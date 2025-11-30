"""
Fast training script - runs in headless mode for maximum speed.
Simply sets HEADLESS=True and runs main.py logic.
"""
from config import SESSION_CONFIG

# Override config for fast training
SESSION_CONFIG["HEADLESS"] = True
SESSION_CONFIG["TRAINING_MODE"] = True
SESSION_CONFIG["NUM_EPISODES"] = 1000  # 10k episodes sequentially

# Import and run main
from main import main

if __name__ == "__main__":
    print("=" * 60)
    print("  SEQUENTIAL FAST TRAINING: 10,000 EPISODES")
    print("=" * 60)
    print(f"Episodes: {SESSION_CONFIG['NUM_EPISODES']:,}")
    print(f"Mode: Headless (no rendering)")
    print(f"Estimated time: 15-20 minutes")
    print("=" * 60)
    print()
    
    import time
    start = time.time()
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user!")
        elapsed = time.time() - start
        print(f"Elapsed time: {elapsed / 60:.1f} minutes")
        print(f"Episodes completed: ~{int(elapsed / 0.1)}")
    
    print("\n" + "=" * 60)
    print("Sequential training complete!")
    print("This should show better learning than parallel training.")
    print("=" * 60)
