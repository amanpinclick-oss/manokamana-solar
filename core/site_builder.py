import os
import shutil
import datetime

class SiteBuilder:
    """
    Utility to manage static site builds and directory structures for Manokamana Solar.
    """

    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.content_dir = os.path.join(base_dir, "content")
        self.blog_dir = os.path.join(self.content_dir, "blogs")
        self.public_dir = os.path.join(base_dir, "public")
        
        self._ensure_dirs()

    def _ensure_dirs(self):
        """Create necessary project directories if they don't exist."""
        for d in [self.content_dir, self.blog_dir, self.public_dir]:
            if not os.path.exists(d):
                os.makedirs(d)
                print(f"[SiteBuilder] Created directory: {d}")

    def rebuild_site(self):
        """
        Simulates a static site rebuild process.
        In a real scenario, this would trigger Vite, Next.js, or Hugo.
        """
        print(f"[SiteBuilder] Rebuilding static site at {datetime.datetime.now()}...")
        # Simulate build by syncing content to public (toy example)
        # In real world: `npm run build`
        return {"status": "success", "timestamp": datetime.datetime.now().isoformat()}

    def get_blog_path(self, slug: str) -> str:
        return os.path.join(self.blog_dir, f"{slug}.md")
