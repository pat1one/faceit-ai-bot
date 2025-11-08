from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import logging
from ..services.ml_service import ml_service

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/analyze-demo")
async def analyze_demo(demo: UploadFile = File(...)):
    """
    Анализ демки CS2 с использованием модели машинного обучения

    Args:
        demo: Файл демки (.dem)

    Returns:
        dict: Результаты анализа
    
    Raises:
        HTTPException: При ошибке в обработке файла или анализе
    """
    if not demo or not demo.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if not demo.filename.endswith('.dem'):
        raise HTTPException(status_code=400, detail="Invalid file format. Only .dem files are supported")

    try:
        image = Image.open(demo.file)
        analysis_result = await ml_service.analyze_image(image)
        return {
            "filename": demo.filename,
            **analysis_result
        }
    except Exception as e:
        logger.error(f"Error analyzing demo: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing demo file")