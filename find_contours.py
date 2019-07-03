import numpy as np
import cv2 as cv2
import sys
import os
from PIL import Image
import webcolors
import codecs, json 

class convert_Image():

        def __init__(self, imgFilename):
                out_dict  = {}
                np.set_printoptions(threshold=sys.maxsize)
                img = cv2.imread(imgFilename)
                colors = self.get_colors(img)
                imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                colors = self.get_colors(imghsv)
                self.all_contours = []
                print(colors[7])
                for color in colors:
                        curMask = cv2.inRange(imghsv, color, color)
                        contours, hierarchy = cv2.findContours(curMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        contourCount = 0
                        for c in contours:
                                out_dict[str("Contour_" + str(contourCount) + "_for_color_" + str(color))] = c.tolist()
                                contourCount += 1
                #print( json.dumps(out_dict, sort_keys=True, indent = 4))
                self.data = out_dict

        def get_all_contours(self):
                return self.all_contours

                
        def get_colors(self, image):
                all_rgb_codes = image.reshape(-1, image.shape[-1])
                unique_rgbs = np.unique(all_rgb_codes, axis=0)
                test = np.array(unique_rgbs)
                colors = np.unique(test, axis=0, return_counts = True)[0]

                return colors
                
def main():
    inputFolderPath = sys.argv[1]
    outputFolderPath = sys.argv[2]
    sys.path.append(inputFolderPath)
    sys.path.append(outputFolderPath)
    for filename in os.listdir(inputFolderPath):
        curImage = convert_Image(inputFolderPath + "/" + filename)
        listContours = curImage.all_contours
 
        with open(outputFolderPath + "/" + filename + ".txt", 'w', encoding='utf-8') as outfile:
                json.dump(curImage.data, outfile, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
