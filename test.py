#!/usr/bin/env python3

import time
import yaml
from blessed import Terminal
from graphics import Graphics
from animation import Animation
from stats import Stats
from interaction import Interaction


def test_imports():
    """Test that all modules can be imported correctly"""
    print("✓ Testing imports...")

    from blessed import Terminal
    from graphics import Graphics
    from animation import Animation
    from stats import Stats
    from interaction import Interaction
    from pet import Pet

    print("✓ All imports successful!")
    return True


def test_config():
    """Test config loading"""
    print("\n✓ Testing config loading...")

    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        print(f"✓ Config loaded: Pet name = {config['pet']['name']}")
        return config
    except Exception as e:
        print(f"✗ Config loading failed: {e}")
        return None


def test_graphics(term, config):
    """Test graphics module"""
    print("\n✓ Testing graphics module...")

    graphics = Graphics(term, config)
    print(f"✓ Graphics initialized with {len(graphics.cat_frames)} cat frames")
    print(f"✓ Rainbow colors: {graphics.colors['rainbow_gradient']}")

    return graphics


def test_stats(config):
    """Test stats module"""
    print("\n✓ Testing stats module...")

    stats = Stats(config)
    stats_data = stats.get_stats()
    print(
        f"✓ Initial stats: Hunger={stats_data['hunger']}, Mood={stats_data['mood']}, Energy={stats_data['energy']}"
    )

    stats.feed(20)
    print(f"✓ After feeding: Hunger={stats.get_stats()['hunger']}")

    return stats


def test_animation(term, config):
    """Test animation module"""
    print("\n✓ Testing animation module...")

    animation = Animation(term, config)
    print(f"✓ Animation initialized at position {animation.get_position()}")

    return animation


def test_interaction(term, config):
    """Test interaction module"""
    print("\n✓ Testing interaction module...")

    interaction = Interaction(term, config)
    print(f"✓ Interaction initialized")
    print(f"✓ Controls: {interaction.get_controls()}")

    return interaction


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("NYAN CAT TERMINAL PET - TEST SUITE")
    print("=" * 50)

    try:
        config = test_config()
        if not config:
            return False

        test_imports()

        term = Terminal()

        graphics = test_graphics(term, config)
        stats = test_stats(config)
        animation = test_animation(term, config)
        interaction = test_interaction(term, config)

        print("\n" + "=" * 50)
        print("✓ ALL TESTS PASSED!")
        print("=" * 50)
        print("\nYou can now run: python main.py")
        print("Press 'h' for help once the pet is running!")

        return True

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
