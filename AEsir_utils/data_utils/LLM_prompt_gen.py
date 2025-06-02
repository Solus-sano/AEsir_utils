import os
from .data_visual import tree_to_string
from pathlib import Path

OVERVIEW_PROMPT = """
====================================== Project Directory Structure (Source Files) ======================================
{proj_dir_tree}
===================================================================================================================
"""

FILE_PROMPT = """
============================================ the content of the file ({file}) ==============================================
{file_content}
===================================================================================================================
"""

def generate_proj_prompt(
    proj_dir: str
) -> str:
    """
    Generate a prompt for a project directory.

    Args:
        proj_dir (str): The path to the project directory.

    Returns:
        str: The generated prompt.
    """
    dir_pefix = proj_dir
    if not dir_pefix.endswith("/"):
        dir_pefix += "/"
    prompt_1 = OVERVIEW_PROMPT.format(proj_dir_tree=tree_to_string(proj_dir))
    
    file_path_lst = []
    for root, dirs, files in os.walk(proj_dir):
        if "/." in root:
            continue
        for file in files:
            if file.startswith('.'):
                continue
            if ".pyc" in file:
                continue
            file_path = os.path.join(root, file)
            file_path_lst.append(file_path)
            
    file_content_lst = []
    for file_path in file_path_lst:
        with open(file_path, 'r') as f:
            file_content = f.read()
            file_content_lst.append(
                FILE_PROMPT.format(
                    file=file_path.replace(dir_pefix, ""),
                    file_content=file_content
                )
            )
            
    prompt_2 = "\n".join(file_content_lst)
    return prompt_1 + "\n" + prompt_2

def generate_proj_prompt_2(
    proj_dir: str,
    include_extensions: list = None, # e.g., [".py", ".txt", ".md"]
    exclude_extensions: list = None, # e.g., [".pyc", ".log"]
    exclude_dirs: list = None,       # e.g., [".git", "node_modules", "__pycache__"]
    exclude_files: list = None,      # e.g., [".DS_Store"]
    max_file_size_kb: int = 1024     # Max file size in KB to include (1MB default)
) -> str:
    """
    Generates a prompt describing a project directory, its structure, and file contents.

    Args:
        proj_dir (str): The path to the project directory.
        include_extensions (list, optional): List of file extensions to explicitly include.
                                            If None, all non-excluded files are considered.
        exclude_extensions (list, optional): List of file extensions to exclude.
                                            Defaults to [".pyc"].
        exclude_dirs (list, optional): List of directory names to exclude.
                                       Defaults to common ones like [".git", "__pycache__", "node_modules"].
                                       Hidden directories (starting with '.') are always excluded.
        exclude_files (list, optional): List of specific file names to exclude.
                                        Defaults to [".DS_Store"].
                                        Hidden files (starting with '.') are always excluded by default,
                                        unless `include_extensions` overrides this for a specific extension.
        max_file_size_kb (int, optional): Maximum file size in kilobytes to include.
                                          Files larger than this will be skipped. Defaults to 1024KB (1MB).

    Returns:
        str: The generated prompt.
    """
    project_path = Path(proj_dir).resolve() # Use pathlib and resolve to an absolute path

    if not project_path.is_dir():
        return "Error: Provided path is not a directory or does not exist."

    # --- Set defaults for exclusions ---
    if exclude_extensions is None:
        exclude_extensions = [".pyc"]
    if exclude_dirs is None:
        exclude_dirs = [".git", "__pycache__", "node_modules", "venv", ".venv"] # Common ones
    if exclude_files is None:
        exclude_files = [".DS_Store"]

    # --- Generate directory tree ---
    # (Assuming your tree_to_string handles exclusions or you adapt the example)
    dir_tree_str = tree_to_string(project_path, ignore_dirs=[d for d in exclude_dirs if not d.startswith('.')]) # Pass non-hidden exclude_dirs
    overview_prompt = OVERVIEW_PROMPT.format(proj_dir_tree=dir_tree_str)

    # --- Collect and filter file paths ---
    file_prompts = []
    for item in project_path.rglob("*"): # rglob searches recursively
        if item.is_file():
            # 1. Check against excluded directories
            if any(excluded_dir in item.parts for excluded_dir in exclude_dirs):
                continue
            # 2. Check for hidden directories in the path (more robustly)
            if any(part.startswith('.') and part not in ('.', '..') for part in item.parent.parts if part != project_path.name):
                 # Exclude if any parent directory (other than project root itself if hidden) is hidden
                if not (item.parent == project_path and project_path.name.startswith('.')): # Allow files in hidden project root if not otherwise excluded
                    continue


            # 3. Check for hidden files
            if item.name.startswith('.') and item.name not in (include_extensions or []): # Allow explicitly included hidden files
                 if item.name not in (exclude_files or []): # Unless also in exclude_files
                    continue


            # 4. Check against excluded files
            if item.name in exclude_files:
                continue

            # 5. Check file extensions
            file_ext = item.suffix.lower()
            if include_extensions and file_ext not in include_extensions:
                continue
            if exclude_extensions and file_ext in exclude_extensions:
                continue

            # 6. Check file size
            if item.stat().st_size > max_file_size_kb * 1024:
                file_prompts.append(
                    f"--- File {item.relative_to(project_path)} is too large (>{max_file_size_kb}KB), content skipped. ---\n"
                )
                continue

            # 7. Read file content
            try:
                
                with open(item, 'r', encoding='utf-8', errors='replace') as f:
                    file_content = f.read()
                file_prompts.append(
                    FILE_PROMPT.format(
                        file=item.relative_to(project_path), # Get relative path for cleaner output
                        file_content=file_content
                    )
                )
            except Exception as e:
                file_prompts.append(
                    f"--- Could not read file {item.relative_to(project_path)}: {e} ---\n"
                )

    all_file_contents_prompt = "\n".join(file_prompts)
    return f"{overview_prompt}\n{all_file_contents_prompt}"

if __name__ == "__main__":
    proj_dir = "./"
    prompt = generate_proj_prompt_2(proj_dir)
    print(prompt)