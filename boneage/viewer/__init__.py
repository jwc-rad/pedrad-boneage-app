import glob, io, json, os, random, string
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objs as go

from flask import Flask, Blueprint, jsonify, request, render_template, send_from_directory, abort

from boneage import db, TEMPLATE_DIR, STATIC_DIR, UPLOAD_DIR
from boneage.models import BoneAge
from boneage.utils.label import BoneAgeLabelText, get_boneage_labeltext

bp_viewer = Blueprint(
    "viewer",
    __name__,
    url_prefix="/boneage/viewer",
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
)

USE_HAND_REF_HE = True

def parse_boneage_query(q=None):
    cols = ["ID", "Action", "PatientID", "Gender", "Age", "StudyDateTime", "CreateDateTime", "Status"]
    
    if q is None:
        return cols
    else:
        dfdata = {}
        dfdata[cols[0]] = getattr(q, "id")
        dfdata[cols[1]] = ""
        dfdata[cols[2]] = getattr(q, "pid")
        dfdata[cols[3]] = getattr(q, "gender")
        dfdata[cols[4]] = getattr(q, "age")
        study_datetime = getattr(q, "study_datetime")
        study_datetime = study_datetime.strftime("%Y-%m-%d %H:%M:%S")
        dfdata[cols[5]] = study_datetime
        create_datetime = getattr(q, "create_date")
        create_datetime = create_datetime.strftime("%Y-%m-%d %H:%M:%S")
        dfdata[cols[6]] = create_datetime
        dfdata[cols[7]] = getattr(q, "status")
        return dfdata


@bp_viewer.route("/")
def viewer():
    qs = BoneAge.query.all()

    data = [parse_boneage_query(q) for q in qs]

    dcols = parse_boneage_query()

    ref_images = {}
    ref_images["F"] = [
        str(Path(x).as_posix()).split(STATIC_DIR)[1].lstrip("/")
        for x in sorted(glob.glob(os.path.join(STATIC_DIR, f"images/{'hand_he' if USE_HAND_REF_HE else 'hand'}/F", "*.png")))
    ]
    ref_images["M"] = [
        str(Path(x).as_posix()).split(STATIC_DIR)[1].lstrip("/")
        for x in sorted(glob.glob(os.path.join(STATIC_DIR, f"images/{'hand_he' if USE_HAND_REF_HE else 'hand'}/M", "*.png")))
    ]

    return render_template("index.html", data=data, dcols=dcols, ref_images=ref_images)


@bp_viewer.route("/reload_data", methods=["GET"])
def reload_data():
    try:
        qs = BoneAge.query.all()

        data = [parse_boneage_query(q) for q in qs]

        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)})


def parse_boneage_data(qi):
    idata = {}
    idata["ID"] = getattr(qi, "id")
    idata["PatientID"] = getattr(qi, "pid")
    idata["Gender"] = getattr(qi, "gender")
    idata["Age"] = getattr(qi, "age")
    study_datetime = getattr(qi, "study_datetime")
    study_datetime = study_datetime.strftime("%Y-%m-%d %H:%M:%S")
    idata["StudyDateTime"] = study_datetime
    create_datetime = getattr(qi, "create_date")
    create_datetime = create_datetime.strftime("%Y-%m-%d %H:%M:%S")
    idata["CreateDateTime"] = create_datetime

    path_image = getattr(qi, "path_image")
    path_image = path_image.split(UPLOAD_DIR)[1].lstrip("/")
    idata["path_image"] = path_image

    bfem = idata["Gender"] == "F"
    alllabeltext = (
        list(BoneAgeLabelText.dict_female.values())
        if bfem
        else list(BoneAgeLabelText.dict_male.values())
    )

    jpreds = getattr(qi, "predictions")
    ipreds = json.loads(jpreds)
    ipreds = np.array(ipreds)
    ibest = int(ipreds.argmax())

    ixtick = np.arange(len(ipreds))
    ixlbls = np.array([get_boneage_labeltext(x, bfem, text=False) for x in ixtick])
    ixlbls = np.round(ixlbls / 12, 1)
    # ixlbls = np.array([f'{x}Y' for x in ixlbls])

    jypred = ipreds.tolist()
    jxtick = ixtick.tolist()
    jxlbls = ixlbls.tolist()

    idata["predictions"] = jypred
    idata["best_pred"] = ibest
    idata["xticks"] = jxtick
    idata["xlabels"] = jxlbls
    idata["alllabeltext"] = alllabeltext

    return idata


@bp_viewer.route("/get_data", methods=["POST"])
def get_data():
    query_id = request.json["query_id"]
    qi = BoneAge.query.get_or_404(query_id)
    idata = parse_boneage_data(qi)
    return jsonify(data=idata)

@bp_viewer.route("/uploads/<filename>", methods=["GET"])
def get_uploaded_filepath(filename):
    return send_from_directory(UPLOAD_DIR, filename)

@bp_viewer.route("/delete_record", methods=["POST"])
def delete_record():
    query_id = request.json["query_id"]
    try:
        qi = BoneAge.query.get_or_404(query_id)
        if qi:
            db.session.delete(qi)
            db.session.commit()
            return jsonify({"message": "Record deleted successfully"}), 200
        else:
            return jsonify({"error": "Record not found"}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting record: {e}")
        return jsonify({"error": str(e)}), 500


@bp_viewer.route("/delete_all_record", methods=["POST"])
def delete_all_record():
    qs = BoneAge.query.all()

    for qi in qs:
        try:
            db.session.delete(qi)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting record: {e}")

    qs = BoneAge.query.all()

    return (
        jsonify(
            {
                "message": f"Records deleted successfully ... {len(qs)} records present",
                "num_records": len(qs),
            }
        ),
        200,
    )


@bp_viewer.route("/toggle_status", methods=["POST"])
def toggle_status():
    query_id = request.json["query_id"]
    try:
        qi = BoneAge.query.get_or_404(query_id)
        if qi:
            tmp_status = getattr(qi, "status")
            if tmp_status == "Wait":
                new_status = "Confirm"
            elif tmp_status == "Confirm":
                new_status = "Wait"
            else:
                new_status = tmp_status
            setattr(qi, "status", new_status)
            db.session.commit()
            return jsonify({"old_status": tmp_status, "new_status": new_status}), 200
        else:
            return jsonify({"error": "Record not found"}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error changing status: {e}")
        return jsonify({"error": str(e)}), 500
