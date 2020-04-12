# horoscopegenerator
Creating horoscopes with Neural Nets


## Setup
### Install

    # You'll need conda.  

    # make sure you have python 3.7
    # anaconda is recommended if you don't have it:
    curl -o /tmp/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
    bash /tmp/miniconda.sh -b
    ~/miniconda3/bin/conda init  # Use `~/miniconda3/bin/conda init zsh` for zsh users
    exec -l $SHELL
    conda install --yes python==3.7.3

    # At this point, make sure you have a `base` in your terminal string
    conda create -n <insert name here> python==3.7.3
    conda activate <insert name here>

    # Next, install other dependencies
    pip install -r requirements.txt


