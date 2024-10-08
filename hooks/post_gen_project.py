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


def first_commit():
    subprocess.run(
        ["git", "add", "."], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    proc = subprocess.run(
        ["git", "commit", "--message", "Initialized project"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(proc.stderr)
    proc.check_returncode()
    subprocess.run(
        ["git", "tag", "--annotate", "--message", "Initialized project", "v0.0.0"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


if __name__ == "__main__":
    initialize_git()
    initialize_pre_commit()
    first_commit()
