import io, json, os, random, string
from datetime import datetime
import numpy as np
from PIL import Image
import pydicom

import torch

from monai.transforms import Compose, Resize, NormalizeIntensity

from flask import Flask, Blueprint, jsonify, request

from boneage import db, UPLOAD_DIR
from boneage.models import BoneAge
from .model import get_prediction

bp_api = Blueprint('api', __name__, url_prefix='/boneage/api')

@bp_api.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        now_datetime = datetime.now()
        
        try:
            timage = request.files['image'].read()
            ds = pydicom.dcmread(io.BytesIO(timage), force=True)
            gender = 1 if 'f' in ds['PatientSex'].value.lower() else 0
        except:
            return "CANNOT LOAD DICOM PROPERLY", 400

        _tfm = Compose([
            Resize(spatial_size=(512, 512), mode='bilinear'),
            NormalizeIntensity(subtrahend=0, divisor=4095),
        ])
        
        ximage = np.expand_dims(ds.pixel_array, axis=0)
        ximage = _tfm(ximage).unsqueeze(0).numpy()
        xtable = np.array([[gender]]).astype('int64')

        try:
            ty = get_prediction(ximage, xtable)
        except:
            return "PREDICTION WENT WRONG", 400
        ty = torch.softmax(torch.tensor(ty), 1)[0].numpy()
        
        mx = ximage[0,0].astype(np.float16)

        preds = {
            'preds': ty.tolist(), 'gender': gender, 
            # 'image': mx.tolist(),
        }
        predict_datetime = datetime.now()

        ## add to DB
        db_gender = 'F' if gender == 1 else 'M'
        
        uid = ds.get('SOPInstanceUID') or ""
        pid = ds.get('PatientID') or ""
        stid = ds.get('StudyInstanceUID') or ""
        srid = ds.get('SeriesInstanceUID') or ""
        db_preds = json.dumps(ty.tolist())

        dtformat = '%Y%m%d%H%M%S'
        study_datetime = ds.get('StudyDate') + ds.get('StudyTime')
        study_datetime = datetime.strptime(study_datetime[:14], dtformat)
        instance_datetime = ds.get('AcquisitionDate') + ds.get('AcquisitionTime')
        instance_datetime = datetime.strptime(instance_datetime[:14], dtformat)

        db_dob = ds.get('PatientBirthDate')
        db_dob = datetime.strptime(db_dob[:8], '%Y%m%d')
        db_age = round((study_datetime - db_dob).days / 365.2425, 2)

        # save image
        h, w = ds.pixel_array.shape
        nw = 512
        nh = int(h/w*nw + 0.5)
        thimg = ds.pixel_array / np.max(ds.pixel_array)
        thimg = Image.fromarray((255*thimg).astype('uint8'))
        thimg = thimg.resize((nw, nh))
        thname = now_datetime.strftime("%Y%m%d_%H%M%S") + '_' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8)) + '.jpg'
        thpath = os.path.join(UPLOAD_DIR, thname)
        thimg.save(thpath)

        a = BoneAge(gender=db_gender, age=db_age, pid=pid, study_datetime=study_datetime, predictions=db_preds, instance_datetime=instance_datetime, instance_id=uid, series_id=srid, study_id=stid, path_image=thpath, create_date=now_datetime, create_predictions_date=predict_datetime)
        db.session.add(a)
        db.session.commit()

        return jsonify(preds)
    
@bp_api.route('/dummy', methods=['POST'])
def dummy():
    if request.method == 'POST':
        cstr = os.path.dirname(os.path.abspath(__file__))
        cstr1 = os.getcwd()
        print(cstr)
        print(cstr1)
        return 'dummy'