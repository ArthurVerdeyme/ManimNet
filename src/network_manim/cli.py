"""Simple Typer CLI wrapper around Manim."""
import typer
from manim import config
from .scenes.multi_clique import MultiCliqueAnimated7

app = typer.Typer(add_help_option=False, rich_help_panel="🕹️  Commands")

@app.command()
def render(scene: str = "multi-clique", quality: str = "m") -> None:
    """Render *scene* at the desired *quality* (l, m, h, 4k)."""
    match scene:
        case "multi-clique":
            scene_cls = MultiCliqueAnimated7
        case _:
            typer.secho(f"Unknown scene ‘{scene}’.", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)

    config.quality = quality
    scene_cls().render()

if __name__ == "__main__":  # pragma: no cover
    app()