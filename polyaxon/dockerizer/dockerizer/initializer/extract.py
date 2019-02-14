import os
import shutil


def extract_code(extract_path: str, build_path: str, context_path: str) -> bool:
    try:
        # We copy all files under the context to the build path
        extract_context_path = os.path.join(extract_path, context_path)
        shutil.copytree(extract_context_path, build_path)
        return True
    except Exception:
        return False


def extract_dockerfile(extract_path: str, dockerfile_path: str, build_context: str) -> bool:
    try:
        # We move all files under the context to the build path
        context_dockerfile_path = os.path.join(extract_path, dockerfile_path)
        build_dockerfile_path = os.path.join(build_context, dockerfile_path)
        shutil.copy(context_dockerfile_path, build_dockerfile_path)
        return True
    except Exception:
        return False
