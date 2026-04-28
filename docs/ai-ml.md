# AI / ML Tech Stack

## YOLOv8 / YOLOv11
- **Role**: Real-time object detection for surface defects
- **Targets**: Cracks, wormholes, scratches, dents, color deviation, paint defects, joint anomalies, suspected repairs
- **Output**: Defect class, bounding box, confidence, quantity, risk level

## PyTorch
- **Role**: Model training, validation, fine-tuning, experiment management
- Transfer learning from pretrained weights

## OpenCV
- **Role**: Image preprocessing and result annotation
- **Operations**: Cropping, augmentation, denoising, color space conversion, result drawing

## ONNX Runtime
- **Role**: Cross-platform inference deployment
- **Why**: Better deployment stability than raw PyTorch export

## SAM / CLIP (Future)
- **Role**: Semi-auto annotation, multimodal quality description, assisted retrieval

## Defect Classification System

| Category | Description |
|----------|-------------|
| Crack | Surface fissures |
| Wormhole | Insect damage holes |
| Scratch | Linear surface damage |
| Dent | Impact damage |
| Color Deviation | Inconsistent coloration |
| Paint Defect | Coating abnormality |
| Joint Anomaly | Uneven seams |
| Suspected Repair | Concealed patchwork |

## Model Evaluation Metrics

- Precision, Recall, mAP@0.5, mAP@0.5:0.95
- FPS, single-image inference latency
- False positive rate, miss rate

## Inference Pipeline

```
Image Upload → Validation → Preprocessing
                                    ↓
                            ONNX/YOLO Inference
                                    ↓
                         NMS + Post-processing
                                    ↓
                       Risk Scoring → Result Storage
                                    ↓
                        Annotated Image Generation
```

## Risk Scoring

Combines rule engine + model confidence:

| Dimension | Weight Factor |
|-----------|--------------|
| Defect category weight | Per-class severity |
| Defect count | Quantity |
| Defect area | Coverage |
| Defect location | Position sensitivity |
| Model confidence | Detection reliability |
| Historical comparison | Delta from baseline |
