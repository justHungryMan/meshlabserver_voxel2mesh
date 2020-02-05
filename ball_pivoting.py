#!/usr/bin/env python

import sys
import os
import subprocess

cwd = os.getcwd()

def create_tmp_filter_file(clustering, angleThreshold, filename='ball-pivoting.mlx'):

    filter_script_mlx = """<!DOCTYPE FilterScript>
    <!DOCTYPE FilterScript>
    <FilterScript>
    <filter name="Surface Reconstruction: Ball Pivoting">
    <Param type="RichAbsPerc" value="0" min="0" name="BallRadius" max="2928.8"/>
    <Param type="RichFloat" value="{clustering}" name="Clustering"/>
    <Param type="RichFloat" value="{angleThreshold}" name="CreaseThr"/>
    <Param type="RichBool" value="false" name="DeleteFaces"/>
    </filter>
    </FilterScript>
    """.format(clustering=clustering, angleThreshold=angleThreshold)


    print("***********************************")
    print(filter_script_mlx)
    print("***********************************")

    with open(cwd + filename, 'w') as f:
        f.write(filter_script_mlx)
    return cwd + '/' + filename


def ball_pivoting(in_file, out_file, clustering, angleThreshold):

    filter_script_path = create_tmp_filter_file(clustering, angleThreshold)


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
    if len(sys.argv) < 3:
        print("Usage:")
        print(sys.argv[0] + " /path/to/input_mesh clustering angle_threshold")
        print("Example:")
        print(sys.argv[0] + " /home/myuser/mymesh.xyz 100 90")
        exit(0)

    in_mesh = sys.argv[1]
    filename = in_mesh.split('/')[-1].split('.')[0]
    clustering = int(sys.argv[2])
    angle_threshold = int(sys.argv[3])

    tmp_folder_name = cwd + '/result/' 

    print("Input mesh: " + in_mesh + " (filename: " + filename + ")")
    print("Clustering: " + str(clustering))
    print("Angle Threshold: " + str(angle_threshold))
    print("Output folder: " + tmp_folder_name)
    print()
    try:
        os.mkdir(tmp_folder_name)
    except OSError as e:
        print(sys.stderr, "Exception creating folder for meshes: " + str(e))

    out_mesh = tmp_folder_name + filename + '_ball_pivoting' + ".stl"
    ball_pivoting(in_mesh, out_mesh, clustering, angle_threshold)

    print()
    print("Done Ball Pivoting, find the files at: " + tmp_folder_name)


