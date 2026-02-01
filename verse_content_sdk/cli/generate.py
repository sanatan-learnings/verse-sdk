#!/usr/bin/env python3
"""
Unified verse content generator - generates text, images, and audio for a specific verse.

This command orchestrates the generation of all content types for a verse:
1. Text content (verse frontmatter and fields) using GPT-4
2. Image using DALL-E 3
3. Audio pronunciation using ElevenLabs

Usage:
    # Generate everything for Chapter 2, Verse 47
    verse-generate --chapter 2 --verse 47 --all

    # Generate only image and audio
    verse-generate --chapter 2 --verse 47 --image --audio

    # Generate only text
    verse-generate --chapter 2 --verse 47 --text

    # For texts without chapters (like Hanuman Chalisa)
    verse-generate --verse 15 --all

Requirements:
    - OPENAI_API_KEY environment variable
    - ELEVENLABS_API_KEY environment variable (for audio)
"""

import os
import sys
import argparse
import subprocess
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


def generate_image(chapter: Optional[int], verse: int, theme: str) -> bool:
    """Generate image for the specified verse."""
    print(f"\n{'='*60}")
    print("STEP 1: GENERATING IMAGE")
    print(f"{'='*60}\n")

    # First, ensure the scene description exists in docs/image-prompts.md
    prompts_file = Path.cwd() / "docs" / "image-prompts.md"

    if not prompts_file.exists():
        print(f"Error: {prompts_file} not found")
        print("Please create scene descriptions in docs/image-prompts.md first")
        return False

    # Read prompts file to check if verse exists
    with open(prompts_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if chapter:
        search_pattern = f"### Chapter {chapter}, Verse {verse}"
    else:
        search_pattern = f"### Verse {verse}"

    if search_pattern not in content:
        print(f"Error: Scene description for {search_pattern} not found in {prompts_file}")
        print(f"\nPlease add a scene description like:")
        print(f"\n{search_pattern}")
        print("**Scene Description**:")
        print("[Describe the visual scene here...]")
        return False

    print(f"✓ Found scene description for {search_pattern}")

    # Construct the filename to regenerate
    if chapter:
        filename = f"chapter-{chapter:02d}-verse-{verse:02d}.png"
    else:
        filename = f"verse-{verse:02d}.png"

    print(f"✓ Will generate: {filename}")
    print(f"✓ Theme: {theme}")

    # Run verse-images command with --regenerate flag
    cmd = [
        "verse-images",
        "--theme-name", theme,
        "--regenerate", filename
    ]

    print(f"\nRunning: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✓ Image generated successfully: images/{theme}/{filename}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error generating image: {e}")
        return False


def generate_audio(chapter: Optional[int], verse: int) -> bool:
    """Generate audio for the specified verse."""
    print(f"\n{'='*60}")
    print("STEP 2: GENERATING AUDIO")
    print(f"{'='*60}\n")

    # Check if verse file exists
    verses_dir = Path.cwd() / "_verses"

    if chapter:
        verse_file = verses_dir / f"chapter_{chapter:02d}_verse_{verse:02d}.md"
    else:
        verse_file = verses_dir / f"verse_{verse:02d}.md"

    if not verse_file.exists():
        print(f"Error: Verse file not found: {verse_file}")
        print("Please create the verse markdown file first")
        return False

    print(f"✓ Found verse file: {verse_file}")

    # Construct the audio filenames to regenerate
    if chapter:
        base_name = f"chapter_{chapter:02d}_verse_{verse:02d}"
    else:
        base_name = f"verse_{verse:02d}"

    filenames = f"{base_name}_full.mp3,{base_name}_slow.mp3"

    print(f"✓ Will generate: {base_name}_full.mp3 and {base_name}_slow.mp3")

    # Run verse-audio command with --regenerate flag
    cmd = [
        "verse-audio",
        "--regenerate", filenames
    ]

    print(f"\nRunning: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✓ Audio generated successfully:")
        print(f"  - audio/{base_name}_full.mp3")
        print(f"  - audio/{base_name}_slow.mp3")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error generating audio: {e}")
        return False


def generate_text(chapter: Optional[int], verse: int) -> bool:
    """Generate text content for the specified verse using GPT-4."""
    print(f"\n{'='*60}")
    print("STEP 1: GENERATING TEXT CONTENT")
    print(f"{'='*60}\n")

    print("Text generation not yet implemented.")
    print("This feature will use GPT-4 to generate:")
    print("  - Sanskrit/Devanagari text")
    print("  - Transliteration")
    print("  - Word meanings")
    print("  - Literal translation")
    print("  - Interpretive meaning")
    print("  - Story/context")
    print("  - Practical application")
    print("\nFor now, please create the verse file manually in _verses/")

    return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate text, images, and audio for a specific verse",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate everything for Chapter 2, Verse 47
  verse-generate --chapter 2 --verse 47 --all

  # Generate only image and audio
  verse-generate --chapter 2 --verse 47 --image --audio

  # Generate for texts without chapters (Hanuman Chalisa)
  verse-generate --verse 15 --all --theme modern-minimalist

Environment Variables:
  OPENAI_API_KEY      - Required for image generation
  ELEVENLABS_API_KEY  - Required for audio generation
        """
    )

    # Verse identification
    parser.add_argument(
        "--chapter",
        type=int,
        help="Chapter number (optional for texts like Hanuman Chalisa)",
        metavar="N"
    )
    parser.add_argument(
        "--verse",
        type=int,
        required=True,
        help="Verse number (required)",
        metavar="N"
    )

    # Content types
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate text, image, and audio"
    )
    parser.add_argument(
        "--text",
        action="store_true",
        help="Generate text content"
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

    # Options
    parser.add_argument(
        "--theme",
        default="modern-minimalist",
        help="Theme name for image generation (default: modern-minimalist)",
        metavar="NAME"
    )

    args = parser.parse_args()

    # Validate options
    if not any([args.all, args.text, args.image, args.audio]):
        parser.error("Please specify at least one of: --all, --text, --image, --audio")

    # Determine what to generate
    generate_text_flag = args.all or args.text
    generate_image_flag = args.all or args.image
    generate_audio_flag = args.all or args.audio

    # Display header
    print("\n" + "="*60)
    print("VERSE CONTENT GENERATOR")
    print("="*60)

    if args.chapter:
        print(f"\nVerse: Chapter {args.chapter}, Verse {args.verse}")
    else:
        print(f"\nVerse: Verse {args.verse}")

    print(f"Theme: {args.theme}")
    print("\nGenerating:")
    if generate_text_flag:
        print("  ✓ Text content")
    if generate_image_flag:
        print("  ✓ Image")
    if generate_audio_flag:
        print("  ✓ Audio")
    print()

    # Check API keys
    if generate_image_flag:
        if not os.getenv("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY not set (required for image generation)")
            print("Set it in .env file or environment")
            sys.exit(1)

    if generate_audio_flag:
        if not os.getenv("ELEVENLABS_API_KEY"):
            print("Error: ELEVENLABS_API_KEY not set (required for audio generation)")
            print("Set it in .env file or environment")
            sys.exit(1)

    # Track success
    results = {
        'text': None,
        'image': None,
        'audio': None
    }

    # Generate content
    try:
        if generate_text_flag:
            results['text'] = generate_text(args.chapter, args.verse)

        if generate_image_flag:
            results['image'] = generate_image(args.chapter, args.verse, args.theme)

        if generate_audio_flag:
            results['audio'] = generate_audio(args.chapter, args.verse)

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

    if generate_text_flag:
        status = "✓" if results['text'] else "✗"
        print(f"{status} Text: {'Success' if results['text'] else 'Failed'}")

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
