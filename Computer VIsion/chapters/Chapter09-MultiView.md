# MultiView

Method to eliminate 3D structure from two arbitrary images of a scene captured with cameras whose intrinsic parameters are known.

## Binocular Field of View

The **Binocular Fied of View** is the overlapping (intersection) filed of view in a binocular system. The field of view of the system is the union of the field of view of two cameras.

We can only estimate depth within the binocular field of view because we need two cameras for estimation.

### Vergence

- If we verge the two cameras, the field of view of the system becomes smaller, but the binocular field of view becomes larger
  - FoV decreases
  - Accuracy of depth estimation increases