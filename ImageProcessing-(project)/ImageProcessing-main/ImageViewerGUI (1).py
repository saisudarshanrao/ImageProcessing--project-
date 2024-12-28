####### REQUIRED IMPORTS FROM THE PREVIOUS ASSIGNMENT #######
import PIL.Image
from matplotlib import pyplot as plt
from my_package import Dataset, InstanceSegmentationModel, plot_visualization

####### ADD THE ADDITIONAL IMPORTS FOR THIS ASSIGNMENT HERE #######
from tkinter import *
from tkinter import ttk, filedialog
import os.path
from functools import partial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Define the function you want to call when the filebrowser button is clicked.
def fileClick(clicked, dataset, segmentor):
    ####### CODE REQUIRED (START) #######
    # This function should pop-up a dialog for the user to select an input image file.
    # Once the image is selected by the user, it should automatically get the corresponding outputs from the segmentor.
    # Hint: Call the segmentor from here, then compute the output images from using the `plot_visualization` function and save it as an image.
    # Once the output is computed it should be shown automatically based on choice the dropdown button is at.
    # To have a better clarity, please check out the sample video.
    global imgpath
    filetypes = (('img files', '*.jpg *.png'),)
    imgpath = filedialog.askopenfilename(title='Open a file', initialdir='./data/imgs', filetypes=filetypes)
    if imgpath:
        e.delete(0, "end")
        img_idx = int(os.path.splitext(os.path.basename(imgpath))[0])
        cache_path = ['./cache/Bounding-box/' + os.path.basename(imgpath),
                      './cache/Segmentation/' + os.path.basename(imgpath)]
        if not (os.path.exists(cache_path[0]) or os.path.exists(cache_path[1])):
            boxes, masks, classes, score = segmentor(dataset[img_idx]['image'])
            plot_visualization(dataset[img_idx]['image'], boxes, masks, classes, score, output=cache_path)
        process(clicked)
    ####### CODE REQUIRED (END) #######


# `process` function definition starts from here.
# will process the output when clicked.
def process(clicked):
    ####### CODE REQUIRED (START) #######
    # Should show the corresponding segmentation or bounding boxes over the input image wrt the choice provided.
    # Note: this function will just show the output, which should have been already computed in the `fileClick` function above.
    # Note: also you should handle the case if the user clicks on the `Process` button without selecting any image file.
    global canvas, imgpath
    canvas.get_tk_widget().destroy()
    if imgpath:
        imgclicked = PIL.Image.open('./cache/' + clicked.get() + '/' + os.path.basename(imgpath))
        img = PIL.Image.open(imgpath)
        plt.rcParams['figure.constrained_layout.use'] = True
        fig = plt.figure(figsize=(10, 5))
        plt1 = fig.add_subplot(121)
        plt1.axis('off')
        plt2 = fig.add_subplot(122)
        plt2.axis('off')
        plt1.imshow(img)
        plt2.imshow(imgclicked)
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=3)
        plt.close()
        e.delete(0, 'end')
    else:
        e.delete(0, 'end')
        e.insert(0, "select image!!")
    ####### CODE REQUIRED (END) #######


# `main` function definition starts from here.
if __name__ == '__main__':
    ####### CODE REQUIRED (START) ####### (2 lines)
    # Instantiate the root window.
    # Provide a title to the root window.
    root = Tk()
    root.title("20CS10019")
    ####### CODE REQUIRED (END) #######

    # Setting up the segmentor model.
    annotation_file = './data/annotations.jsonl'
    transforms = []

    # Instantiate the segmentor model.
    segmentor = InstanceSegmentationModel()
    # Instantiate the dataset.
    dataset = Dataset(annotation_file, transforms=transforms)

    # Declare the options.
    options = ["Segmentation", "Bounding-box"]
    clicked = StringVar()
    clicked.set(options[0])

    e = Entry(root, width=70)
    e.grid(row=0, column=0)

    ####### CODE REQUIRED (START) #######
    # Declare the file browsing button
    canvas = FigureCanvasTkAgg()
    e.insert(0, "select image!!")
    imgpath = ''
    filebutton = Button(root, text='Image', command=partial(fileClick, clicked, dataset, segmentor))
    filebutton.grid(row=0, column=1)
    ####### CODE REQUIRED (END) #######

    ####### CODE REQUIRED (START) #######
    # Declare the drop-down button
    dropdown = ttk.Combobox(root, textvariable=clicked)
    dropdown['values'] = options
    dropdown.grid(row=0, column=2)
    ####### CODE REQUIRED (END) #######

    # This is a `Process` button, check out the sample video to know about its functionality
    myButton = Button(root, text="Process", command=partial(process, clicked))
    myButton.grid(row=0, column=3)

    ####### CODE REQUIRED (START) ####### (1 line)
    # Execute with mainloop()
    root.mainloop()
    ####### CODE REQUIRED (END) #######
