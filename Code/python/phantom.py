import cv2
import numpy as np
import copy

rows = 0
cols = 0

Pic_data_dir = "../../Images/"

def create_pic():
    global rows, cols
    #image_path = Pic_data_dir+"small_p.png"
    image_path = Pic_data_dir+"p.png"
    s = {}
    image = cv2.imread(image_path)
    # cv2.imshow("1", image)
    h, w, c = image.shape
    rows = h
    cols = w
    cnt = 0
    for i in range(h):
        for j in range(w):
            try:
                s[image[i][j][0]] == cnt
            except:
                s[image[i][j][0]] = cnt
                print("[{},{},{}],".format(image[i][j][0], image[i][j][1], image[i][j][2]))
                cnt += 1
    file = open("mypic.txt", 'w')
    for i in range(h):
        for j in range(w):
            file.write(str(s[image[i][j][0]]))
            file.write(" ")
    file.close()

def read_image():
    image_path = "mypic.txt"
    file = open(image_path, 'r')
    data = file.readlines()[0]
    file.close()
    data = data.split(" ")[:-1]
    image = list(map(int, data))
    image = np.array(image)
    image.resize((rows, cols))
    return image

def save_image(image):
    file = open("p.txt", 'w')
    for i in range(rows):
        for j in range(cols):
            if image[i][j]==0:
                file.write(str(255))
            else:
                file.write(str(0))
            file.write("\n")
    file.close()

def save_image_t(image):
    file = open("p_t.txt", 'w')
    for i in range(rows):
        for j in range(cols):
            if image[j][i] == 0:
                file.write(str(255))
            else:
                file.write(str(0))
            file.write("\n")
    file.close()

def read_p_image():
    image_path = "p.txt"
    file = open(image_path, 'r')
    lines = file.readlines()
    data = []
    for line in lines:
        data.append(line[:-1])
    file.close()
    image = list(map(int, data))
    image = np.array(image)
    image.resize((rows, cols))
    image = np.uint8(image)
    return image

def show_image(image):
    colors = [
        [255, 255, 255],
        [14, 201, 255],
        [21, 0, 136],
        [0, 0, 0],
        [87, 122, 185],
        [76, 177, 34],
        [36, 28, 237],
    ]
    color_image = []
    for i in range(rows):
        for j in range(cols):
            # color_image.append(colors[image[i][j]-1])
            if image[i][j]==0:
                color_image.append(colors[0])
            else:
                color_image.append(colors[3])
    color_image = np.array(color_image)
    color_image.resize((rows, cols, 3))
    color_image = np.uint8(color_image)
    cv2.imshow("1", color_image)
    cv2.waitKey()

def get_observation_image(image):
    mean = [
        0, 255
    ]

    delta = [
        200, 200
    ]

    oberservation_image = []

    for i in range(rows):
        for j in range(cols):
            if image[i][j]==255:
                color_class = 1
            else:
                color_class = 0
            random_number = np.random.normal(mean[color_class], delta[color_class])
            oberservation_image.append(random_number)
    oberservation_image = np.array(oberservation_image)
    oberservation_image.resize((rows, cols))
    return oberservation_image


def show_2gray():
    file = open("2gray.txt", 'r')
    data = file.readline()
    file.close()
    data = data.split(" ")[:-1]
    print(len(data))
    image = list(map(int, data))
    image = np.array(image)
    image.resize((rows, cols))
    image = np.uint8(image)
    cv2.imshow("1", image)
    cv2.waitKey()

def show_observation_image(image):
    min = image.min()
    max = image.max()
    image-=min
    image/=max
    image*=255
    image = np.uint8(image)
    cv2.imshow("observation_image", image)
    cv2.imwrite("observation_image.jpg", image)
    # cv2.waitKey()

def show_mean_filter_image(image):
    min = image.min()
    max = image.max()
    image-=min
    image/=max
    image*=255
    image = np.uint8(image)
    cv2.imshow("mean_filter_image", image)
    cv2.imwrite("mean_filter_image.jpg", image)
    # cv2.waitKey()

def show_midle_filter_image(image):
    min = image.min()
    max = image.max()
    image-=min
    image/=max
    image*=255
    image = np.uint8(image)
    cv2.imshow("midle_filter_image", image)
    cv2.imwrite("midle_filter_image.jpg", image)
    cv2.waitKey()

def mean_local_filter(image):
    kernal_size = 3
    kk = kernal_size*kernal_size
    r = int(kernal_size/2)
    add_image = copy.deepcopy(image)
    new_image = copy.deepcopy(image)
    for i in range(rows):
        for j in range(cols):
            l = 0
            u = 0
            lu = 0
            if i-1>=0:
                u = add_image[i-1][j]
            if j-1>=0:
                l = add_image[i][j-1]
            if  i-1>=0 and j-1>=0:
                lu = add_image[i-1][j-1]
            add_image[i][j] = l+u-lu+add_image[i][j]

    for i in range(r, rows-r):
        for j in range(r, cols-r):
            new_image[i][j] = (add_image[i+r][j+r]-add_image[i+r][j-r]-add_image[i-r][j+r]+add_image[i-r][j-r])/kk
    return new_image

def midle_local_filter(image):
    kernal_size = 5
    kk = kernal_size * kernal_size
    r = int(kernal_size / 2)
    new_image = copy.deepcopy(image)
    mid_no = int(kk / 2) + 1
    for i in range(r, rows - r):
        for j in range(r, cols - r):
            temp = []
            for p in range(-r, r+1):
                for q in range(-r, r+1):
                    temp.append(image[i+p][j+q])
            temp.sort()
            new_image[i][j] = temp[mid_no]
    return new_image

if __name__ == '__main__':
    create_pic()
    image = read_image()
    save_image(image)
    save_image_t(image)
    # show_image(image)
    image = read_p_image()
    oberservation_image = get_observation_image(image)
    show_observation_image(oberservation_image)
    mean_filter_image = mean_local_filter(oberservation_image)
    show_mean_filter_image(mean_filter_image)
    midle_filter_image = midle_local_filter(oberservation_image)
    show_midle_filter_image(midle_filter_image)


