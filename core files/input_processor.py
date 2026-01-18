"""
Input Processor: Multi-Modal Input Handler

Converts diverse input types (text, images, documents) into a unified
representation ready for LLM processing. Maintains source attribution
for traceability.

Supported Formats:
    - Text: Direct string content
    - Images: PNG, JPG, JPEG, GIF, BMP (base64 encoded)
    - Documents: PDF, DOCX (text extraction)

Example:
    >>> processor = InputProcessor()
    >>> result = processor.process_inputs([
    ...     {"type": "text", "content": "Build a dashboard"},
    ...     {"type": "image", "path": "wireframe.png"}
    ... ])
    >>> result['modalities']
    ['text', 'image']
"""

import base64
from pathlib import Path
from typing import List, Dict, Any
from PIL import Image
import PyPDF2
import docx


class InputProcessor:
    """
    Processes different input modalities into unified format for LLM consumption.
    
    This class handles the preprocessing stage, converting all inputs into
    a structure containing text content and base64-encoded images. It maintains
    source attribution to enable multi-modal conflict detection.
    
    Attributes:
        supported_image_formats (set): File extensions for valid images
        supported_doc_formats (set): File extensions for valid documents
    
    Example:
        >>> processor = InputProcessor()
        >>> result = processor.process_inputs([
        ...     {"type": "text", "content": "Create a blog platform"},
        ...     {"type": "document", "path": "requirements.pdf"}
        ... ])
        >>> len(result['text_content'])
        2
        >>> result['text_content'][0]['source']
        'text'
    """
    
    def __init__(self):
        self.supported_image_formats = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
        self.supported_doc_formats = {'.pdf', '.docx'}
    
    def process_inputs(self, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process multiple inputs into unified representation for LLM.
        
        This method is the main entry point for converting diverse inputs
        into a standardized format. It maintains source attribution for each
        piece of content to enable conflict detection across modalities.
        
        Args:
            inputs (List[Dict[str, Any]]): List of input dictionaries, each with:
                - type (str): 'text', 'image', 'pdf', or 'document'
                - For 'text': 'content' (str) - the actual text string
                - For 'image': 'path' (str) - file path to image
                - For 'pdf'/'document': 'path' (str) - file path to document
            
            Examples of valid inputs:
                [{"type": "text", "content": "Build an app for..." }]
                [{"type": "image", "path": "mockup.png"}]
                [{"type": "pdf", "path": "requirements.pdf"}]
                [
                    {"type": "text", "content": "BookMyShow clone"},
                    {"type": "image", "path": "swiggy_ui.png"},
                    {"type": "document", "path": "smarthome.docx"}
                ]
        
        Returns:
            Dict[str, Any]: Processed inputs containing:
                - modalities (list): Unique list of input types used
                - text_content (list): Array of dicts with:
                    - source (str): 'text' or 'document'
                    - content (str): Extracted text
                - image_data (list): Array of dicts with:
                    - filename (str): Original filename
                    - base64 (str): Base64-encoded image
                    - mime_type (str): Image MIME type
                - notes (list): Processing notes or warnings
        
        Example:
            >>> processor = InputProcessor()
            >>> result = processor.process_inputs([
            ...     {"type": "text", "content": "E-commerce app"},
            ...     {"type": "image", "path": "design.png"}
            ... ])
            >>> result['modalities']
            ['text', 'image']
            >>> result['text_content'][0]['source']
            'text'
            >>> result['image_data'][0]['mime_type']
            'image/png'
        """
        processed = {
            'modalities': [],
            'text_content': [],
            'image_data': [],
            'notes': []
        }
        
        for inp in inputs:
            input_type = inp.get('type', '').lower()
            
            if input_type == 'text':
                text_content = self._process_text(inp.get('content', ''))
                processed['text_content'].append({
                    'source': 'text',
                    'content': text_content
                })
                processed['modalities'].append('text')
            
            elif input_type == 'image':
                image_data = self._process_image(inp.get('path'))
                if image_data:
                    processed['image_data'].append(image_data)
                    processed['modalities'].append('image')
            
            elif input_type in ['pdf', 'document']:
                doc_text = self._process_document(inp.get('path'))
                if doc_text:
                    processed['text_content'].append({
                        'source': 'document',
                        'content': doc_text
                    })
                    processed['modalities'].append('document')
        
        # Remove duplicates from modalities
        processed['modalities'] = list(set(processed['modalities']))
        
        return processed
    
    def _process_text(self, text: str) -> str:
        """Clean and normalize text input"""
        return text.strip()
    
    def _process_image(self, image_path: str) -> Dict[str, Any]:
        """
        Process image and prepare for vision API
        Returns dict with base64 encoded image
        """
        try:
            path = Path(image_path)
            if not path.exists():
                return None
            
            if path.suffix.lower() not in self.supported_image_formats:
                return None
            
            # Read and encode image
            with open(path, 'rb') as f:
                image_bytes = f.read()
            
            # Encode to base64
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Determine mime type
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.bmp': 'image/bmp'
            }
            mime_type = mime_types.get(path.suffix.lower(), 'image/jpeg')
            
            return {
                'filename': path.name,
                'base64': image_base64,
                'mime_type': mime_type
            }
        
        except Exception as e:
            print(f"Error processing image: {e}")
            return None
    
    def _process_document(self, doc_path: str) -> str:
        """Extract text from PDF or DOCX"""
        try:
            path = Path(doc_path)
            if not path.exists():
                return ""
            
            if path.suffix.lower() == '.pdf':
                return self._extract_pdf_text(path)
            elif path.suffix.lower() == '.docx':
                return self._extract_docx_text(path)
            else:
                return ""
        
        except Exception as e:
            print(f"Error processing document: {e}")
            return ""
    
    def _extract_pdf_text(self, pdf_path: Path) -> str:
        """Extract text from PDF"""
        try:
            text_parts = []
            with open(pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
            return "\n\n".join(text_parts)
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""
    
    def _extract_docx_text(self, docx_path: Path) -> str:
        """Extract text from DOCX"""
        try:
            doc = docx.Document(docx_path)
            text_parts = [para.text for para in doc.paragraphs if para.text.strip()]
            return "\n\n".join(text_parts)
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
            return ""
