from pathlib import Path

def ask(prompt, default=None):
    if default:
        return input(f"{prompt} [{default}]: ") or default
    return input(f"{prompt}: ")

def init_project():
    print("Welcome to Clean-Py-Kit project initializer!")
    name = ask("Project name", "my_clean_py_kit_project")
    use_color = ask("Use colored logging? (y/n)", "y").lower() == "y"
    log_fmt = ask("Logging format (default/json)", "default")

    project_dir = Path(name)
    project_dir.mkdir(exist_ok=True)

    src_dir = project_dir / "src"
    src_dir.mkdir(parents=True, exist_ok=True)
    (src_dir / "__init__.py").touch()

    config_yaml = project_dir / "config.yaml"
    config_yaml.write_text(f"log_level: DEBUG\nlog_use_color: {use_color}\nlog_format: {log_fmt}\n")

    main_py = src_dir / "main.py"
    main_py.write_text(f"""from cleanpykit.config import BaseConfig, load_config
from cleanpykit.logging import get_logger
                       
class Config(BaseConfig):
    log_level: str = "DEBUG"
    log_use_color: bool = {str(use_color)}
    log_format: str = "{log_fmt}"
                    
config = load_config(Config)
logger = get_logger(__name__, level=config.log_level, fmt=config.log_format, use_color=config.log_use_color)
                    
logger.info("Hello from {name}!")""")

    (project_dir / "README.md").write_text(f"# {name}\n\nGenerated with Clean-Py-Kit CLI")
    print(f"Project '{name}' initialized successfully at {project_dir.resolve()}")

init_project()