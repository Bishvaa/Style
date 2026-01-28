from rembg import remove, new_session
from PIL import Image
import io

# Load model once at startup
umbg_session = new_session("u2netp")

def process_image_background(input_path, output_path):
    """
    Reads image from input_path, removes background, saves to output_path.
    Optimized: Resizes large images & reuses model session.
    """
    try:
        with open(input_path, 'rb') as i:
            input_data = i.read()
            
        # Resize logic using PIL to reduce processing time
        # We process in memory before sending to rembg
        img = Image.open(io.BytesIO(input_data))
        
        # Max dimension 800px is usually enough for web display and much faster
        max_size = 800
        if max(img.size) > max_size:
            img.thumbnail((max_size, max_size))
            
            # Save resized image to bytes for rembg
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            input_data = buf.getvalue()

        # Use cached session
        output_data = remove(input_data, session=umbg_session)
        
        with open(output_path, 'wb') as o:
            o.write(output_data)
            
        return True
    except Exception as e:
        print(f"Error removing background: {e}")
        return False
