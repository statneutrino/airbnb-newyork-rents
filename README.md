# End-to-end ML Pipeline for Short-Term Rental Prices in NYC
This github repository (https://github.com/statneutrino/airbnb-newyork-rents) 
is the final outcome for a project that I undertook at Udacity. I wrote a 
Machine Learning Pipeline to solve the following problem: a property management company is renting
rooms and properties in New York for short periods on various rental platforms.

Brief:
To estimate the typical price for a given property based on the price of similar properties. 
The company receives new data in bulk every week, so the model
needs to be retrained with the same cadence, necessitating
a reusable pipeline.

This solution is an *end-to-end* pipeline covering data fetching, validation, segregation, train
and validation, test, and release. I have run the model on an initial
data sample, re-run it on a new data sample simulating a
new data delivery, and it can be reran on new data in production.

## Hydra sweep: _axsweeper_ and bayesian optimisation

This solution implements *Bayesian optimisation* using [Adaptive Experimentation Platform](https://ax.dev/) or
[Ax](https://ax.dev/) to search for optimum hyperparameters. This can be found in release v1.0.3

## Experiment tracking using Weights & Biases
I have used [Weights & Biases](https://wandb.ai/site) for tracking for artifacts, experiments and hyperparameters
for this project. I have made my W&B project public and can be found [here](https://wandb.ai/statneutrino/nyc_airbnb)


## Instructions to for training model
In order to run the scripts from a linux console, install mlflow and python=3.8. The run the following command

    $ mlflow run https://github.com/statneutrino/airbnb-newyork-rents.git -v 1.0.4

This runs the latest release.

If wanting to use hydra-axsweeper to perform Bayesian optimisation for hyperparameter search:

    $ mlflow run https://github.com/statneutrino/airbnb-newyork-rents.git -v 1.0.3

## Further work

### axsweeper bug
There is currently a bug with the current implementation of axsweeper - only the first 5 jobs can be run before
an error is raised - I am currently investigating this and will update when ready

### Improving performance

#### BART
What I'd like to do next is implement Bayesian Additive Regression Trees (BART) within an mlflow pipeline.
Advantages are:
- Much less parameter optimization required than random forests and gradient-boosting methods
- Provides confidence intervals in addition to just point estimates
- Flexible through use of priors and embedding in bigger models

#### Data
Personally I think this model's performance could be improved quite easily with new data sources e.g.
- Image data (CNN/deep learning) of homes/rooms features
- Data linkage of latitude and longitude with neighbourhood/spatial economic or tourism data


