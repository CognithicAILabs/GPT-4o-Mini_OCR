# GPT-4o-Mini OCR

A powerful command-line OCR (Optical Character Recognition) tool that uses OpenAI's GPT-4o-mini model to extract text from images and scanned PDF documents.

## Features

- Extract text from images (JPG, PNG, GIF, WebP)
- Extract text from scanned PDF documents
- Preserve layout and formatting
- Handle tables and structured content
- Custom prompts for specialized extraction
- Multiple OpenAI model support
- Save output to file or display in console

## Prerequisites

- Python 3.7 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation

1. Clone this repository:
```bash
git clone https://github.com/CognithicAILabs/GPT-4o-Mini_OCR.git
cd GPT-4o-Mini_OCR
```

2. Install required dependencies:
```bash
pip install openai
```

3. Set up your OpenAI API key:

**Option 1: Environment variable (recommended)**
```bash
# Windows
set OPENAI_API_KEY=your_api_key_here

# Linux/Mac
export OPENAI_API_KEY=your_api_key_here
```

**Option 2: Pass via command line**
```bash
python openai_ocr.py image.jpg -k your_api_key_here
```

## Usage

### Basic Usage

Extract text from an image and display in console:
```bash
python openai_ocr.py image.jpg
```

### Save Output to File

```bash
python openai_ocr.py image.jpg -o output.txt
```

### Process PDF Documents

```bash
python openai_ocr.py document.pdf -o extracted_text.txt
```

### Use Custom Prompt

```bash
python openai_ocr.py image.jpg -p "Extract only the email addresses from this image"
```

### Specify Different Model

```bash
python openai_ocr.py image.jpg -m gpt-4o
```

## Command Line Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `input_file` | | Path to the image or PDF file (required) |
| `--output` | `-o` | Output file path (optional, prints to console if not specified) |
| `--api-key` | `-k` | OpenAI API key (or set OPENAI_API_KEY environment variable) |
| `--prompt` | `-p` | Custom prompt for text extraction |
| `--model` | `-m` | OpenAI model to use: `gpt-4o-mini` (default), `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo` |

## Supported File Formats

- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- **Documents**: `.pdf`

## Examples

### Example 1: Extract text from a receipt
```bash
python openai_ocr.py receipt.jpg -o receipt_text.txt
```

### Example 2: Extract data from a table
```bash
python openai_ocr.py table.png -p "Extract the data from this table and format it as CSV"
```

### Example 3: Process a scanned document
```bash
python openai_ocr.py scanned_doc.pdf -o document.txt -m gpt-4o
```

## How It Works

1. The script encodes the image or PDF to base64 format
2. Sends it to OpenAI's API with the specified prompt
3. GPT-4o-mini (or selected model) processes the image and extracts text
4. Returns the extracted text preserving layout and formatting

## Error Handling

The script includes error handling for:
- Missing API key
- File not found
- Unsupported file types
- API errors

## Cost Considerations

Using OpenAI's API incurs costs based on:
- Model used (gpt-4o-mini is the most cost-effective)
- Image size and complexity
- Number of tokens in the response

GPT-4o-mini is recommended for most OCR tasks due to its balance of performance and cost.

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on GitHub.

## Acknowledgments

Built using OpenAI's GPT-4o-mini vision capabilities.

---

**Developed by Cognithic AI Labs**
