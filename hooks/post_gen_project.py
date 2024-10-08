import subprocess


def initialize_git():
    subprocess.run(
        ["git", "init"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )


def initialize_pre_commit():
    subprocess.run(
        ["pre-commit", "install"],
        # This is allowed to fail, in case pre-commit is not installed.
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


if __name__ == "__main__":
    initialize_git()
    initialize_pre_commit()
