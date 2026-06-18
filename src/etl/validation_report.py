from pathlib import Path


def save_validation_report(
    df,
    output_path="data/exports/validation_failures.csv",
):
    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        output_path,
        index=False,
    )
