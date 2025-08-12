import mcp.types as types
import os
import json
import logging
from pathlib import Path

# Set up logging
logger = logging.getLogger(__name__)

def problem_imports():
    """Handle problematic imports for PyMuPDF."""
    try:
        import fitz  # PyMuPDF
        logger.info("PyMuPDF (fitz) imported successfully")
    except ImportError as e:
        logger.error(f"Failed to import PyMuPDF (fitz): {e}")
        logger.error("Please install PyMuPDF: pip install PyMuPDF")
        raise

async def tool_info() -> dict:
    """Returns information about the lng_pdf_extract_images tool."""
    return {
        "description": """Extracts all images from PDF files and saves them as PNG files with maximum quality.

**Parameters:**
- `pdf_path` (string, required): Absolute path to the PDF file.
- `output_directory` (string, optional): Directory to save extracted images. Default: same directory as PDF.
- `image_prefix` (string, optional): Prefix for image filenames. Default: "image".

**Output Behavior:**
- Extracts ALL images from the specified PDF file
- Saves images in PNG format with maximum quality and original resolution
- Names images sequentially: image1.png, image2.png, image3.png, etc.
- Saves images in the same directory as the source PDF file (unless output_directory specified)

**Example Usage:**
- Extract all images: `{"pdf_path": "/path/to/document.pdf"}`
- Custom output directory: `{"pdf_path": "/path/to/document.pdf", "output_directory": "/path/to/images"}`
- Custom prefix: `{"pdf_path": "/path/to/document.pdf", "image_prefix": "page"}`

**Returns:**
- List of extracted image file paths
- Total count of extracted images
- Success/error status with detailed information

**Error Handling:**
- Password-protected PDFs: Returns detailed error information and fails gracefully
- Corrupted PDFs: Returns detailed error information and fails gracefully
- Missing files: Returns appropriate error message

This tool uses PyMuPDF for robust PDF processing and image extraction.""",
        "schema": {
            "type": "object",
            "properties": {
                "pdf_path": {
                    "type": "string",
                    "description": "Absolute path to the PDF file"
                },
                "output_directory": {
                    "type": "string",
                    "description": "Directory to save extracted images (default: same directory as PDF)"
                },
                "image_prefix": {
                    "type": "string",
                    "description": "Prefix for image filenames (default: 'image')",
                    "default": "image"
                }
            },
            "required": ["pdf_path"]
        }
    }

async def run_tool(name: str, parameters: dict) -> list[types.Content]:
    """Extracts all images from PDF files and saves them as PNG files."""
    try:
        # Import PyMuPDF
        try:
            import fitz  # PyMuPDF
        except ImportError:
            error_metadata = {
                "operation": "pdf_extract_images",
                "success": False,
                "error": "PyMuPDF library not available. Please install with: pip install PyMuPDF"
            }
            result = json.dumps({"metadata": error_metadata}, indent=2)
            return [types.TextContent(type="text", text=result)]

        # Extract parameters
        pdf_path = parameters.get("pdf_path", "")
        output_directory = parameters.get("output_directory")
        image_prefix = parameters.get("image_prefix", "image")
        
        if not pdf_path:
            error_metadata = {
                "operation": "pdf_extract_images",
                "success": False,
                "error": "pdf_path parameter is required"
            }
            result = json.dumps({"metadata": error_metadata}, indent=2)
            return [types.TextContent(type="text", text=result)]
        
        # Convert to absolute path if needed
        if not os.path.isabs(pdf_path):
            pdf_path = os.path.abspath(pdf_path)
        
        # Check if PDF file exists
        if not os.path.exists(pdf_path):
            error_metadata = {
                "operation": "pdf_extract_images",
                "pdf_path": pdf_path,
                "success": False,
                "error": f"PDF file not found: {pdf_path}"
            }
            result = json.dumps({"metadata": error_metadata}, indent=2)
            return [types.TextContent(type="text", text=result)]
        
        # Check if it's a file (not directory)
        if not os.path.isfile(pdf_path):
            error_metadata = {
                "operation": "pdf_extract_images",
                "pdf_path": pdf_path,
                "success": False,
                "error": f"Path is not a file: {pdf_path}"
            }
            result = json.dumps({"metadata": error_metadata}, indent=2)
            return [types.TextContent(type="text", text=result)]

        # Determine output directory
        if output_directory is None:
            output_directory = os.path.dirname(pdf_path)
        else:
            if not os.path.isabs(output_directory):
                output_directory = os.path.abspath(output_directory)
        
        # Create output directory if it doesn't exist
        try:
            os.makedirs(output_directory, exist_ok=True)
        except Exception as e:
            error_metadata = {
                "operation": "pdf_extract_images",
                "pdf_path": pdf_path,
                "output_directory": output_directory,
                "success": False,
                "error": f"Failed to create output directory: {str(e)}"
            }
            result = json.dumps({"metadata": error_metadata}, indent=2)
            return [types.TextContent(type="text", text=result)]

        # Open PDF file
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            error_str = str(e).lower()
            if "password" in error_str or "decrypt" in error_str or "authentication" in error_str:
                error_metadata = {
                    "operation": "pdf_extract_images",
                    "pdf_path": pdf_path,
                    "success": False,
                    "error": f"PDF is password-protected or encrypted: {str(e)}",
                    "error_type": "password_protected"
                }
            elif "corrupt" in error_str or "damaged" in error_str or "invalid" in error_str:
                error_metadata = {
                    "operation": "pdf_extract_images",
                    "pdf_path": pdf_path,
                    "success": False,
                    "error": f"PDF file appears to be corrupted or damaged: {str(e)}",
                    "error_type": "corrupted"
                }
            else:
                error_metadata = {
                    "operation": "pdf_extract_images",
                    "pdf_path": pdf_path,
                    "success": False,
                    "error": f"Failed to open PDF: {str(e)}",
                    "error_type": "unknown"
                }
            result = json.dumps({"metadata": error_metadata}, indent=2)
            return [types.TextContent(type="text", text=result)]

        # Check if PDF has any pages
        if len(doc) == 0:
            doc.close()
            error_metadata = {
                "operation": "pdf_extract_images",
                "pdf_path": pdf_path,
                "success": False,
                "error": "PDF file contains no pages"
            }
            result = json.dumps({"metadata": error_metadata}, indent=2)
            return [types.TextContent(type="text", text=result)]

        # Extract images
        extracted_images = []
        image_count = 0
        total_pages = len(doc)
        
        try:
            for page_num in range(total_pages):
                page = doc.load_page(page_num)
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    try:
                        # Get image data
                        xref = img[0]  # xref number
                        pix = fitz.Pixmap(doc, xref)
                        
                        # Skip if image has alpha channel (convert to RGB)
                        if pix.alpha:
                            pix = fitz.Pixmap(fitz.csRGB, pix)
                        
                        # Generate filename
                        image_count += 1
                        image_filename = f"{image_prefix}{image_count}.png"
                        image_path = os.path.join(output_directory, image_filename)
                        
                        # Save image as PNG with maximum quality
                        pix.save(image_path)
                        extracted_images.append(image_path)
                        
                        # Clean up
                        pix = None
                        
                    except Exception as e:
                        logger.warning(f"Failed to extract image {img_index} from page {page_num}: {str(e)}")
                        continue
            
            doc.close()
            
            # Prepare result
            metadata = {
                "operation": "pdf_extract_images",
                "pdf_path": pdf_path,
                "output_directory": output_directory,
                "image_prefix": image_prefix,
                "total_pages": total_pages,
                "images_extracted": len(extracted_images),
                "success": True
            }
            
            result = {
                "extracted_images": extracted_images,
                "metadata": metadata
            }
            
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
        except Exception as e:
            doc.close()
            error_metadata = {
                "operation": "pdf_extract_images",
                "pdf_path": pdf_path,
                "success": False,
                "error": f"Error during image extraction: {str(e)}"
            }
            result = json.dumps({"metadata": error_metadata}, indent=2)
            return [types.TextContent(type="text", text=result)]
        
    except Exception as e:
        error_metadata = {
            "operation": "pdf_extract_images",
            "success": False,
            "error": str(e)
        }
        result = json.dumps({"metadata": error_metadata}, indent=2)
        return [types.TextContent(type="text", text=result)]