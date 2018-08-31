import scipy.misc

class Check:


    def __init__(self, picPath):
        self.img_array = scipy.misc.imread(picPath, flatten=True)
        # print(img_array)
        # 常规数据0指黑色，255是白色，但是MNISt数据集使用相反的方式表示，所以需要用255去减
        temp_img_data = 255.0 - self.img_array.reshape(784)
        # print(img_data)
        self.img_data = (temp_img_data / 255.0 * 0.99) + 0.01
        # print(img_data)
        pass

    def check(self, n):
        outputs = n.query(self.img_data)
        print(outputs)