"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           YOUR TASK GENERATOR                                 ║
║                                                                               ║
║  CUSTOMIZE THIS FILE to implement your data generation logic.                 ║
║  Replace the example implementation with your own task.                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw
from typing import List, Tuple, Set

from core import BaseGenerator, TaskPair, ImageRenderer
from core.video_utils import VideoGenerator
from .config import TaskConfig
from .prompts import get_prompt


class TaskGenerator(BaseGenerator):
    """
    Symmetry Expansion Task Generator.
    
    This generator creates tasks where a random scatter pattern on the left half of a grid
    is symmetrically expanded to the right half, creating a complete symmetric pattern.
    
    Required:
        - generate_task_pair(task_id) -> TaskPair
    """
    
    def __init__(self, config: TaskConfig):
        super().__init__(config)
        self.renderer = ImageRenderer(image_size=config.image_size)
        
        # Initialize video generator if enabled
        self.video_generator = None
        if config.generate_videos and VideoGenerator.is_available():
            self.video_generator = VideoGenerator(
                fps=config.video_fps, 
                output_format="mp4"
            )
    
    def generate_task_pair(self, task_id: str) -> TaskPair:
        """Generate one symmetry expansion task pair."""
        
        # Generate random task parameters
        grid_size = random.randint(
            self.config.min_grid_size, 
            self.config.max_grid_size
        )
        scatter_size = random.randint(
            self.config.min_scatter_size, 
            self.config.max_scatter_size
        )
        # Generate random RGB color (avoid too dark or too light colors for visibility)
        # R, G, B each in range [50, 255] to ensure good visibility
        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        
        # Generate initial scatter pattern on left half
        initial_scatter = self._generate_initial_scatter(grid_size, scatter_size)
        
        # Generate symmetric scatter pattern
        symmetric_scatter = self._generate_symmetric_scatter(initial_scatter, grid_size)
        
        # Render images
        first_image = self._render_scatter(initial_scatter, grid_size, color, show_grid=True)
        final_image = self._render_scatter(symmetric_scatter, grid_size, color, show_grid=True)
        
        # Generate video (optional)
        video_path = None
        if self.config.generate_videos and self.video_generator:
            video_path = self._generate_video(first_image, final_image, task_id)
        
        # Select prompt
        prompt = get_prompt("scatter")
        
        # Build task_data dict from parameters
        # Only include task-specific parameters (removed signature, derivable symmetric_scatter)
        task_data = {
            "color": color,
            "grid_size": grid_size,
            "scatter_size": scatter_size,
            "initial_scatter": sorted(list(initial_scatter)),  # Convert set to sorted list for consistency
        }

        metadata = self._build_metadata(task_id, task_data)
        
        
        
        return TaskPair(
            task_id=task_id,
            domain=self.config.domain,
            prompt=prompt,
            first_image=first_image,
            final_image=final_image,
            ground_truth_video=video_path,
            metadata=metadata
        )
    
    # ══════════════════════════════════════════════════════════════════════════
    #  TASK-SPECIFIC METHODS
    # ══════════════════════════════════════════════════════════════════════════
    
    def _generate_initial_scatter(self, grid_size: int, scatter_size: int) -> Set[Tuple[int, int]]:
        """
        Generate a random scatter pattern on the left half of the grid.
        
        Args:
            grid_size: Size of the grid (number of squares per side)
            scatter_size: Number of squares in the scatter pattern
            
        Returns:
            Set of (row, column) coordinates representing the scatter pattern
        """
        scatter = set()
        
        # Calculate the vertical axis (middle of the grid)
        vertical_axis = grid_size // 2
        
        # Generate random scatter on the left half (columns < vertical_axis)
        while len(scatter) < scatter_size:
            row = random.randint(0, grid_size - 1)
            col = random.randint(0, vertical_axis - 1)
            scatter.add((row, col))
        
        return scatter
    
    def _generate_symmetric_scatter(self, initial_scatter: Set[Tuple[int, int]], grid_size: int) -> Set[Tuple[int, int]]:
        """
        Generate a symmetric scatter pattern by mirroring the initial scatter across the vertical axis.
        
        Args:
            initial_scatter: Set of (row, column) coordinates for the initial scatter
            grid_size: Size of the grid (number of squares per side)
            
        Returns:
            Set of (row, column) coordinates representing the symmetric scatter pattern
        """
        symmetric_scatter = set(initial_scatter)  # Start with initial scatter
        
        # Calculate the vertical axis (middle of the grid)
        vertical_axis = grid_size // 2
        
        # Mirror each point across the vertical axis
        for (row, col) in initial_scatter:
            # Calculate the mirrored column
            mirrored_col = (vertical_axis * 2) - 1 - col if grid_size % 2 == 0 else (vertical_axis * 2) - col
            symmetric_scatter.add((row, mirrored_col))
        
        return symmetric_scatter
    
    def _render_scatter(self, scatter: Set[Tuple[int, int]], grid_size: int, color: Tuple[int, int, int], show_grid: bool = False) -> Image.Image:
        """
        Render the scatter pattern on a grid canvas.
        
        Args:
            scatter: Set of (row, column) coordinates for the scatter pattern
            grid_size: Size of the grid (number of squares per side)
            color: Color for the scatter squares (RGB tuple)
            show_grid: Whether to show the grid lines
            
        Returns:
            PIL Image representing the rendered scatter pattern
        """
        # Create blank image
        image = self.renderer.create_blank_image(bg_color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # Calculate square size and ensure alignment with grid
        width, height = image.size
        square_w = width // grid_size
        square_h = height // grid_size
        
        # Draw the grid if requested
        if show_grid:
            image = self.renderer.draw_grid(image, grid_size, grid_size)
        
        # Draw scatter squares
        for (row, col) in scatter:
            # Calculate precise square positions to ensure alignment with grid
            x0 = int((col / grid_size) * width)
            y0 = int((row / grid_size) * height)
            x1 = int(((col + 1) / grid_size) * width)
            y1 = int(((row + 1) / grid_size) * height)
            draw.rectangle([x0, y0, x1, y1], fill=color)
        
        # Draw vertical symmetry axis (dashed line)
        axis_x = width // 2
        dash_length = square_w // 4
        gap_length = square_w // 4
        y = 0
        while y < height:
            draw.line([(axis_x, y), (axis_x, min(y + dash_length, height))], 
                     fill=(100, 100, 100), width=2)
            y += dash_length + gap_length
        
        return image
    
    def _generate_video(
        self,
        first_image: Image.Image,
        final_image: Image.Image,
        task_id: str
    ) -> str:
        """
        Generate a 3-second ground truth video with smooth cross-fade transition.
        
        Args:
            first_image: Initial state image
            final_image: Final state image
            task_id: Unique task identifier
            
        Returns:
            Path to the generated video file
        """
        temp_dir = Path(tempfile.gettempdir()) / f"{self.config.domain}_videos"
        temp_dir.mkdir(parents=True, exist_ok=True)
        video_path = temp_dir / f"{task_id}_ground_truth.mp4"
        
        # Calculate total frames and transition frames
        total_frames = int(self.config.video_duration * self.config.video_fps)
        hold_frames = int(total_frames * self.config.hold_frames_ratio)
        transition_frames = total_frames - 2 * hold_frames
        
        # Create video with smooth cross-fade
        result = self.video_generator.create_crossfade_video(
            start_image=first_image,
            end_image=final_image,
            output_path=video_path,
            hold_frames=hold_frames,
            transition_frames=transition_frames
        )
        
        return str(result) if result else None
