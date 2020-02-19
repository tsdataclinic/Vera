#!/bin/bash
docker run -it --rm  -p 8888:8888 -v $(pwd):/data vera jupyter lab --ip 0.0.0.0 --allow-root --NotebookApp.notebook_dir=/data
