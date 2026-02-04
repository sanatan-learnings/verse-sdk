#!/usr/bin/env python3
"""
Collection-aware verse content generator - orchestrates image and audio generation for verses.

This command simplifies the generation of media for a specific verse by calling
verse-images and verse-audio with the correct collection-aware parameters.

Usage:
    # Generate image and audio for Hanuman Chalisa verse 15
    verse-generate --collection hanuman-chalisa --verse 15 --all --theme modern-minimalist

    # Generate only image
    verse-generate --collection sundar-kaand --verse 3 --image --theme modern-minimalist

    # Generate only audio
    verse-generate --collection sankat-mochan-hanumanashtak --verse 5 --audio

Requirements:
    - OPENAI_API_KEY environment variable (for image generation)
    - ELEVENLABS_API_KEY environment variable (for audio generation)
"""

import os
import sys
import argparse
import subprocess
import yaml
import shutil
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv package not installed")
    print("Install with: pip install python-dotenv")
    sys.exit(1)

# Load environment variables
load_dotenv()


def find_command(command_name: str) -> str:
    """Find the full path to a command, checking common locations."""
    # First try shutil.which (checks PATH)
    cmd_path = shutil.which(command_name)
    if cmd_path:
        return cmd_path

    # Check common installation locations
    common_paths = [
        Path.home() / "Library" / "Python" / "3.13" / "bin" / command_name,
        Path.home() / "Library" / "Python" / "3.12" / "bin" / command_name,
        Path.home() / "Library" / "Python" / "3.11" / "bin" / command_name,
        Path.home() / ".local" / "bin" / command_name,
        Path("/usr/local/bin") / command_name,
    ]

    for path in common_paths:
        if path.exists():
            return str(path)

    # If not found, return command name and hope it's in PATH
    return command_name


def validate_collection(collection: str, project_dir: Path = Path.cwd()) -> bool:
    """Validate that collection exists and is enabled."""
    # Check _verses directory
    verses_dir = project_dir / "_verses" / collection
    if not verses_dir.exists():
        print(f"✗ Error: Collection directory not found: {verses_dir}")
        return False

    # Check collections.yml
    collections_file = project_dir / "_data" / "collections.yml"
    if collections_file.exists():
        with open(collections_file) as f:
            data = yaml.safe_load(f)
            if collection not in data:
                print(f"✗ Error: Collection '{collection}' not found in collections.yml")
                return False
            if not data[collection].get('enabled', False):
                print(f"✗ Error: Collection '{collection}' is disabled in collections.yml")
                return False

    return True


def list_collections(project_dir: Path = Path.cwd()):
    """List available collections from _data/collections.yml"""
    collections_file = project_dir / "_data" / "collections.yml"
    if not collections_file.exists():
        print("No collections.yml found")
        return []

    with open(collections_file) as f:
        data = yaml.safe_load(f)
        enabled = [
            (key, info.get('name', {}).get('en', key))
            for key, info in data.items()
            if info.get('enabled', False)
        ]

    print("\nAvailable collections:")
    for key, name in enabled:
        verses_dir = project_dir / "_verses" / key
        count = len(list(verses_dir.glob("*.md"))) if verses_dir.exists() else 0
        print(f"  ✓ {key:30s} - {name} ({count} verses)")

    return enabled


def generate_image(collection: str, verse: int, theme: str) -> bool:
    """Generate image for the specified verse."""
    print(f"\n{'='*60}")
    print("GENERATING IMAGE")
    print(f"{'='*60}\n")

    # Check if prompts file exists
    prompts_file = Path.cwd() / "docs" / "image-prompts" / f"{collection}.md"
    if not prompts_file.exists():
        print(f"✗ Error: Prompts file not found: {prompts_file}")
        print(f"Please create scene descriptions in {prompts_file} first")
        return False

    # Construct the verse identifier
    verse_id = f"verse_{verse:02d}"

    print(f"✓ Collection: {collection}")
    print(f"✓ Verse: {verse_id}")
    print(f"✓ Theme: {theme}")

    # Run verse-images command
    verse_images_cmd = find_command("verse-images")
    cmd = [
        verse_images_cmd,
        "--collection", collection,
        "--theme", theme,
        "--verse", verse_id
    ]

    print(f"\nRunning: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✓ Image generated successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error generating image: {e}")
        return False


def generate_audio(collection: str, verse: int) -> bool:
    """Generate audio for the specified verse."""
    print(f"\n{'='*60}")
    print("GENERATING AUDIO")
    print(f"{'='*60}\n")

    # Check if verse file exists
    verses_dir = Path.cwd() / "_verses" / collection
    verse_id = f"verse_{verse:02d}"
    verse_file = verses_dir / f"{verse_id}.md"

    if not verse_file.exists():
        print(f"✗ Error: Verse file not found: {verse_file}")
        print("Please create the verse markdown file first")
        return False

    print(f"✓ Collection: {collection}")
    print(f"✓ Verse: {verse_id}")

    # Run verse-audio command
    verse_audio_cmd = find_command("verse-audio")
    cmd = [
        verse_audio_cmd,
        "--collection", collection,
        "--verse", verse_id
    ]

    print(f"\nRunning: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✓ Audio generated successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error generating audio: {e}")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate images and audio for a specific verse",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate both image and audio
  verse-generate --collection hanuman-chalisa --verse 15 --all --theme modern-minimalist

  # Generate only image
  verse-generate --collection sundar-kaand --verse 3 --image --theme modern-minimalist

  # Generate only audio
  verse-generate --collection sankat-mochan-hanumanashtak --verse 5 --audio

  # List available collections
  verse-generate --list-collections

Environment Variables:
  OPENAI_API_KEY      - Required for image generation
  ELEVENLABS_API_KEY  - Required for audio generation
        """
    )

    # List collections
    parser.add_argument(
        "--list-collections",
        action="store_true",
        help="List available collections and exit"
    )

    # Collection and verse identification
    parser.add_argument(
        "--collection",
        type=str,
        help="Collection key (e.g., hanuman-chalisa, sundar-kaand)",
        metavar="KEY"
    )
    parser.add_argument(
        "--verse",
        type=int,
        help="Verse number (required unless --list-collections)",
        metavar="N"
    )

    # Content types
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate both image and audio"
    )
    parser.add_argument(
        "--image",
        action="store_true",
        help="Generate image"
    )
    parser.add_argument(
        "--audio",
        action="store_true",
        help="Generate audio pronunciation"
    )

    # Theme for image generation
    parser.add_argument(
        "--theme",
        default="modern-minimalist",
        help="Theme name for image generation (default: modern-minimalist)",
        metavar="NAME"
    )

    args = parser.parse_args()

    # Handle list collections
    if args.list_collections:
        list_collections()
        sys.exit(0)

    # Validate required arguments
    if not args.collection:
        parser.error("--collection is required")
    if not args.verse:
        parser.error("--verse is required")

    # Validate options
    if not any([args.all, args.image, args.audio]):
        parser.error("Please specify at least one of: --all, --image, --audio")

    # Validate collection
    if not validate_collection(args.collection):
        sys.exit(1)

    # Determine what to generate
    generate_image_flag = args.all or args.image
    generate_audio_flag = args.all or args.audio

    # Display header
    print("\n" + "="*60)
    print("VERSE CONTENT GENERATOR")
    print("="*60)

    print(f"\nCollection: {args.collection}")
    print(f"Verse: {args.verse}")
    if generate_image_flag:
        print(f"Theme: {args.theme}")

    print("\nGenerating:")
    if generate_image_flag:
        print("  ✓ Image")
    if generate_audio_flag:
        print("  ✓ Audio")
    print()

    # Check API keys
    if generate_image_flag:
        if not os.getenv("OPENAI_API_KEY"):
            print("✗ Error: OPENAI_API_KEY not set (required for image generation)")
            print("Set it in .env file or environment")
            sys.exit(1)

    if generate_audio_flag:
        if not os.getenv("ELEVENLABS_API_KEY"):
            print("✗ Error: ELEVENLABS_API_KEY not set (required for audio generation)")
            print("Set it in .env file or environment")
            sys.exit(1)

    # Track success
    results = {
        'image': None,
        'audio': None
    }

    # Generate content (image first, then audio)
    try:
        if generate_image_flag:
            results['image'] = generate_image(args.collection, args.verse, args.theme)

        if generate_audio_flag:
            results['audio'] = generate_audio(args.collection, args.verse)

    except KeyboardInterrupt:
        print("\n\n⚠ Generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Summary
    print(f"\n{'='*60}")
    print("GENERATION SUMMARY")
    print(f"{'='*60}\n")

    if generate_image_flag:
        status = "✓" if results['image'] else "✗"
        print(f"{status} Image: {'Success' if results['image'] else 'Failed'}")

    if generate_audio_flag:
        status = "✓" if results['audio'] else "✗"
        print(f"{status} Audio: {'Success' if results['audio'] else 'Failed'}")

    print()

    # Exit with appropriate code
    all_results = [r for r in results.values() if r is not None]
    if all_results and all(all_results):
        print("✓ All tasks completed successfully!")
        sys.exit(0)
    elif any(all_results):
        print("⚠ Some tasks completed with errors")
        sys.exit(1)
    else:
        print("✗ All tasks failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
