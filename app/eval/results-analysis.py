import os
import json
import numpy as np
import matplotlib.pyplot as plt


eval_dir = "../../results"
output_dir = "plots/"

os.makedirs(output_dir, exist_ok=True)

models = ["Llama3", "Mistral", "Qwen2"]
prompts = ["Z1", "Z2", "Z3"]


def load_eval_data(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def calculate_average_scores(data):
    general_scores = []
    alignment_scores = []
    coverage_scores = []

    for item in data:
        general_scores.append(item["score"])
        alignment_scores.append(item["score_breakdown:"]["Alignment"])
        coverage_scores.append(item["score_breakdown:"]["Coverage"])

    avg_general = np.mean(general_scores)
    avg_alignment = np.mean(alignment_scores)
    avg_coverage = np.mean(coverage_scores)

    return avg_general, avg_alignment, avg_coverage


### average general score, average alignment score, and average coverage score for each model and for each prompt

def plot_scores(scores, title, ylabel, model_name, prompt_labels, filename):
    fig, ax = plt.subplots()

    width = 0.4
    bars = ax.bar(prompt_labels, scores, color=["skyblue", "yellowgreen", "gold"], width=width)

    ax.set_title(f"{model_name} - {title}")
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, 1.0)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2),
                ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()


model_scores = {model: {"general": [], "alignment": [], "coverage": []} for model in models}

# to be used later
optimal_scores = {}
optimal_prompts = {}
best_prompt = None
best_general_score = -1

for model in models:

    for prompt in prompts:
        file_name = f"data_{model}-{prompt}_eval.json"
        file_path = os.path.join(eval_dir, file_name)

        eval_data = load_eval_data(file_path)

        avg_general, avg_alignment, avg_coverage = calculate_average_scores(eval_data)

        model_scores[model]["general"].append(avg_general)
        model_scores[model]["alignment"].append(avg_alignment)
        model_scores[model]["coverage"].append(avg_coverage)

        if avg_general > best_general_score:
            best_general_score = avg_general
            best_model = model
            best_prompt = prompt
            optimal_scores[model] = {
                'General': avg_general,
                'Alignment': avg_alignment,
                'Coverage': avg_coverage
            }
            optimal_prompts[model] = prompt


for model in models:
    plot_scores(
        model_scores[model]['general'],
        'Average General Score per Prompt Type',
        'Average General Score',
        model,
        prompts,
        f'{model}_general_scores.png'
    )


for model in models:
    plot_scores(
        model_scores[model]["alignment"],
        "Average Alignment Score per Prompt Type",
        "Average Alignment Score",
        model,
        prompts,
        f"{model}_alignment_scores.png"
    )


for model in models:
    plot_scores(
        model_scores[model]["coverage"],
        "Average Coverage Score per Prompt Type",
        "Average Coverage Score",
        model,
        prompts,
        f"{model}_coverage_scores.png"
    )


### average general score, average alignment score, and average coverage score for each model across prompt types

def plot_model_comparison(scores, title, ylabel, filename, model_labels):
    fig, ax = plt.subplots()

    width = 0.4
    bars = ax.bar(model_labels, scores, color=["thistle", "lightsalmon", "lightsteelblue"], width=width)

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, 1.0)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2),
                ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()


overall_scores = {
    model: {
        "general": np.mean(model_scores[model]["general"]),
        "alignment": np.mean(model_scores[model]["alignment"]),
        "coverage": np.mean(model_scores[model]["coverage"])
    }
    for model in models
}


avg_general_scores = [overall_scores[model]["general"] for model in models]
avg_alignment_scores = [overall_scores[model]["alignment"] for model in models]
avg_coverage_scores = [overall_scores[model]["coverage"] for model in models]


plot_model_comparison(
    avg_general_scores,
    "Average General Score Comparison",
    "Average General Score",
    "general_score_comparison.png",
    models
)


plot_model_comparison(
    avg_alignment_scores,
    "Average Alignment Score Comparison",
    "Average Alignment Score",
    "alignment_score_comparison.png",
    models
)


plot_model_comparison(
    avg_coverage_scores,
    "Average Coverage Score Comparison",
    "Average Coverage Score",
    "coverage_score_comparison.png",
    models
)


### finding and plotting the optimal model-prompt type combination

def plot_optimal_comparison(optimal_scores, title, filename, model_labels, prompt_labels):
    fig, ax = plt.subplots()

    categories = ["General", "Alignment", "Coverage"]
    bar_width = 0.2

    index = np.arange(len(categories))
    for i, model in enumerate(model_labels):
        scores = [optimal_scores[model][cat] for cat in categories]
        label_with_prompt = f"{model} ({prompt_labels[model]})"
        ax.bar(index + i * bar_width, scores, width=bar_width, label=label_with_prompt)

    ax.set_title(title)
    ax.set_ylabel("Scores")
    ax.set_ylim(0, 1.0)
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(categories)
    ax.legend()

    for i, model in enumerate(model_labels):
        scores = [optimal_scores[model][cat] for cat in categories]
        for j, score in enumerate(scores):
            ax.text(index[j] + i * bar_width, score + 0.02, round(score, 2), ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()


plot_optimal_comparison(
    optimal_scores,
    "Optimal Model-Prompt Combination Comparison",
    "optimal_model_prompt_comparison.png",
    models,
    optimal_prompts
)


### compare optimal model-prompt type combinations against human-generated summaries

human_eval_file = "data_Zusammenfassung_eval.json"
human_data = load_eval_data(os.path.join(eval_dir, human_eval_file))

avg_human_general, avg_human_alignment, avg_human_coverage = calculate_average_scores(human_data)


def plot_optimal_vs_human(optimal_scores, human_scores, title, filename, model_labels, prompt_labels):
    fig, ax = plt.subplots()

    categories = ["General", "Alignment", "Coverage"]
    bar_width = 0.25

    index = np.arange(len(categories))
    for i, model in enumerate(model_labels):
        scores = [optimal_scores[model][cat] for cat in categories]
        label_with_prompt = f"{model} ({prompt_labels[model]})"
        ax.bar(index + i * bar_width, scores, width=bar_width, label=label_with_prompt)

    human_label = "Human Summaries"
    human_scores_list = [human_scores[cat] for cat in categories]
    ax.bar(index + len(model_labels) * bar_width, human_scores_list, width=bar_width, label=human_label, color="gray")

    ax.set_title(title)
    ax.set_ylabel("Scores")
    ax.set_ylim(0, 1.0)
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(categories)
    ax.legend()

    for i, model in enumerate(model_labels):
        scores = [optimal_scores[model][cat] for cat in categories]
        for j, score in enumerate(scores):
            ax.text(index[j] + i * bar_width, score + 0.02, round(score, 2), ha="center", va="bottom")

    for j, score in enumerate(human_scores_list):
        ax.text(index[j] + len(model_labels) * bar_width, score + 0.02, round(score, 2), ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()


human_scores = {
    "General": avg_human_general,
    "Alignment": avg_human_alignment,
    "Coverage": avg_human_coverage
}


plot_optimal_vs_human(
    optimal_scores,
    human_scores,
    "Optimal Model-Prompt Combination vs Human Summaries",
    "optimal_vs_human_comparison.png",
    models,
    optimal_prompts
)
