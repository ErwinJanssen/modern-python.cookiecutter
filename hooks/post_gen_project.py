import subprocess


def initialize_git():
    subprocess.run(
        ["git", "init"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )


if __name__ == "__main__":
    initialize_git()
