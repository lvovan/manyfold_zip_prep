# Manyfold ZIP Prep

Manyfold ZIP Prep is a command line utility designed to prepare ZIP model files for uploading [Manyfold](https://manyfold.app). The input is a folder containing ZIP files that contain one or multiple 3D models arranged in folders and in the case of multiple subfolders creates a set of ZIP files, one per folder (each folder corresponding to one model as per Manyfold's scanner logic)

## Features

- Process ZIP files containing 3D models
- Rezip files to ensure each ZIP contains a single model
- Validate and prepare files for Manyfold upload

## Installation

No installation is necessary: this script only uses standard Python 3.x modules

## Usage

To use the utility, run the following command:

```sh
python manyfold_zip_prep.py <input_zip_file> <output_directory> [optional: --exclusion_list]
```

### Arguments

- `<input_zip_file>`: Path to the input ZIP file containing 3D models.
- `<output_directory>`: Path to the directory where the processed ZIP files will be saved.
- `<--exclusion_list [str1, str2...]>`: (optional) in Python syntax, a list of string that, if encountered in paths of the files contained input ZIP file, will cause these items to be skipped

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/yourusername/manyfold_zip_prep).

