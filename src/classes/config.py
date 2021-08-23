import json

from classes.mask import Mask

class Config:
    def getColorMasks():
        f = open("config.json")
        data = json.load(f)
        f.close()
        
        colors = data['colors']
        masks = []
        for color in colors:
            if (color['include'] == "True"):
                mask = Mask(name=color['name'], low=color['lower'], high=color['upper'])
                masks.append(mask)
        return masks