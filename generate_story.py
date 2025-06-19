import os
import cv2
import insightface
from glob import glob

face_analyzer = None
face_swapper = None

def init_models():
    global face_analyzer, face_swapper
    if face_analyzer is None:
        face_analyzer = insightface.app.FaceAnalysis(name='buffalo_l')
        face_analyzer.prepare(ctx_id=0, det_size=(640, 640))
    if face_swapper is None:
        face_swapper = insightface.model_zoo.get_model('models/inswapper_128.onnx')
    return face_analyzer, face_swapper

def generate_story(child_image_path, template_dir='templates', output_dir='output'):
    os.makedirs(output_dir, exist_ok=True)
    analyzer, swapper = init_models()

    # Load child image
    child_img = cv2.imread(child_image_path)
    child_faces = analyzer.get(child_img)
    if not child_faces:
        raise ValueError("No face detected in uploaded child image.")

    child_face = child_faces[0]

    # Loop through templates
    template_paths = sorted(glob(os.path.join(template_dir, 'page*.png')))

    swapped_pages = []
    for template_path in template_paths:
        template_img = cv2.imread(template_path)
        detected_faces = analyzer.get(template_img)

        if not detected_faces:
            print(f"⚠️ No face detected in: {template_path}")
            continue

        # Swap face onto first detected face in template
        swapped_img = swapper.get(template_img, detected_faces[0], child_face)

        output_path = os.path.join(output_dir, os.path.basename(template_path))
        cv2.imwrite(output_path, swapped_img)
        swapped_pages.append(output_path)

    return swapped_pages

