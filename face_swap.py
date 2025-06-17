import insightface
import cv2
import os

# Load the face detection model
app = insightface.app.FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0, det_size=(640, 640))

# Load InSwapper model
swapper = insightface.model_zoo.get_model('models/inswapper_128.onnx', download=False)

def swap_face(template_path, child_image_path, output_path):
    """
    Swap the face in the template image with the child face. If no face is detected in the template,
    the original template image is saved as-is.
    Args:
        template_path (str): Path to the story template image.
        child_image_path (str): Path to the uploaded child image.
        output_path (str): Path to save the swapped or fallback output image.
    """
    # Load images
    template_img = cv2.imread(template_path)
    child_img = cv2.imread(child_image_path)

    if template_img is None or child_img is None:
        print(f"[❌] Could not load image: {template_path} or {child_image_path}")
        return

    # Detect faces
    template_faces = app.get(template_img)
    child_faces = app.get(child_img)

    if len(template_faces) == 0:
        print(f"[⚠️] No face found in template: {template_path}, passing template as-is.")
        cv2.imwrite(output_path, template_img)
        return
    if len(child_faces) == 0:
        print(f"[⚠️] No face found in child image.")
        return

    try:
        swapped = swapper.get(template_img, template_faces[0], child_faces[0], paste_back=True)
        cv2.imwrite(output_path, swapped)
        print(f"[✅] Face swapped and saved to: {output_path}")
    except Exception as e:
        print(f"[❌] Error swapping face in {template_path}: {e}")
        cv2.imwrite(output_path, template_img)
