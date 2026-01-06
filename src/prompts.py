"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           YOUR TASK PROMPTS                                   ║
║                                                                               ║
║  CUSTOMIZE THIS FILE to define prompts/instructions for your task.            ║
║  Prompts are selected based on task type and returned to the model.           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random


# ══════════════════════════════════════════════════════════════════════════════
#  DEFINE YOUR PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

PROMPTS = {
    "default": [
        "Animate the symmetric expansion of the scatter pattern. Start with the initial scatter on the left, then smoothly reveal its mirror image on the right, creating a complete symmetric pattern along the vertical axis.",
        "Show the scatter pattern expanding symmetrically. Starting from the left half, gradually extend the pattern to the right half, creating a perfect mirror image along the central vertical axis.",
        "Demonstrate the symmetric expansion of the scatter pattern. Begin with the random scatter on the left, then smoothly generate the mirrored pattern on the right to form a fully symmetric shape.",
        "Animate the process of creating a symmetric scatter pattern. Starting with the initial scatter on the left, gradually reveal its mirror image on the right to complete the symmetric design.",
    ],
    
    "scatter": [
        "Show the random scatter expanding symmetrically. The initial scatter on the left should be mirrored to the right, creating a perfect symmetric pattern along the vertical axis.",
        "Animate the symmetric extension of the scatter. Start with the left side scatter, then gradually reveal its mirror image on the right to form a complete symmetric design.",
    ],
    
    "grid": [
        "Animate the grid-based symmetric expansion. Starting with the left half scatter, smoothly generate the mirrored pattern on the right, maintaining perfect symmetry along the central vertical line.",
        "Show the grid scatter pattern becoming symmetric. Begin with the random scatter on the left, then gradually extend it to the right to form a complete symmetric pattern.",
    ],
}


def get_prompt(task_type: str = "default") -> str:
    """
    Select a random prompt for the given task type.
    
    Args:
        task_type: Type of task (key in PROMPTS dict)
        
    Returns:
        Random prompt string from the specified type
    """
    prompts = PROMPTS.get(task_type, PROMPTS["default"])
    return random.choice(prompts)


def get_all_prompts(task_type: str = "default") -> list[str]:
    """Get all prompts for a given task type."""
    return PROMPTS.get(task_type, PROMPTS["default"])
