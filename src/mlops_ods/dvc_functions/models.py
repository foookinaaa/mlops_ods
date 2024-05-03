import pickle
from pathlib import Path

import click
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from .cli import cli


def train(data: np.ndarray, target: np.ndarray) -> LogisticRegression:
    model_params = {"random_state": 42, "max_iter": 300, "C": 10}
    model_lr = LogisticRegression(**model_params)
    model_lr.fit(data, target)
    return model_lr


def test(model: LogisticRegression, data: np.ndarray, target: np.ndarray) -> dict:
    predicts = model.predict(data)
    return classification_report(target, predicts, output_dict=True)


@cli.command()
@click.argument("train_frame_path", type=Path)
@click.argument("train_target_path", type=Path)
@click.argument("model_path", type=Path)
def cli_train(
    train_frame_path: Path,
    train_target_path: Path,
    model_path: Path,
):
    train_features = np.load(train_frame_path)
    train_target = np.load(train_target_path)
    model = train(train_features, train_target)
    pickle.dump(model, model_path.open("wb"))