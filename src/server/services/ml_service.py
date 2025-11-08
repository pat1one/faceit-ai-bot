import torch
import torchvision.transforms as transforms
from PIL import Image
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        self._model = None
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    @property
    def model(self):
        if self._model is None:
            try:
                self._model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
                self._model.eval()
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                raise HTTPException(status_code=500, detail="Failed to load ML model")
        return self._model

    async def analyze_image(self, image):
        try:
            input_tensor = self.transform(image).unsqueeze(0)
            output = self.model(input_tensor)
            _, predicted = output.max(1)
            return {
                "prediction": predicted.item(),
                "confidence": output.softmax(1).max().item(),
            }
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            raise HTTPException(status_code=500, detail="Error analyzing image")

ml_service = MLService()