# Training Tips - Helping Your Agent Learn Better

## Problem: Agent Stuck in Local Optimum

Your agent learned to turn right but can't find the left turn on the sharp corner. This is a common RL problem called "local optimum" - the agent found a decent strategy and stopped exploring.

## Solutions

### 1. Boost Exploration (Recommended First Step)

Run the exploration boost script:
```bash
python retrain_exploration.py
```

**What it does:**
- Slows exploration decay: 0.995 → 0.998
- Increases minimum exploration: 0.05 → 0.15
- Trains for 5000 episodes with more exploration
- Keeps existing knowledge but explores more

**Why it works:**
- Agent keeps trying new actions longer
- 15% chance to explore even late in training
- More likely to discover the left turn

### 2. Adjust Reward Function

The agent might need better incentives for forward progress. Consider:

**In `config.py`, try:**
```python
REWARD_CONFIG = {
    "FORWARD_PROGRESS_WEIGHT": 1.0,  # Increase to 1.5 or 2.0
    "COLLISION_PENALTY": -5.0,       # Reduce penalty (was -10)
}
```

**Why it works:**
- Encourages trying new paths
- Less afraid of collisions during exploration
- Rewards distance traveled more

### 3. Add Checkpoints to Circuit

Add gray pixels (RGB: 128, 128, 128) to `assets/images/circuit_2.png`:
- Place checkpoints at key points (before/after turns)
- Agent gets +10 reward for passing checkpoints
- Guides learning toward completing the track

**Why it works:**
- Provides intermediate goals
- Rewards progress even if agent crashes later
- Helps discover the full track

### 4. Curriculum Learning

Train on easier circuits first, then progress to harder ones:

1. Start with `circuit_1.png` (if simpler)
2. Once mastered, switch to `circuit_2.png`
3. Agent transfers knowledge to harder tracks

**In `models/environment.py`, change:**
```python
circuit_image_path = os.path.join(parent_directory, "assets/images/circuit_1.png")
```

### 5. Reset and Retrain from Scratch

If the agent is too stuck, start fresh:

```bash
# Backup current progress
copy machine_learning\q_learning\q_tables\v2.pkl machine_learning\q_learning\q_tables\v2_backup.pkl

# Delete current Q-table
del machine_learning\q_learning\q_tables\v2.pkl

# Train from scratch with better parameters
python retrain_exploration.py
```

### 6. Increase Episode Duration

Give the agent more time to explore:

**In `config.py`:**
```python
SESSION_CONFIG = {
    "EPISODE_DURATION": 30,  # Increase from 20 to 30 seconds
}
```

**Why it works:**
- More time to try different strategies
- Can explore further before episode ends

## Recommended Approach

**Step 1:** Try exploration boost (easiest)
```bash
python retrain_exploration.py
```

**Step 2:** If still stuck, adjust rewards in `config.py`:
- Increase `FORWARD_PROGRESS_WEIGHT` to 1.5
- Reduce `COLLISION_PENALTY` to -5.0

**Step 3:** If still stuck, add checkpoints to the circuit image

**Step 4:** Last resort - reset and retrain from scratch with better parameters

## Monitoring Progress

After retraining, check if it's working:
```bash
# Watch the agent
python watch_agent.py

# Check training progress
python visualization/plot_training.py
```

Look for:
- ✅ Increasing distance over time
- ✅ Agent attempting left turns
- ✅ Higher peak distances

## Understanding the Issue

**Why agents get stuck:**
- Early success with right turns → high rewards
- Exploration decays → stops trying new things
- Never discovers left turn → stuck at local optimum

**The fix:**
- Keep exploring longer (higher epsilon)
- Better reward shaping (guide toward goal)
- Intermediate rewards (checkpoints)
