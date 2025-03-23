# Unreal Engine Locres Translators Tools

<div align="center">
  <img src="assets/banner.svg" alt="Unreal Engine Locres Translators Tools Banner" width="600">
</div>

<div align="center">

![Unreal Engine](https://img.shields.io/badge/Unreal%20Engine-black?style=for-the-badge&logo=unrealengine) ![Translators love](https://img.shields.io/badge/Translators%20%E2%9D%A4-green?style=for-the-badge) ![Built with Python](https://img.shields.io/badge/Built%20with-Python-%233776AB?style=for-the-badge&logo=python)

</div>

Unreal Engine Locres Translators Tools is a community-driven command-line application designed to streamline the localization process for Unreal Engine projects. It enables translators and developers to extract dialogues and text from locres files into a CSV format for translation purposes, and then seamlessly reapply those translations back into the original locres files. Additionally, the tool integrates with `u4pak` to list and extract files from pak archives.

---

## Overview

This tool provides robust commands that simplify localization tasks:

**Decode:**  
Transforms a `.locres` file into a CSV file. When using the `--variables` option, the generated CSV contains three columns—*Variable*, *Original*, and *Translation*—with the variable formatted as `<namespace.name|entry.key>`. Without this option, the CSV includes only the *Original* and *Translation* columns. (Note: All newline characters in the text are replaced by the literal `\n`.)

**Encode:**  
Incorporates translations from a CSV file into a `.locres` file. The CSV should have three columns if the `--variables` option is used; otherwise, it should consist of two columns. During this process, literal `\n` sequences are converted back to actual newline characters.

**u4pak-unpack:**  
Extracts a designated folder from a pak file through the `u4pak` tool. This command automatically downloads the correct binary for your OS, temporarily stores it, and executes the extraction. The confirmation prompt can be bypassed using the `--yes` flag.

**u4pak-list:**  
Lists the files contained in a pak file via `u4pak`. File names are printed to the console or, if specified with `--output`, saved to a text file. Similar to the unpack command, this also entails an automatic binary download and can skip confirmation with the `--yes` flag.

---

## Installation

Clone the repository with:

```bash
git clone https://github.com/efonte/ue-localization-tools.git
cd ue-localization-tools
```

(Optional) Create and activate a virtual environment to isolate dependencies.

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## Usage

After installation, you can run the tool directly from the command line. Here are some common examples:

**Decoding a locres file into CSV:**

```bash
python locres_tool.py decode path/to/input.locres path/to/output.csv
```

**Encoding a locres file using CSV translations:**

```bash
python locres_tool.py encode path/to/input.locres path/to/translations.csv path/to/updated.locres
```

**Extracting a folder from a pak file:**

```bash
python locres_tool.py u4pak-unpack path/to/pakchunk0-WindowsNoEditor.pak "ColonyShipGame/Content/Localization" path/to/output_folder --yes
```

**Listing files in a pak file:**

```bash
python locres_tool.py u4pak-list path/to/pakchunk0-WindowsNoEditor.pak --output path/to/list.txt --yes
```

For more detailed options and usage instructions, run:

```bash
python locres_tool.py --help
```

---

## Contributing

Contributions, bug reports, and feature suggestions are welcome! If you encounter any issues or have ideas for improvements, please feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.
