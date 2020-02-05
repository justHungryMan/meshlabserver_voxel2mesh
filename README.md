# meshserver_voxel2mesh

## Required
- meshlabserver
- xvfb

## How to use?

```python
python ball_pivoting.py {yourFile} {clustering} {angle_thresholg}
python hole_filling.py {yourFile} {max_size}
python laplacian_smoothing.py {yourFile} {iterate}
python taubin_smoothing.py {yourFile} {iterate}
```


## Error

- meshlabserver: cannot connect to X server

     you need use xvfb (apt get install xvfb) in this case,like this:$ xvfb-run -a -s "-screen 0 800x600x24" meshlabserver