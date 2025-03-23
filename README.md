# Unreal Engine Locres Translators Tools

```
 ██▓     ▒█████   ▄████▄   ██▀███  ▓█████   ██████    ▄▄▄█████▓ ▒█████   ▒█████   ██▓
▓██▒    ▒██▒  ██▒▒██▀ ▀█  ▓██ ▒ ██▒▓█   ▀ ▒██    ▒    ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒
▒██░    ▒██░  ██▒▒▓█    ▄ ▓██ ░▄█ ▒▒███   ░ ▓██▄      ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░
▒██░    ▒██   ██░▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓█  ▄   ▒   ██▒   ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░
░██████▒░ ████▓▒░▒ ▓███▀ ░░██▓ ▒██▒░▒████▒▒██████▒▒     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒
░ ▒░▓  ░░ ▒░▒░▒░ ░ ░▒ ▒  ░░ ▒▓ ░▒▓░░░ ▒░ ░▒ ▒▓▒ ▒ ░     ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░
░ ░ ▒  ░  ░ ▒ ▒░   ░  ▒     ░▒ ░ ▒░ ░ ░  ░░ ░▒  ░ ░       ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░
  ░ ░   ░ ░ ░ ▒  ░          ░░   ░    ░   ░  ░  ░       ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░
    ░  ░    ░ ░  ░ ░         ░        ░  ░      ░                  ░ ░      ░ ░      ░
                 ░
```

Unreal Engine Locres Translators Tools is a community-driven command-line tool for extracting and reinserting dialogues and text from Unreal Engine locres files. It helps translators and developers manage localization by allowing you to decode locres files into CSV for translation and encode CSV translations back into locres files. The tool also integrates with `u4pak` to list and extract files from pak archives.

---

## Overview

This tool provides the following commands:

- **decode**  
  Decodes a `.locres` file into a CSV file.  
  When used with the `--variables` option, the CSV will have three columns:  
  *Variable, Original, Translation* (with Variable formatted as `<namespace.name|entry.key>`). Otherwise, the CSV contains two columns: *Original* and *Translation*.  
  Note: Newlines in the text are replaced by literal `\n`.

- **encode**  
  Applies translations from a CSV file to a `.locres` file and writes the updated file.  
  If the `--variables` option is enabled, the CSV is expected to have three columns. Without it, the CSV should have two columns.  
  During replacement, literal `\n` sequences in the CSV are converted back to newlines.

- **u4pak-unpack**  
  Extracts a specific folder from a pak file using the `u4pak` tool.  
  This command downloads the appropriate `u4pak` binary for your OS, extracts it to a temporary directory, and executes it.  
  You can skip the confirmation prompt by using the `--yes` flag.

- **u4pak-list**  
  Lists the files contained in a pak file using the `u4pak` tool.  
  The list of files is output to the console or, if specified with `--output`, written to a text file.  
  Like unpacking, this command also downloads and uses the `u4pak` binary (optionally bypassing the confirmation with `--yes`).

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/efonte/ue-localization-tools.git
   cd ue-localization-tools
   ```

2. (Optional) Create and activate a virtual environment.
3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

After installation, you can run the tool from the command line. For example:

- Decode a locres file into CSV:

  ```bash
  python locres_tool.py decode path/to/input.locres path/to/output.csv
  ```

- Encode a locres file from CSV translations:

  ```bash
  python locres_tool.py encode path/to/input.locres path/to/translations.csv path/to/updated.locres
  ```

- Extract a specific folder from a pak file:

  ```bash
  python locres_tool.py u4pak-unpack path/to/pakchunk0-WindowsNoEditor.pak "ColonyShipGame/Content/Localization" path/to/output_folder --yes
  ```

- List files in a pak file:

  ```bash
  python locres_tool.py u4pak-list path/to/pakchunk0-WindowsNoEditor.pak --output path/to/list.txt --yes
  ```

For more details, run the help command:

```bash
python locres_tool.py --help
```

---

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

---

## License

This tool is available under the MIT License.
