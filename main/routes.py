from flask import render_template
from flask_login import current_user, login_required
from flask import Blueprint, render_template
from ml.service import get_perceptron_results


from . import main_bp

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', current_user=current_user)
@main_bp.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    ml_results = get_perceptron_results()

    recent_activity = [
        {
            "title": "Model training",
            "description": "Result: Completed",
            "time": "Just now",
            "type": "training",
            "status": "success"
        },
        {
            "title": "Perceptron accuracy",
            "description": f'Result: {ml_results["accuracy"]:.1f}%',
            "time": "Just now",
            "type": "analysis",
            "status": "success"
        }
    ]

    return render_template(
        "dashboard.html",

        # top cards
        total_predictions=len(ml_results["comparison"]),
        total_predictions_change="+10%",
        model_accuracy=ml_results["accuracy"] * 100,
        model_accuracy_change="+2.1%",
        models_trained=1,
        last_active="Today",

        # dataset info card
        training_samples=891,
        test_samples=418,
        survival_rate=38.4,

        # activity panel
        recent_activity=recent_activity,

        # perceptron results for use anywhere in the template
        confusion_matrix=ml_results["confusion_matrix"],
        epoch_errors=ml_results["epoch_errors"],
        comparison=ml_results["comparison"]
    )

@main_bp.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', current_user=current_user)


