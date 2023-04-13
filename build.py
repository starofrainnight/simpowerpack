# -*- coding: utf-8 -*-
import pathlib
import click
import subprocess
import glob
import os
from pytosim.__main__ import main as pytosim_main


@click.command()
@click.option(
    "-o",
    "--output-dir",
    default="./build",
    help="The source output directory",
)
def main(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    srcs = glob.glob("./src/*.py")
    if len(srcs) < 0:
        click.echo("No source found!")

    click.echo("Ouptut to %s" % output_dir)
    for src_fpath in srcs:
        dst_fpath = os.path.join(
            output_dir,
            pathlib.Path(src_fpath).with_suffix(".em").name,
        )

        click.echo("Transpile: %s" % src_fpath)

        pytosim_main(["compile", "-o", dst_fpath, src_fpath])


if __name__ == "__main__":
    main()
