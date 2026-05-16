import numpy as np

def resolve_seed (seed: int | None = None) -> int:
    """Resolves seed that will be passed into GridOptions.
    
    If seed is already an int it checks if it is non-negative and returns it.
    If it is None then it generates a seed from entropy."""

    if seed is not None:

        if seed < 0:
            raise ValueError (f'Seed value cannot be negative. You gave {seed}')
        
        return seed
    
    random_seed = np. random. SeedSequence (). entropy
    
    assert isinstance(random_seed, int)

    return random_seed