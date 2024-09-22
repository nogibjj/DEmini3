# generate_structure.py
import os

def generate_directory_structure(start_path='.', output_file='project_structure.md'):
    """
    Generates the file and directory structure of the project and saves it to a markdown file.

    :param start_path: The root directory to start generating the structure from.
    :param output_file: The output markdown file where the structure will be saved.
    """
    structure = []

    for root, dirs, files in os.walk(start_path):
        # Skip hidden directories and files
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * level
        structure.append(f"{indent}- {os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            structure.append(f"{sub_indent}- {f}")

    # Save the structure to the output markdown file
    with open(output_file, 'w') as f:
        f.write('# Project File Structure\n\n')
        f.write('\n'.join(structure))

    print(f"Project structure saved to {output_file}")

if __name__ == "__main__":
    generate_directory_structure('.', 'project_structure.md')
