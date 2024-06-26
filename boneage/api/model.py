import os, glob
import onnxruntime

model_basebase = os.path.dirname(os.path.abspath(__file__))
model_base = os.path.join(model_basebase, 'onnx')
model_name = '2024-06-18_09-55-03__best_f1'
model_path = os.path.join(model_base, model_name, 'model.onnx')

ort_session = onnxruntime.InferenceSession(model_path)

def get_prediction(x1, x2):
    input1_name = ort_session.get_inputs()[0].name
    input2_name = ort_session.get_inputs()[1].name
    ort_inputs = {input1_name: x1, input2_name: x2}
    ort_outs = ort_session.run(None, ort_inputs)
    return ort_outs[0]
