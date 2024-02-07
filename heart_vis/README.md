<div id="top"></div>
<div align="center">
  <h3 align="center">Bi-directional streamlines and glyphs in Blender</h3>
  <p align="center">
    A Blender Python module to build 3D reconstructions as seen in Dileep, Syed et al. 
</div>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This Blender-Python workflow was used to create the 3D models used throughout the paper:
(Dileep, Syed, et al.)

<div id="refs" class="references csl-bib-body hanging-indent">
<div id="ref-xie2018" class="csl-entry">

Drisya Dileep, Tabish Syed,  Tyler Sloan, Dhandapany Perundurai, Kaleem Siddiqi, and Minhajuddin Sirajuddin. 2023. *Cardiomyocyte orientation recovery at micrometer scale reveals long‐axis fiber continuum in heart walls*.
EMBO J (2023) 42: e113288 https://doi.org/10.15252/embj.2022113288
The scripts used to generate the 3D models are assembled into this module.

</div>

</div>

<p align="right">(<a href="#top">back to top</a>)</p>


### Built With
* [Blender](https://blender.org/)
* [Python](https://python.org/)
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started
All scripts in this repository must be run within [Blender](https://blender.org). At a minimum, you must install a version of Blender >= 2.80. Setting up Blender is straightforward, as is loading and running a Python script from 'Scripting' window inside the Blender UI. 
Blender come with its own Python interpreter, the version of which depends on the Blender release. This Python installation is independent of the system Python installation, and so installing packages to the correct Python can be tricky. The Python included with Blender contains several useful packages already, such as NumPy and is located in `<path_to_blender_installation>/<blender_version>/Python/ `. However, running scripts from this repository requires additions python packages which need to be added to the bundled interpreter. The required packages can be easily added to Blender Python by adding `pip` to Blender Python using `ensurepip`.

To add `pip` to Blender Python, locate the Blender Python interpreter and run 
```sh
 python3.X  -m ensurepip --upgrade
```
<p align="right">(<a href="#top">back to top</a>)</p>

### Prerequisites
Some advanced processing steps will require additional packages, as listed below. A full list of requirements can be found in the `requirements.txt`  file. Make sure you use pip for bundled Python interpreter for you Blender installation to run the following steps.
```sh
     pip install -r path/to/requirements.txt
```

<!-- USAGE EXAMPLES -->
## Usage

Once Blender is loaded, navigate to the 'Scripting' tab, and load a script from file. Navigate to the folder containing this module, and open `main.py`.

`main.py` loads the necessary scripts and functions from the module, and builds the model according to the parameters in `config.py`

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Clean code and publish to Git
- [x] Add License
- [ ] Upload .blend template

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@quorumetrix](https://twitter.com/quorumetrix) - tyler@quorumetrix.com

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [The Blender Foundation](https://https://www.blender.org/)
* [scikit-image](https://https://scikit-image.org/)
* [Choose an Open Source License](https://choosealicense.com)

<p align="right">(<a href="#top">back to top</a>)</p>
