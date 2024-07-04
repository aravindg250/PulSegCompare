# Pulmonary Hypertension Segmentation Comparison

Pulmonary hypertension (PH) is a deadly disease with a worse prognosis than systemic hypertension. In PH, the distal pulmonary vasculature remodels, leading to an increase in blood pressure within the lungs. To track disease progress, clinicians use imaging such as computed tomography (CT) and magnetic resonance imaging (MRI) to quantify changes in lung geometry and morphometry. However, many of the most important changes occur in the distal vasculature that are too small to capture with typical imaging approaches.

To better understand the time course of disease development, researchers have turned to ex vivo imaging in animal models of disease. Micro-CT has much higher resolution than traditional CT and is able to capture the size of vessels that drive long-term complications. In these micro-CT scans, thousands of vessel segments are present, which poses a challenge for manual measurements.

## Project Overview
This project investigates an automated segmentation tool to determine its fidelity against manual measurements, focusing on both geometric and morphometric factors that determine patient hemodynamics. We utilize open-source software packages, 3D Slicer and ClearMap, to evaluate images of mouse, sheep, and human lungs with different types of PH. The goal is to quantify the visible changes in the disease.

## Repository Purpose
This repository is part of a Carnegie Mellon University research project that aims to:

Automate the segmentation of the pulmonary arteries from mouse and sheep lungs from Micro-CT scans.
Determine the accuracy of the computer-generated model.
By automating the segmentation process, we hope to streamline the analysis of these high-resolution scans and provide more accurate and reproducible measurements of disease progression.

## Tools and Software
* 3D Slicer: An open-source software platform for medical image informatics, image processing, and three-dimensional visualization.
* ClearMap: A software for analyzing, visualizing, and exploring large-scale biological image data.

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

## Tools and Software
* 3D Slicer: An open-source software platform for medical image informatics, image processing, and three-dimensional visualization.
* ClearMap: A software for analyzing, visualizing, and exploring large-scale biological image data.

## TODO
- [ ] Make a region with connected black pixels
- [ ] Find eccentricity index for all regions
- [ ] Ones closer to 0 are probably vessel versus other being cros sections or others
- [ ] Compare to the segmentation (make sure overlap and offset are right)
- [ ] Find areas that have about 75% similarity within the overlap region
- [ ] Those are probably what the tubmap picked up as vessels
- [ ] Go step by step making each a function and then put together
