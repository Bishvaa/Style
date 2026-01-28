from rembg import remove
import io

def process_image_background(input_path, output_path):
    """
    Reads image from input_path, removes background, saves to output_path.
    """
    try:
        with open(input_path, 'rb') as i:
            input_data = i.read()
            
        output_data = remove(input_data)
        
        with open(output_path, 'wb') as o:
            o.write(output_data)
            
        return True
    except Exception as e:
        print(f"Error removing background: {e}")
        return False
