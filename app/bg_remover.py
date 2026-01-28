from rembg import remove, new_session

def process_image_background(input_path, output_path):
    """
    Reads image from input_path, removes background, saves to output_path.
    """
    try:
        with open(input_path, 'rb') as i:
            input_data = i.read()
            
        # Use 'u2netp' (Lightweight model) for Render Free Tier compatibility
        # Default u2net is 170MB+ and crashes 512MB instances.
        session = new_session("u2netp")
        output_data = remove(input_data, session=session)
        
        with open(output_path, 'wb') as o:
            o.write(output_data)
            
        return True
    except Exception as e:
        print(f"Error removing background: {e}")
        return False
