import os
import base64
import argparse
from pathlib import Path
from openai import OpenAI


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_mime_type(file_path):
    extension = Path(file_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.pdf': 'application/pdf'
    }
    return mime_types.get(extension, 'image/jpeg')


def extract_text_from_image(client, image_path, custom_prompt=None):
    # Encode image
    base64_image = encode_image_to_base64(image_path)
    mime_type = get_mime_type(image_path)
    
    # Default OCR prompt
    if custom_prompt is None:
        custom_prompt = """Extract all text from this image. 
        Preserve the layout and formatting as much as possible.
        If there are tables, format them clearly.
        If there is no text, respond with 'No text found in image.'"""
    
    # Prepare the message
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": custom_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{base64_image}"
                    }
                }
            ]
        }
    ]
    
    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=4096
    )
    
    return response.choices[0].message.content


def extract_text_from_pdf(client, pdf_path, custom_prompt=None):
    # For PDFs, we can send them directly to the API
    base64_pdf = encode_image_to_base64(pdf_path)
    
    # Default OCR prompt for PDFs
    if custom_prompt is None:
        custom_prompt = """Extract all text from this scanned PDF document.
        Preserve the layout and formatting as much as possible.
        If there are multiple pages, clearly separate them.
        If there are tables, format them clearly.
        If there is no text, respond with 'No text found in document.'"""
    
    # Prepare the message
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": custom_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:application/pdf;base64,{base64_pdf}"
                    }
                }
            ]
        }
    ]
    
    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=4096
    )
    
    return response.choices[0].message.content


def save_output(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Output saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract text from images and scanned PDFs using OpenAI API'
    )
    parser.add_argument(
        'input_file',
        help='Path to the image or PDF file'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (optional, prints to console if not specified)'
    )
    parser.add_argument(
        '-k', '--api-key',
        help='OpenAI API key (or set OPENAI_API_KEY environment variable)'
    )
    parser.add_argument(
        '-p', '--prompt',
        help='Custom prompt for text extraction'
    )
    parser.add_argument(
        '-m', '--model',
        default='gpt-4o-mini',
        choices=['gpt-4o-mini', 'gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo'],
        help='OpenAI model to use (default: gpt-4o-mini)'
    )
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("Error: OpenAI API key not provided.")
        print("Set OPENAI_API_KEY environment variable or use -k flag.")
        return
    
    # Check if file exists
    if not os.path.exists(args.input_file):
        print(f"Error: File not found: {args.input_file}")
        return
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Determine file type and extract text
    file_extension = Path(args.input_file).suffix.lower()
    
    print(f"Processing: {args.input_file}")
    print(f"Using model: {args.model}")
    
    try:
        if file_extension == '.pdf':
            extracted_text = extract_text_from_pdf(
                client, 
                args.input_file, 
                args.prompt
            )
        elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            extracted_text = extract_text_from_image(
                client, 
                args.input_file, 
                args.prompt
            )
        else:
            print(f"Error: Unsupported file type: {file_extension}")
            print("Supported types: .jpg, .jpeg, .png, .gif, .webp, .pdf")
            return
        
        # Output results
        if args.output:
            save_output(extracted_text, args.output)
        else:
            print("\n" + "="*50)
            print("EXTRACTED TEXT:")
            print("="*50)
            print(extracted_text)
            print("="*50)
    
    except Exception as e:
        print(f"Error during OCR processing: {str(e)}")


if __name__ == "__main__":
    main()
