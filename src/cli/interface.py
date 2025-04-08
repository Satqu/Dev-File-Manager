import click
from .commands import search,organize,stats


@click.group()
def cli():
    """Інструмент для управління файлами та проєктами

    Команди:
    - Пошук файлів за сигнатурами (текстовими рядками)
    - Організація проєктів за мовами програмування
    - Аналіз статистики мов програмування у проєктах
    """
    pass

cli.add_command(search)
cli.add_command(organize)
cli.add_command(stats)

if __name__ == '__main__':
    cli()