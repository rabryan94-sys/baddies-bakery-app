"""
Baddie's Bakery - Module Utils
"""

from utils.prompts import (
    BRAND_IDENTITY, 
    PROMPTS, 
    PLATFORM_GUIDELINES,
    CITATION_THEMES,
    EDUCATIONAL_TOPICS,
    VIDEO_TYPES
)

from utils.generator import (
    generate_post,
    generate_launch_post,
    generate_citation_post,
    generate_educational_post,
    generate_video_script
)

from utils.database import (
    save_post,
    get_all_posts,
    get_posts_by_type,
    get_posts_by_platform,
    get_post_by_id,
    delete_post,
    get_stats
)
