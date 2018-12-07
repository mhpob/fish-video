library(reticulate)

use_condaenv('fish-video', required = T)
py_config()
source_python('code/fishtrack.py')

#BSB test vid: block_size = 501, offset = 10, min_area = 8000, max_area = 740000
py_run_string("fishtrack(n_inds = 3,
             ind_id = ['A', 'B', 'C', 'D'],
             colors = [(0,0,255), (0,255,255), (255,0,255), (255,255,255), (255,255,0), (255,0,0), (0,255,0), (0,0,0)],
             block_size = 451,
             offset = 10,
             min_area = 8000,
             max_area = 740000,
             vid_name = 'bsb_vid',
             vid_loc = 'p:/obrien/biotelemetry/darpa/fish-video/')")


py_run_string("fishtrack(n_inds = 1,
             ind_id = ['A', 'B', 'C', 'D'],
             colors = [(0,0,255), (0,255,255), (255,0,255), (255,255,255), (255,255,0), (255,0,0), (0,255,0), (0,0,0)],
             block_size = 61,
             offset = 45,
             min_area = 7,
             max_area = 250,
             vid_name = 'turtle_short',
             vid_loc = 'p:/obrien/biotelemetry/darpa/fish-video/')")
