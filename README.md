<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

<br />
<div align="center">
  <a href="https://github.com/jerrome2685/olygeo">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">olygeo</h3>

  <p align="center">
    A projective geometry library for olympiad-style constructions and proofs in Python.
    <br />
    <a href="https://github.com/jerrome2685/olygeo"><strong>Explore the docs »</strong></a>
    <br /><br />
    <a href="https://github.com/jerrome2685/olygeo">View Demo</a>
    &middot;
    <a href="https://github.com/jerrome2685/olygeo/issues/new?labels=bug&template=bug-report.md">Report Bug</a>
    &middot;
    <a href="https://github.com/jerrome2685/olygeo/issues/new?labels=enhancement&template=feature-request.md">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a>
      <ul><li><a href="#built-with">Built With</a></li></ul>
    </li>
    <li><a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

Olygeo is a Python library for olympiad geometry, concentrated on verifying geometrical statements. It also can numerically calculate the   

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![Python][python-shield]][python-url]
- [![Sympy][sympy-shield]][sympy-url]
- [![mpmath][mpmath-shield]][mpmath-url]
- [![multimethod][multimethod-shield]][multimethod-url]
- [![Matplotlib][matplotlib-shield]][matplotlib-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

Follow these steps to get a local copy up and running.

### Prerequisites

* Python 3.8 or higher
* pip

### Installation

1. Clone the repo

   ```sh
   git clone https://github.com/jerrome2685/olygeo.git
   cd olygeo
   ```
2. Install olygeo

   ```sh
   pip install -e .
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Here’s a quick example:

```python
from olygeo import *

A = ProPoint(0,0,1)
B = ProPoint(1,0,1)
C = ProPoint(0,1,1)
tri = ProTriangle(A, B, C)
I = tri.incenter()

print(I)
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

* **1. Condition statements API**
  DSL for predicates like `on_segment`, `in_polygon`, `on_different_sides`.

* **2. Conditional definitions**
  Constructors that solve for coordinates, e.g., “Point X on segment AB” or mixtilinear incircle touchpoints.

* **3. Concurrency & Collinearity**
  Generic predicates: `Geo.is_concurrent([ℓ1,ℓ2,ℓ3])`, `Geo.is_collinear([P,Q,R])`.

* **4. ProPolygon class**
  Polygon type with `.contains()`, `.intersect()`, built from vertices or bounding lines.

* **5. Drawer / Visualizer**
  Numeric plotting layer using Matplotlib or SVG, honoring geometric constraints.

* **6. Prover**
  Algebraic prover using grid-based zero-testing to prove statements exactly.

See [open issues](https://github.com/jerrome2685/olygeo/issues) for more.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

Contributions are welcome! Please fork the repo, create a feature branch, and open a pull request. For details, see `CONTRIBUTING.md`.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Hyeongjoe Chu – [GitHub](https://github.com/jerrome2685)
Project Link: [https://github.com/jerrome2685/olygeo](https://github.com/jerrome2685/olygeo)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments

* [Sympy](https://www.sympy.org/)
* [mpmath](https://mpmath.org/)
* [multimethod](https://github.com/mrocklin/multimethod)
* [Matplotlib](https://matplotlib.org/)
* Best-README-Template by [othneildrew](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/jerrome2685/olygeo.svg?style=for-the-badge
[contributors-url]: https://github.com/jerrome2685/olygeo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/jerrome2685/olygeo.svg?style=for-the-badge
[forks-url]: https://github.com/jerrome2685/olygeo/network/members
[stars-shield]: https://img.shields.io/github/stars/jerrome2685/olygeo.svg?style=for-the-badge
[stars-url]: https://github.com/jerrome2685/olygeo/stargazers
[issues-shield]: https://img.shields.io/github/issues/jerrome2685/olygeo.svg?style=for-the-badge
[issues-url]: https://github.com/jerrome2685/olygeo/issues
[license-shield]: https://img.shields.io/github/license/jerrome2685/olygeo.svg?style=for-the-badge
[license-url]: https://github.com/jerrome2685/olygeo/blob/master/LICENSE
ib-url]: https://matplotlib.org/

[python-shield]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org/
[sympy-shield]: https://img.shields.io/badge/Sympy-336790?style=for-the-badge&logo=sympy&logoColor=white
[sympy-url]: https://www.sympy.org/
[mpmath-shield]: https://img.shields.io/badge/mpmath-005555?style=for-the-badge&logo=python&logoColor=white
[mpmath-url]: https://mpmath.org/
[multimethod-shield]: https://img.shields.io/badge/multimethod-552288?style=for-the-badge&logo=python&logoColor=white
[multimethod-url]: https://github.com/mrocklin/multimethod
[matplotlib-shield]: https://img.shields.io/badge/Matplotlib-CC5500?style=for-the-badge&logo=python&logoColor=white
[matplotlib-url]: https://matplotlib.org/

