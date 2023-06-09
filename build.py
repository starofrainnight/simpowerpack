#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import click
import subprocess
import glob
import os
import subprocess
import fnmatch
from pytosim.__main__ import (
    compile as pytosim_compile,
    compile_base as pytosim_compile_base,
)


@click.command()
@click.option(
    "-o",
    "--output-dir",
    default="./build",
    help="The source output directory",
)
@click.pass_context
def main(ctx, output_dir):
    # type: (click.Context, str) -> None
    os.makedirs(output_dir, exist_ok=True)

    srcs = list(
        filter(
            lambda it: not fnmatch.fnmatch(os.path.basename(it), "__init__.*"),
            glob.glob("./src/*.py"),
        )
    )
    if len(srcs) < 0:
        click.echo("No source found!")

    try:
        subprocess.check_call("mypy ./src", shell=True)
    except subprocess.CalledProcessError:
        raise click.ClickException(
            "Mypy check failed! Please fix those issues first!"
        )

    click.echo("Ouptut to %s" % output_dir)

    for src_fpath in srcs:
        dst_fpath = os.path.join(
            output_dir,
            pathlib.Path(src_fpath).with_suffix(".em").name,
        )

        click.echo("Transpile: %s" % src_fpath)

        ctx.invoke(pytosim_compile, output=dst_fpath, pyscript=src_fpath)

    ctx.invoke(pytosim_compile_base, output_dir=output_dir)


if __name__ == "__main__":
    main()
