# Symmetry Random Data Generator 🎲

A generator for creating "random scatter symmetric expansion" animation tasks. Each task includes a start frame with a random scatter pattern and an end frame with the symmetric expansion, along with a 3-second crossfade animation.

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/your-org/your-task-generator.git
cd your-task-generator

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

# 4. Generate tasks
python examples/generate.py --num-samples 50
```

---

## 📁 Structure

```
template-data-generator/
├── core/                    # ✅ KEEP: Standard utilities
│   ├── base_generator.py   # Abstract base class
│   ├── schemas.py          # Pydantic models
│   ├── image_utils.py      # Image helpers
│   ├── video_utils.py      # Video generation
│   └── output_writer.py    # File output
├── src/                     # ⚠️ CUSTOMIZE: Your task logic
│   ├── generator.py        # Your task generator
│   ├── prompts.py          # Your prompt templates
│   └── config.py           # Your configuration
├── examples/
│   └── generate.py         # Entry point
└── data/questions/         # Generated output
```

---

## 📦 Output Format

Every generator produces:

```
data/questions/{domain}_task/{task_id}/
├── first_frame.png          # Initial state (REQUIRED)
├── final_frame.png          # Goal state (or goal.txt)
├── prompt.txt               # Instructions (REQUIRED)
└── ground_truth.mp4         # Solution video (OPTIONAL)
```

---

## 🎨 Customization (3 Files to Modify)

### 1. Update `src/generator.py`

The generator creates symmetric expansion tasks with random scatter patterns:

```python
from core import BaseGenerator, TaskPair, ImageRenderer
from core.video_utils import VideoGenerator

class TaskGenerator(BaseGenerator):
    def __init__(self, config):
        super().__init__(config)
        self.renderer = ImageRenderer(config.image_size)
        
        # Initialize video generator if enabled
        self.video_generator = None
        if config.generate_videos and VideoGenerator.is_available():
            self.video_generator = VideoGenerator(
                fps=config.video_fps, 
                output_format="mp4"
            )
    
    def generate_task_pair(self, task_id: str) -> TaskPair:
        # Generate random task parameters
        grid_size = random.randint(self.config.min_grid_size, self.config.max_grid_size)
        scatter_size = random.randint(self.config.min_scatter_size, self.config.max_scatter_size)
        color = random.choice(self.config.color_palette)
        
        # Generate initial scatter on left half
        initial_scatter = self._generate_initial_scatter(grid_size, scatter_size)
        
        # Generate symmetric scatter
        symmetric_scatter = self._generate_symmetric_scatter(initial_scatter, grid_size)
        
        # Render images
        first_image = self._render_scatter(initial_scatter, grid_size, color, show_grid=True)
        final_image = self._render_scatter(symmetric_scatter, grid_size, color, show_grid=True)
        
        # Generate video (optional)
        video_path = self._generate_video(first_image, final_image, task_id) if self.config.generate_videos else None
        
        return TaskPair(
            task_id=task_id,
            domain=self.config.domain,
            prompt=self.select_prompt(),
            first_image=first_image,
            final_image=final_image,
            ground_truth_video=video_path
        )
```

### 2. Update `src/prompts.py`

Define prompts for symmetric expansion tasks:

```python
import random

PROMPTS = {
    "default": [
        "Animate the symmetric expansion of the scatter pattern. Start with the initial scatter on the left, then smoothly reveal its mirror image on the right, creating a complete symmetric pattern along the vertical axis.",
        "Show the scatter pattern expanding symmetrically. Starting from the left half, gradually extend the pattern to the right half, creating a perfect mirror image along the central vertical axis.",
    ],
    "scatter": [
        "Show the random scatter expanding symmetrically. The initial scatter on the left should be mirrored to the right, creating a perfect symmetric pattern along the vertical axis.",
        "Animate the symmetric extension of the scatter. Start with the left side scatter, then gradually reveal its mirror image on the right to form a complete symmetric design.",
    ],
}

def get_prompt(task_type: str = "default") -> str:
    prompts = PROMPTS.get(task_type, PROMPTS["default"])
    return random.choice(prompts)
```

### 3. Update `src/config.py`

**All hyperparameters go here** - both general and task-specific:

```python
from core import GenerationConfig
from pydantic import Field

class TaskConfig(GenerationConfig):
    """Symmetry expansion task configuration."""
    # Inherits: num_samples, domain, seed, output_dir, image_size
    
    # Override defaults
    domain: str = Field(default="symmetry_random")
    image_size: tuple[int, int] = Field(default=(512, 512))
    
    # Video settings
    generate_videos: bool = Field(default=True, description="Whether to generate ground truth videos")
    video_fps: int = Field(default=30, description="Video frame rate")
    video_duration: float = Field(default=3.0, description="Duration of the video in seconds")
    
    # Task-specific settings
    min_grid_size: int = Field(default=8, description="Minimum grid size (number of squares per side)")
    max_grid_size: int = Field(default=12, description="Maximum grid size (number of squares per side)")
    
    min_scatter_size: int = Field(default=5, description="Minimum number of squares in initial scatter")
    max_scatter_size: int = Field(default=15, description="Maximum number of squares in initial scatter")
    
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
    hold_frames_ratio: float = Field(default=0.1, description="Ratio of video duration to hold at start and end")
    transition_frames_ratio: float = Field(default=0.8, description="Ratio of video duration for transition effect")
```

**Single entry point:** `python examples/generate.py --num-samples 50`