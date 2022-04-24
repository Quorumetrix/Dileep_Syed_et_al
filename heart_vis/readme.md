<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Bi-directional streamlines and glyphs in Blender</h3>

  <p align="center">
    A Blender Python module to build 3D reconstructions as seen in Dileep, Syed et al. (Under review)


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

(Dileep, Syed, et al. _in Review_)

<div id="refs" class="references csl-bib-body hanging-indent">

<div id="ref-xie2018" class="csl-entry">

Drisya Dileep, Tabish Syed,  Tyler Sloan, Dhandapany Perundurai, Kaleem Siddiqi, and Minhajuddin Sirajuddin. 202X. *Myofiber reconstruction at micron scale reveals longitudinal bands in heart ventricular walls*.

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

Blender come with its own Python installation, the version of which depends on the Blender release. This Python installation is independent of the system Python installation, and so installing packages to the correct Python can be tricky. The Python included with Blender contains several useful packages already, such as NumPy. However, for more advanced usage, one will need to install additional Python packages to the Blender Python installation. A comprehensive tutorial on how to do this is beyond the scope of this paper.

### Prerequisites

At a minimum, you must install a version of Blender >= 2.80. Some advanced processing steps will require additional packages, as listed below. A full list of requirements can be found in the `requirements.txt`  file

Individual packages can be installed separately:

* scikit image: Image processing in Python
  ```sh
  pip install scikit-image
  ```
 * Pillow: Image processing in Python
    ```sh
    pip install pillow
    ```

Or the entire list of dependencies can be installed at once:

```sh
pip install r- path/to/requirements.txt
```

### Installation

_Setting up Blender is straightforward, as is loading and running a Python script from Blender's 'Scripting' window. However, ensuring any additional Python packages are installed and available to Blender's Python installation is much trickier._

1. Download a recent version of [Blender](https://blender.org)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Location your Blender installation, and navigate to Blender's Python installation. It should be found at MyDrive/Program Files/Blender Foundation/Blender/X.X/python/bin

4. Open system console and navigate to the folder containing your version of Blender's Python installation.
From this folder, ensure that pip is installed, and use pip to install necessary packages to Blenders Python installation.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Once Blender is loaded, navigate to the 'Scripting' tab, and load a script from file. Navigate to the folder containing this module, and open main.py.

main.py loads the necessary scripts and functions from the module, and builds the model according to the parameters in config.py

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

Project Link: [https://github.com/Quorumetrix/Dileep_Syed_et_al](https://github.com/Quorumetrix/Dileep_Syed_et_al)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [The Blender Foundation](https://https://www.blender.org/)
* [scikit-image](https://https://scikit-image.org/)
* [Choose an Open Source License](https://choosealicense.com)

<p align="right">(<a href="#top">back to top</a>)</p>
