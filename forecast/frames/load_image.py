from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import OpenGL.GL as gl

TICKS_STEP = {
    "3D": 15,
    "W": 10,
    "2W": 5,
    "M": 2
}


def create_image(purchases_df, prediction_results, aggr_window):
    plt.plot(prediction_results, label="predicted")
    plt.plot(purchases_df["sales"].values, alpha=0.6, label="true")
    plt.xticks(
        np.arange(len(purchases_df.index), step=TICKS_STEP[aggr_window]),
        purchases_df.index[::TICKS_STEP[aggr_window]].strftime('%Y-%m-%d'),
        fontsize=10, rotation=90
    )
    plt.yticks(fontsize=12)
    plt.legend(fontsize=14)
    plt.savefig('prediction.jpg', bbox_inches="tight")
    plt.close()


def get_textureID():
    image = Image.open("prediction.jpg") 
    image = image.convert('RGB')   
    img_data = np.array(list(image.getdata()), np.uint8)

    textureID = gl.glGenTextures(1)
    gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, textureID)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_BASE_LEVEL, 0)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAX_LEVEL, 0)
    gl.glTexImage2D(
        gl.GL_TEXTURE_2D, 0, gl.GL_RGB, image.size[0],
        image.size[1], 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img_data
    )
    image.close()
    
    return textureID, image.size