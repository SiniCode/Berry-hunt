from invoke import task

@task
def start(ctx):
    ctx.run("python3 src/index.py")

@task
def lint(ctx):
    ctx.run("pylint src")
