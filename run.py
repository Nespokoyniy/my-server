import sys
import os


def up():
    os.system("docker-compose -f docker-compose.dev.yml up")


def build_and_up():
    os.system(
        "docker-compose -f docker-compose.dev.yml build && docker-compose -f docker-compose.dev.yml up"
    )


def down():
    os.system("docker-compose -f docker-compose.dev.yml down")


def restart():
    os.system(
        "docker-compose -f docker-compose.dev.yml down && docker-compose -f docker-compose.dev.yml up"
    )


def help():
    print("Usage: python run.py [command]")
    print("Commands:")
    print("  up         - Start containers")
    print("  build-up   - Build and start containers")
    print("  down       - Stop containers")
    print("  restart    - Restart containers")
    print("  help       - Show this help")


def main():
    command = sys.argv[1]
    if command == "up":
        up()
    elif command == "build-up":
        build_and_up()
    elif command == "down":
        down()
    elif command == "restart":
        restart()
    else:
        print("Unknown command")
        help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Operation was being stopped")
