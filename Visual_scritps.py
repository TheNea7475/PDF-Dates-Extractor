import os
import time

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def loading_bar(total_steps=50, duration=5):
    """
    Displays a loading bar that fills progressively.
    
    Args:
    - total_steps (int): The total number of steps for the bar.
    - duration (int or float): Total duration for the bar to complete in seconds.
    """
    for step in range(total_steps + 1):
        filled = '■' * step
        empty = '□' * (total_steps - step)
        print(f'\r[{filled}{empty}] {step / total_steps * 100:.1f}%', end='', flush=True)
        time.sleep(duration / total_steps)
    print()  # To move to the next line after completion


def loading_bar_controlled(current_step, total_steps=50):
    """
    Updates the loading bar based on the current progress.

    Args:
    - current_step (int): The current step or progress.
    - total_steps (int): The total number of steps for the bar.
    """
    filled = '■' * current_step
    empty = '□' * (total_steps - current_step)
    print(f'\r[{filled}{empty}] {current_step / total_steps * 100:.1f}%', end='', flush=True)
