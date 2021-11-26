#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd
import os
import tempfile


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()
    logger.info(f"Downloading artifact {args.input_artifact} from W&B")
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    df = pd.read_csv(artifact_local_path)

    # Drop outliers
    logger.info("Dropping outliers")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    logger.info("Converting last_review to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:

        logger.info(f"Saving cleaned data as {args.output_artifact}")
        export_path = os.path.join(temp_dir, args.output_artifact)
        df.to_csv(export_path, index=False)

        logger.info(f"Logging artifact with W&B as {args.output_artifact}")
        artifact = wandb.Artifact(
            args.output_artifact,
            type=args.output_type,
            description=args.output_description,
        )

        artifact.add_file(export_path)
        run.log_artifact(artifact)

        # Make sure the artifact is uploaded before the temp dir
        # gets deleted
        artifact.wait()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Unprocessed data requiring cleaning",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Data cleaned by removing outliers and converting variables to correct type",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of output artifact (for storing in W&B)",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Threshold for min rent price for outlier removal",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Threshold for max rent price",
        required=True
    )


    args = parser.parse_args()

    go(args)
