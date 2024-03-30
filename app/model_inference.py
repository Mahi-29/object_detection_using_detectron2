
import cv2
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from detectron2.utils.logger import setup_logger
import traceback
setup_logger()

class Detection:

    def __init__(self, base_path) -> None:
        self.image_base_path = base_path
        self.image_width = 500
        self.image_height = 500
        self.cfg = get_cfg()
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_C4_1x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_C4_1x.yaml")
        self.predictor = DefaultPredictor(self.cfg)

    def preprocessing_image(self, image):
        print("inside_preprocessing")
        resized_image = cv2.resize(image, (self.image_width, self.image_height))
        return resized_image


    def inference(self, image_path):
        try:
            image = cv2.imread(image_path)
            print("inside_inference")
            preprocessed_image = self.preprocessing_image(image)
        except:
            traceback.print_exc()
            return False
        
        try:
            outputs  = self.predictor(preprocessed_image)
            print(outputs["instances"].pred_classes)
            print(outputs["instances"].pred_boxes)
            v = Visualizer(preprocessed_image[:, :, ::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.2)
            out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
            cv2.imwrite(self.image_base_path,out.get_image()[:, :, ::-1])
            return True
        except:
            traceback.print_exc
            return False
