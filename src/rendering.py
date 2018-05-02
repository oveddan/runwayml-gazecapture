import cv2
import numpy as np

def render_gazes_on_image(frame, outputs, window_width, window_height, window_height_cm, camera_h_from_screen_top):
    pixels_per_cm = window_height * 1. / window_height_cm

    print(window_height, window_height_cm)

    camera_pixels_from_l = window_width / 2
    camera_pixels_from_top = camera_h_from_screen_top * pixels_per_cm

    x_translation_from_camera_c = camera_pixels_from_l
    y_translation_from_camera_c = camera_pixels_from_top

    print(pixels_per_cm, x_translation_from_camera_c, y_translation_from_camera_c)
    print(outputs)

    for output in outputs:
        screen_x = output[0] * pixels_per_cm + x_translation_from_camera_c 
        screen_y = -output[1] * pixels_per_cm + y_translation_from_camera_c

        print("in px:", round(screen_x), round(screen_y))

        if screen_x >= 0 and screen_y >= 0:
            #  cv2.circle(frame, (20, 20), 5, (0, 0, 255), -1)
            cv2.circle(frame, (int(round(screen_x)),int(round(screen_y))), 20, (0, 0, 255), -1)



def render_gaze_on_simulated_screen(screen_size, outputs):
    screen_width = screen_size
    screen_height = screen_size 
    pixels_per_cm = screen_size / 25.0
    frame = np.zeros((screen_width, screen_height), np.uint8) 

    camera_pixels_from_l = screen_width / 2
    camera_pixels_from_top = screen_height / 2


    for output in outputs:
        screen_x = output[0] * pixels_per_cm + camera_pixels_from_l
        screen_y = -output[1] * pixels_per_cm + camera_pixels_from_top

        print('results:', output)
        print("in px:", [round(screen_x), round(screen_y)])

        if screen_x >= 0 and screen_y >= 0:
            cv2.circle(frame, (int(round(screen_x)),int(round(screen_y))), 5, 255, -1)

    return frame


def combine_simulated_and_screen(simulated_size, screen_width, screen_height, outputs, frame):
    simulated_screen = render_gaze_on_simulated_screen(simulated_size, outputs)

    flipped = cv2.flip(frame, 1)
    gray = cv2.cvtColor(flipped, cv2.COLOR_RGB2GRAY )

    scale_size = (screen_width - simulated_size) / (frame.shape[1] * 1.)
    scaled_for_combined = cv2.resize(gray, None, fx=scale_size, fy=scale_size, interpolation=cv2.INTER_AREA)
    #  print(screen.shape, scaled_for_combined.shape)
    combined = np.ones((scaled_for_combined.shape[0], screen_width), np.uint8)
    combined[0:simulated_size, 0:simulated_size] = simulated_screen

    second_start = simulated_size
    #  print(scaled_for_combined.shape)
    #  print('the results', scaled_for_combined.shape[1], scaled_for_combined.shape[0])
    combined[0:scaled_for_combined.shape[0],second_start:second_start+scaled_for_combined.shape[1]] = scaled_for_combined[:, :]

    #  return scaled_for_combined
    return combined
