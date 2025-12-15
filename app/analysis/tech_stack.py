def detect_tech_stack(files):
    stack = set()

    for f in files:
        name = f.get("name", "").lower()

        if name.endswith(".py"):
            stack.add("python")

        if name in {"requirements.txt", "pyproject.toml", "setup.py"}:
            stack.add("python-deps")

        if name == "dockerfile":
            stack.add("docker")

        if name.endswith(".js"):
            stack.add("javascript")

        if name.endswith(".ts"):
            stack.add("typescript")

        if name in {"package.json", "pnpm-lock.yaml", "yarn.lock"}:
            stack.add("nodejs")

    return sorted(stack)
