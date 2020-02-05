#!/usr/bin/env python

import sys
import os
import subprocess

# Script taken from doing the needed operation
# (Filters > Remeshing, Simplification and Reconstruction >
# Quadric Edge Collapse Decimation, with parameters:
# 0.9 percentage reduction (10%), 0.3 Quality threshold (70%)
# Target number of faces is ignored with those parameters
# conserving face normals, planar simplification and
# post-simplimfication cleaning)
# And going to Filter > Show current filter script

cwd = os.getcwd()

def create_tmp_filter_file(max_size, filename='hole-filling.mlx'):

    filter_script_mlx = """<!DOCTYPE FilterScript>
    <FilterScript>
    <filter name="Merge Close Vertices">
    <Param name="Threshold" description="Merging distance" value="0" min="0" max="1" type="RichAbsPerc" tooltip="All the vertices that closer than this threshold are merged together. Use very small values, default values is 1/10000 of bounding box diagonal."/>
    </filter>
    <filter name="Close Holes">
    <Param type="RichInt" value="{max_size}" name="MaxHoleSize"/>
    <Param type="RichBool" value="false" name="Selected"/>
    <Param type="RichBool" value="true" name="NewFaceSelected"/>
    <Param type="RichBool" value="true" name="SelfIntersection"/>
    </filter>
    </FilterScript>
    """.format(max_size=max_size)


    print("***********************************")
    print(filter_script_mlx)
    print("***********************************")

    with open(cwd + '/' + filename, 'w') as f:
        f.write(filter_script_mlx)
    return cwd + '/'+ filename


def hole_filling(in_file, out_file, max_size):

    filter_script_path = create_tmp_filter_file(max_size)

    print(filter_script_path)

    # Add input mesh
    command = 'xvfb-run -a -s "-screen 0 800x600x24" meshlabserver -i ' + in_file
    # Add the filter script
    command += " -s " + filter_script_path
    # Add the output filename and output flags
    command += " -o " + out_file
    # Execute command
    print("Going to execute: " + command)
    output = subprocess.call(command, shell=True)
    last_line = output
    print()
    print("Done:")
    print(in_file + " > " + out_file + ": " + str(last_line))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print(sys.argv[0] + " /path/to/input_mesh max_hole_size")
        print("Example:")
        print(sys.argv[0] + " /home/myuser/mymesh.stl 30")
        exit(0)

    in_mesh = sys.argv[1]
    filename = in_mesh.split('/')[-1].split('.')[0]
    max_size = int(sys.argv[2])

    folder_name = filename.replace('.', '_')
    tmp_folder_name = cwd + '/'+ filename + '_meshes/'

    print("Input mesh: " + in_mesh + " (filename: " + filename + ")")
    print("Max hole size: " + str(max_size))
    print("Output folder: " + tmp_folder_name)
    print()

    out_mesh = tmp_folder_name + filename + "_hole_filling_{max_size}".format(max_size=max_size) + ".stl"
    hole_filling(in_mesh, out_mesh, max_size)

    print()
    print("Done reducing, find the files at: " + tmp_folder_name)


