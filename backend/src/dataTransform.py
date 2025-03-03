def fromIntSetToString(setToTransform: set[int]) -> str:
    result: str = ""
    # print(type(setToTransform))
    setToTransform = list(setToTransform)
    setToTransform.sort()
    for item in setToTransform:
        # print('skibidi')
        item = str(item)
        result += item
    return result

def fromStringToIntSet(stringToTransform: str) -> set[int]:
    result = set()
    for item in stringToTransform:
        item = int(item)
        result.add(item)
    return result