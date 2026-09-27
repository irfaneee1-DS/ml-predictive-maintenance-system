# Source-File and Validation-Fold Definitions

## Source Dataset

The analytical workflow uses the engineered CWRU bearing dataset:

`phase1_full_dataset.csv`

The dataset contains 6,153 rows and 25 columns.

`Source_File` is used as the grouping variable to prevent samples originating from the same source file from appearing in both training and test sets.

## Source Files

The source files used in the grouped validation are:

- 97.mat
- 98.mat
- 99.mat
- 100.mat
- 105.mat
- 106.mat
- 107.mat
- 108.mat
- 118.mat
- 119.mat
- 120.mat
- 121.mat
- 130.mat
- 131.mat
- 132.mat
- 133.mat

## Four Grouped Validation Folds

The four test folds are constructed by selecting one source file from each class for each fold.

### Fold 1

Test files:

- 100.mat
- 105.mat
- 118.mat
- 130.mat

### Fold 2

Test files:

- 97.mat
- 106.mat
- 119.mat
- 131.mat

### Fold 3

Test files:

- 98.mat
- 107.mat
- 120.mat
- 132.mat

### Fold 4

Test files:

- 99.mat
- 108.mat
- 121.mat
- 133.mat

## Grouping Method

The validation uses `Source_File` as the grouping variable.

For each fold:

1. The four designated source files are used as the test set.
2. All remaining source files are used for training.
3. The training and test source-file sets are checked for overlap.
4. Random Forest is trained using 200 trees with `random_state=42`.
5. Accuracy is calculated on the held-out test files.

The notebook reports no source-file overlap between the training and test sets for all four folds.

## Validation Results

The Random Forest accuracy reported by the notebook is:

| Fold | Accuracy |
|---:|---:|
| 1 | 1.0 |
| 2 | 1.0 |
| 3 | 1.0 |
| 4 | 1.0 |

Average accuracy: `1.0`

Standard deviation: `0.0`

The resulting fold-level accuracy output is stored in:

`data/groupfold_results.csv`
