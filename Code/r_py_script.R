library(reticulate)

use_condaenv('fish-video', required = T)
# py_config()
source_python('code/fishtrack.py')


py_run_string("fishtrack(n_inds = 3,
             ind_id = ['A', 'B', 'C', 'D'],
             colors = [(0,0,255), (0,255,255), (255,0,255), (255,255,255), (255,255,0), (255,0,0), (0,255,0), (0,0,0)],
             block_size = 701,
             offset = 11,
             min_area = 8000,
             max_area = 740000,
             vid_name = 'bsb_vid',
             vid_loc = 'c:/users/secor/desktop/fish-video/')")
