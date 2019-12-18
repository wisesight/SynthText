# Author: Ankush Gupta
# Date: 2015

"""
Visualize the generated localization synthetic
data stored in h5 data-bases
"""
from __future__ import division
import os
import os.path as osp
import numpy as np
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import h5py
from common import *
from PIL import Image


def viz_textbb(text_im, charBB_list, wordBB, alpha=1.0):
    """
    text_im : image containing text
    charBB_list : list of 2x4xn_i bounding-box matrices
    wordBB : 2x4xm matrix of word coordinates
    """
    plt.close(1)
    plt.figure(1)
    plt.imshow(text_im)
    # img = Image.fromarray(text_im)
    # img.show()
    # plt.hold(True)
    H, W = text_im.shape[:2]

    # # plot the character-BB:
    # for i in range(len(charBB_list)):
    #     bbs = charBB_list[i]
    #     ni = bbs.shape[-1]
    #     for j in range(ni):
    #         bb = bbs[:,:,j]
    #         bb = np.c_[bb,bb[:,0]]
    #         plt.plot(bb[0,:], bb[1,:], 'r', alpha=alpha/2)

    # # plot the word-BB:
    # for i in range(wordBB.shape[-1]):
    #     bb = wordBB[:,:,i]
    #     bb = np.c_[bb,bb[:,0]]
    #     plt.plot(bb[0,:], bb[1,:], 'g', alpha=alpha)
    #     # visualize the indiv vertices:
    #     vcol = ['r','g','b','k']
    #     for j in range(4):
    #         plt.scatter(bb[0,j],bb[1,j],color=vcol[j])

    plt.gca().set_xlim([0, W - 1])
    plt.gca().set_ylim([H - 1, 0])
    plt.show(block=False)

def main(db_fname):
    dt = h5py.special_dtype(vlen=str)
    db = h5py.File(db_fname, "r")
    dsets = sorted(db["data"].keys())
    print("total number of images : ", colorize(Color.RED, len(dsets), highlight=True))
    
    counter = 0
    f = open('gt.txt', 'w')
    output_path = 'results/cropped/'
    for k in dsets:
        rgb = db["data"][k][...]
        charBB = db["data"][k].attrs["charBB"]
        wordBB = db["data"][k].attrs["wordBB"]
        txt = db["data"][k].attrs["txt"]
        txt = [n.decode("utf-8", "ignore") for n in txt]

        # viz_textbb(rgb, [charBB], wordBB)
        # get cropped images
        img = Image.fromarray(rgb)
        
        for i in range(wordBB.shape[-1]):
            bb = wordBB[:,:,i]
            left = min(bb[0])
            up = min(bb[1])
            right = max(bb[0])
            lower = max(bb[1])

            cropped = img.crop((left, up, right, lower))
            filename = str(counter) + '.jpg'
            cropped.save(output_path + filename)
            counter += 1
            f.write(filename + '\t' + txt[i] + '\n')

        # print("image name        : ", colorize(Color.RED, k, bold=True))
        # print("  ** no. of chars : ", colorize(Color.YELLOW, charBB.shape[-1]))
        # print("  ** no. of words : ", colorize(Color.YELLOW, wordBB.shape[-1]))
        # print("  ** text         : ", colorize(Color.GREEN, txt))

        # if "q" in input("next? ('q' to exit) : "):
        #     break
    db.close()
    f.close()


if __name__ == "__main__":
    main("results/SynthText.h5")
