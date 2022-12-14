from abc import abstractmethod
from typing import Protocol

import cv2
import numpy as np
import numpy.typing as npt


class Scene(Protocol):
    """The Scene Class is a superclass that all scenes inherit from.

    The Scene Class is a superclass that all scenes inherit from. It contains
    the basic functionality that all scenes need to have. In a nutshell, the
    Scene Class acts upon an image and defines a conditional that determines
    whether the image is a match for the Scene's template. It is purposefully
    written to be highly flexible in order to be as widely applicable as
    possible. The Scene Class is not meant to be instantiated directly, but
    rather to be subclassed.
    """

    scene_bounds: tuple[int, int, int, int]
    template_path: str

    @abstractmethod
    def transform(self, image: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
        """Transforms the image into a form that is easier to compare.

        Transforms the image into a form that is easier to compare. This
        function is meant to be overridden by subclasses.

        Args:
            image (npt.NDArray[np.uint8]): The image to transform

        Returns:
            npt.NDArray[np.uint8]: The transformed image
        """
        raise NotImplementedError

    @abstractmethod
    def compare(self, image: npt.NDArray[np.uint8]) -> bool:
        """Compares the image to the template.

        Compares the image to the template. This function is meant to be
        overridden by subclasses.

        Args:
            image (npt.NDArray[np.uint8]): The image to compare

        Returns:
            bool: Whether the image matches the template
        """
        raise NotImplementedError


class DefaultScene(Scene):
    """The DefaultScene is a subclass of Scene.

    The DefaultScene is a subclass of Scene. It is meant to be used as a
    placeholder for when a scene is not recognized. It is also meant to be
    subclassed.
    """

    scene_bounds = (0, 0, 0, 0)

    def transform(self, image: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
        """Transforms the image into a form that is easier to compare.

        Transforms the image into a form that is easier to compare. This
        function is meant to be overridden by subclasses.

        Args:
            image (npt.NDArray[np.uint8]): The image to transform

        Returns:
            npt.NDArray[np.uint8]: The transformed image
        """
        # Crop the image to the scene bounds
        return image[
            self.scene_bounds[0] : self.scene_bounds[2],
            self.scene_bounds[1] : self.scene_bounds[3],
        ]

    def compare(self, image: npt.NDArray[np.uint8]) -> bool:
        """Compares the image to the template.

        Compares the image to the template. This function is meant to be
        overridden by subclasses.

        Args:
            image (npt.NDArray[np.uint8]): The image to compare

        Returns:
            bool: Whether the image matches the template
        """
        # Compare the image to the template
        return np.array_equal(image, cv2.imread(self.template_path))
