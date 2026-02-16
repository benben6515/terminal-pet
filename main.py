import yaml
import time
import sys
from blessed import Terminal
from pet import Pet


def load_config(config_path="config.yaml"):
    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Config file not found: {config_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing config file: {e}")
        return None


def main():
    config = load_config()
    if config is None:
        return

    term = Terminal()

    with term.hidden_cursor():
        sys.stdout.write("\x1b[2J\x1b[H")  # Clear screen and home
        print(
            term.center(term.bold + "Welcome to NYAN CAT Terminal Pet!" + term.normal)
        )
        print(term.center(term.dim + "Initializing..." + term.normal))

        pet = Pet(term, config)

        with term.cbreak():
            last_render_time = time.time()
            animation_speed = config["pet"]["animation_speed"]
            while True:
                key = term.inkey(timeout=0.016)

                if key:
                    action = pet.handle_input(key)

                    if action == "quit":
                        print("\x1b[2J\x1b[H")  # Clear screen
                        print(
                            term.center(
                                term.bold
                                + "Goodbye! Thanks for playing with Nyan! 😸"
                                + term.normal
                            )
                        )
                        print(
                            term.center(
                                term.dim + "Press any key to exit..." + term.normal
                            )
                        )
                        term.inkey()
                        break

                current_time = time.time()
                if current_time - last_render_time >= animation_speed:
                    pet.update()
                    last_render_time = current_time
                    pet.render()


if __name__ == "__main__":
    main()
