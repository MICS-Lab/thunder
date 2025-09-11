import torch
import torch.nn.functional as F


# Adapted from https://medium.com/data-scientists-diary/implementation-of-dice-loss-vision-pytorch-7eef1e438f68
def multiclass_dice_loss(
    pred: torch.Tensor, label: torch.Tensor, mask: torch.Tensor, smooth: float = 1
) -> torch.Tensor:
    """
    Computes Dice Loss for multi-class segmentation.
    :param pred: Tensor of predictions (B, C, H, W).
    :param label: Ground truth labels (B, H, W).
    :param mask: Mask to apply to pred and target.
    :param smooth: Smoothing factor.

    :return: Scalar Dice Loss.
    """

    pred = F.softmax(pred, dim=1)  # Converting logits to probabilities
    num_classes = pred.shape[1]  # Number of classes (C)

    target = label.clone()
    target[~mask] = (
        num_classes  # Adding a dummy class to account for masked pixels (-1 label values)
    )
    target = F.one_hot(
        target, num_classes=num_classes + 1
    )  # Creating a tensor of one-hot target vectors
    target = target[..., :-1]  # Removing dummy class channel
    target = target.permute((0, 3, 1, 2))
    mask = mask.unsqueeze(1)

    intersection = (pred * target * mask).sum(
        dim=(0, 2, 3)
    )  # Element-wise multiplication
    union = (pred * mask).sum(dim=(0, 2, 3)) + (target * mask).sum(
        dim=(0, 2, 3)
    )  # Sum of all pixels

    dice = (2.0 * intersection + smooth) / (
        union + smooth
    )  # Per-class and per-image Dice score

    return 1 - dice.mean()  # Averaging Dice Loss across classes
