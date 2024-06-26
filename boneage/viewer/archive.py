import io, json, os, random, string
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objs as go

from flask import Flask, Blueprint, jsonify, request, render_template

from boneage import TEMPLATE_DIR, STATIC_DIR
from boneage.models import BoneAge
from boneage.utils.label import BoneAgeLabelText, get_boneage_labeltext

#@bp_viewer.route("/show/q", methods=["GET"])
def show_q():
    query_id = request.args.get("menu_id")
    if query_id:
        # single query
        qi = BoneAge.query.get_or_404(query_id)

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
        path_image = path_image.split(STATIC_DIR)[1].lstrip(os.sep)

        idata["path_image"] = path_image

        # Plotly bar chart
        # plot_div = create_BA_plot(ipreds, gender=idata["Gender"])

        plot_div = {}
        jpreds = getattr(qi, "predictions")
        ipreds = json.loads(jpreds)
        ipreds = np.array(ipreds)
        ixlbls = np.arange(len(ipreds)).tolist()
        jxlbls = json.dumps(ixlbls)

        plot_div["predictions"] = jpreds
        plot_div["xlabels"] = jxlbls

        return render_template("content_q.html", content=idata, plot_div=plot_div)
    return "Invalid query ID.", 400


def create_BA_plot(numbers, gender="M"):
    from boneage.utils.label import get_boneage_labeltext

    bfemale = gender == "F"

    # xlabels =

    # Create a Plotly bar chart
    fig = go.Figure(data=[go.Bar(x=np.arange(len(numbers)), y=numbers)])
    fig.update_layout(title="Bar Chart", xaxis_title="Category", yaxis_title="Value")

    # Add custom JavaScript code for click events on bars
    fig.update_traces(
        marker=dict(color="rgba(50, 171, 96, 0.6)"), selector=dict(type="bar")
    )
    fig.update_layout(
        clickmode="event+select",
        annotations=[
            dict(text="", x=xi, y=yi, showarrow=True, arrowhead=1, ax=0, ay=-40)
            for xi, yi in zip(["A", "B", "C", "D"], numbers)
        ],
    )

    return fig.to_html(full_html=False, include_plotlyjs="cdn")
