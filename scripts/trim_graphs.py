#!/usr/bin/env python3

"""Deletes unessecary folders for upload into overleaf

For some reason overleaf rejects the git pushes when there are too many graphs
First copy graphs into a folder called paper_graphs
then manually delete the non nessecary folders (later add this)
Then run this script to delete all control plane results, which we don't use
It also deletes stub folders, which we also don't use (we use stub_or_multihomed)
"""

import shutil
from pathlib import Path


def delete_control_plane_dirs(start_path):
    for path in start_path.rglob('*'):
        if not path.is_dir():
            continue
        # We only use control plane in this one location
        if(path.name == 'control_plane'
           and not any(parent.name == 'ctrl_vs_data_plane' for parent in path.parents)):
            print(f"Deleting directory: {path}")
            shutil.rmtree(path)
        # We never use stub graphs in the paper
        elif path.name == 'stub':
            print(f"Deleting directory: {path}")
            shutil.rmtree(path)
        # We only use adopting_is_Any in the subprefix category
        elif(path.name == 'adopting_is_Any'
             and not any(parent.name == 'subprefix' for parent in path.parents)):
            print(f"Deleting directory: {path}")
            shutil.rmtree(path)


if __name__ == "__main__":
    delete_control_plane_dirs(Path.home() / "paper_graphs")
