from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve(strict=True).parent.parent
DJANGO_ROOT = PROJECT_ROOT / "{{ project_name }}"

DEFAULT_ENV = {"DJANGO_SETTINGS_MODULE": "{{ project_name }}.settings.BaseSettings"}
