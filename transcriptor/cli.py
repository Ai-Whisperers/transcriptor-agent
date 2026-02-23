import typer
import os
from transcriptor.engine import TranscriptorEngine
from transcriptor.collector import Collector

app = typer.Typer()

@app.command()
def version():
    """Display the version of Transcriptor."""
    typer.echo("Transcriptor v0.3.0 (Cascaded Fallback)")

@app.command()
def transcribe(file_path: str):
    """Transcribe a single audio file with cascaded fallback."""
    if not os.path.exists(file_path):
        typer.echo(f"Error: File not found: {file_path}", err=True)
        raise typer.Exit(code=1)
    
    engine = TranscriptorEngine()
    try:
        result = engine.transcribe(file_path)
        meta = result["metadata"]
        typer.echo(f"✅ Success! Provider: {meta.get('provider')}, Model: {meta.get('model')}")
        typer.echo("-" * 20)
        typer.echo(result["text"])
        typer.echo("-" * 20)
    except Exception as e:
        typer.echo(f"❌ Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def batch(
    directory: str = typer.Option("targets", help="Base directory for audio collection"),
    output_dir: str = typer.Option("outputs", help="Directory for transcription results"),
    log_file: str = typer.Option("transcription_log.txt", help="Log file for progress")
):
    """Transcribe all audio files recursively with cascaded fallback."""
    collector = Collector(base_dir=directory)
    files_to_process = collector.collect()
    
    if not files_to_process:
        typer.echo(f"No audio files found in {directory}")
        return

    os.makedirs(output_dir, exist_ok=True)
    engine = TranscriptorEngine()
    
    msg = f"🚀 Starting cascaded batch transcription for {len(files_to_process)} files...\n"
    typer.echo(msg)
    
    for input_path in files_to_process:
        rel_path = os.path.relpath(input_path, directory)
        clean_name = rel_path.replace(os.sep, "_")
        # Include extension in the output name to avoid collisions (e.g. .mpeg and .ogg with same name)
        output_path = os.path.join(output_dir, f"{clean_name}.txt")
        
        if os.path.exists(output_path):
            continue

        typer.echo(f"Processing: {rel_path}...")
        try:
            result = engine.transcribe(input_path)
            meta = result["metadata"]
            
            content = [
                f"METADATA: Provider={meta.get('provider')}, Model={meta.get('model')}",
                f"FILE: {rel_path}",
                "-" * 40,
                result["text"]
            ]
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(content))
            
            typer.echo(f"✓ Saved to {output_path} (via {meta.get('provider')})")
        except Exception as e:
            typer.echo(f"✗ Failed: {rel_path}: {e}", err=True)

if __name__ == "__main__":
    app()
