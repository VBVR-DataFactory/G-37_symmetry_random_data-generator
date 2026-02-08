"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           YOUR TASK CONFIGURATION                             ║
║                                                                               ║
║  CUSTOMIZE THIS FILE to define your task-specific settings.                   ║
║  Inherits common settings from core.GenerationConfig                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from pydantic import Field
from core import GenerationConfig


class TaskConfig(GenerationConfig):
    """
    Your task-specific configuration for symmetry expansion.
    
    CUSTOMIZE THIS CLASS to add your task's hyperparameters.
    
    Inherited from GenerationConfig:
        - num_samples: int          # Number of samples to generate
        - domain: str               # Task domain name
        - difficulty: Optional[str] # Difficulty level
        - random_seed: Optional[int] # For reproducibility
        - output_dir: Path          # Where to save outputs
        - image_size: tuple[int, int] # Image dimensions
    """
    
    # ══════════════════════════════════════════════════════════════════════════
    #  OVERRIDE DEFAULTS
    # ══════════════════════════════════════════════════════════════════════════
    
    domain: str = Field(default="symmetry_random")
    image_size: tuple[int, int] = Field(default=(1024, 1024))
    
    # ══════════════════════════════════════════════════════════════════════════
    #  VIDEO SETTINGS
    # ══════════════════════════════════════════════════════════════════════════
    
    generate_videos: bool = Field(
        default=True,
        description="Whether to generate ground truth videos"
    )
    
    video_fps: int = Field(
        default=16,  # Higher FPS for smoother animation
        description="Video frame rate"
    )
    
    video_duration: float = Field(
        default=3.0,  # 3 seconds as required
        description="Duration of the video in seconds"
    )
    
    # ══════════════════════════════════════════════════════════════════════════
    #  TASK-SPECIFIC SETTINGS
    # ══════════════════════════════════════════════════════════════════════════
    
    # Canvas grid size range (8×8 to 12×12)
    min_grid_size: int = Field(
        default=8,
        description="Minimum grid size (number of squares per side)"
    )
    
    max_grid_size: int = Field(
        default=12,
        description="Maximum grid size (number of squares per side)"
    )
    
    # Initial scatter size range (5-15 grid squares)
    min_scatter_size: int = Field(
        default=5,
        description="Minimum number of squares in initial scatter"
    )
    
    max_scatter_size: int = Field(
        default=15,
        description="Maximum number of squares in initial scatter"
    )
    
    # Color palette for scatter elements
    color_palette: list[str] = Field(
        default=[
            "#FF0000",  # Red
            "#FFA500",  # Orange
            "#0000FF",  # Blue
            "#800080",  # Purple
            "#00FF00",  # Green
            "#FF00FF",  # Magenta
            "#00FFFF",  # Cyan
        ],
        description="List of colors to use for scatter elements"
    )
    
    # Animation settings
    hold_frames_ratio: float = Field(
        default=0.1,  # 10% of frames at start/end
        description="Ratio of video duration to hold at start and end"
    )
    
    transition_frames_ratio: float = Field(
        default=0.8,  # 80% of frames for transition
        description="Ratio of video duration for transition effect"
    )
