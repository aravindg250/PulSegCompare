# Pulmonary Artery Segmentation Comparison

This repository is part of a Carnegie Mellon University research project that aims to automate the segmentation of the pulmonary arteries from mouse and sheep lungs from MicroCT scans and determine the accuracy of the computer-generated model.

## Features

- Converts an `.nrrd` 3D segmentation to a multi-image `.tif` stack.
- Overlays the computer-generated `.tif` stack on top of the 3D Slicer exported segmentation.
- Compares the accuracy of the computer model.
- Displays the error per slice and overall error.


## Usage

1. Replace the corresponding file paths in `filePaths.py`.
2. Run `main.py`.



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors and Acknowledgements

- Aravind Gunasekaran
- Dr. Jason Szafron

## Technologies Used

- Python
- NumPy
- PILLOW
- scikit-image
- nrrd

