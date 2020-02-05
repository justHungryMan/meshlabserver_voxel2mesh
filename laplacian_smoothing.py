#!/usr/bin/env python

import sys
import os
import subprocess

cwd = os.getcwd()

def create_tmp_filter_file(iterate, filename='laplacian-smoothing.mlx'):

    filter_script_mlx = """<!DOCTYPE FilterScript>
    <FilterScript>
    <filter name="Merge Close Vertices">
    <Param name="Threshold" description="Merging distance" value="0" min="0" max="1" type="RichAbsPerc" tooltip="All the vertices that closer than this threshold are merged together. Use very small values, default values is 1/10000 of bounding box diagonal."/>
    </filter>
    <filter name="Laplacian Smooth">
    <Param type="RichInt" value="{iterate}" name="stepSmoothNum"/>
    <Param type="RichBool" value="true" name="Boundary"/>
    <Param type="RichBool" value="true" name="cotangentWeight"/>
    <Param type="RichBool" value="false" name="Selected"/>
    </filter>
    </FilterScript>
    """.format(iterate=iterate)


    print("***********************************")
    print(filter_script_mlx)
    print("***********************************")

    with open(cwd + '/' + filename, 'w') as f:
        f.write(filter_script_mlx)
    return cwd + '/'+ filename


def laplacian_smoothing(in_file, out_file, iterate):

    filter_script_path = create_tmp_filter_file(iterate)

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
        print(sys.argv[0] + " /path/to/input_mesh iterate")
        print("Example:")
        print(sys.argv[0] + " /home/myuser/mymesh.stl 3")
        exit(0)

    in_mesh = sys.argv[1]
    filename = in_mesh.split('/')[-1].split('.')[0]
    iterate = int(sys.argv[2])

    tmp_folder_name = cwd + '/result/'
    3
    print("Input mesh: " + in_mesh + " (filename: " + filename + ")")
    print("Iterate size: " + str(iterate))
    print("Output folder: " + tmp_folder_name)
    print()

    out_mesh = tmp_folder_name + filename + "_laplacian_{iterate}".format(iterate=iterate) + ".stl"
    laplacian_smoothing(in_mesh, out_mesh, iterate)

    print()
    print("Done Laplacian Smoothing, find the files at: " + tmp_folder_name)


