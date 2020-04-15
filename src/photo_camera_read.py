import cv2
import numpy as np
import pickle
import pandas as pd

#####################################################

scale = 1
cached_sudoku_boards = 20

data = pd.read_csv("src/train/labels.csv")
pickle_file = open("src/train/model_trained.p", "rb")
model = pickle.load(pickle_file)


################### CNN functions ###########################


def grayscale(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def equalize(img):
    img = cv2.equalizeHist(img)
    return img


def preprocessing(img):
    img = cv2.resize(img, (32, 32))
    img = grayscale(img)
    img = equalize(img)
    img = img / 255
    return img


def recognise(img):
    img = preprocessing(img)
    img_pred = img.reshape(1, 32, 32, 1)

    # PREDICTION
    predictions = model.predict(img_pred)

    digit_predicted = np.argmax(predictions[0]) + 1

    return digit_predicted


#####################################################


def make_image_rectangle(img):
    img_small = cv2.resize(img, (0, 0), fx=scale, fy=scale)
    width = int(np.size(img_small, 1))
    height = int(np.size(img_small, 0))
    centre = int((width - height) / 2)

    return img_small[0:height, centre:width - centre]


def draw_user_interface(img_user):
    cv2.line(img_user, (70, 70), (70, 570), (0, 0, 0), 2)
    cv2.line(img_user, (70, 570), (570, 570), (0, 0, 0), 2)
    cv2.line(img_user, (570, 570), (570, 70), (0, 0, 0), 2)
    cv2.line(img_user, (570, 70), (70, 70), (0, 0, 0), 2)
    cv2.putText(img_user, "Press enter to confirm", (130, 60), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)

    return img_user


def get_dilated_image(img_small):
    img_blur = cv2.GaussianBlur(img_small, (5, 5), 1)
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 90, 20)

    return cv2.dilate(img_canny, np.ones((5, 5)), iterations=1)


def get_contour_points(img_dilate):
    max_area = 0
    sudoku_points = []

    contours, hierarchy = cv2.findContours(img_dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        points = cv2.approxPolyDP(contour, 50, 10, True)

        if area > max_area and len(points) == 4:
            sudoku_points = points
            max_area = area

    return sudoku_points


def sort_points(points):
    if len(points) != 4: raise ValueError

    x_average = (points[0][0][0] + points[1][0][0] + points[2][0][0] + points[3][0][0]) / 4
    y_average = (points[0][0][1] + points[1][0][1] + points[2][0][1] + points[3][0][1]) / 4

    se = nw = ne = sw = None

    for point in points:
        point = point[0]
        if point[0] > x_average and point[1] > y_average:
            se = point
        elif point[0] < x_average and point[1] < y_average:
            nw = point
        elif point[0] > x_average and point[1] < y_average:
            ne = point
        elif point[0] < x_average and point[1] > y_average:
            sw = point

    return [nw, ne, sw, se]


def get_transformed_sudoku(img_small, points):
    before = np.float32(points)
    after = np.float32([[0, 0], [900, 0], [0, 900], [900, 900]])

    matrix = cv2.getPerspectiveTransform(before, after)
    return cv2.warpPerspective(img_small, matrix, (900, 900))


def get_separated_sudoku_numbers(img_sudoku):
    img_sudoku_blur = cv2.GaussianBlur(img_sudoku, (3, 3), 1)
    img_sudoku_gray = cv2.cvtColor(img_sudoku_blur, cv2.COLOR_BGR2GRAY)
    img_sudoku_canny = cv2.Canny(img_sudoku_gray, 90, 20)
    img_sudoku_dilate = cv2.dilate(img_sudoku_canny, np.ones((6, 6)))
    img_sudoku_processed = cv2.morphologyEx(img_sudoku_dilate, cv2.MORPH_CLOSE, np.ones((6, 6)))

    horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 100))
    vertical_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 1))
    img_sudoku_horizontal = cv2.morphologyEx(img_sudoku_processed, cv2.MORPH_OPEN, horizontal_structure)
    img_sudoku_vertical = cv2.morphologyEx(img_sudoku_processed, cv2.MORPH_OPEN, vertical_structure)

    img_sudoku_table = img_sudoku_horizontal + img_sudoku_vertical
    img_sudoku_table = cv2.dilate(img_sudoku_table, np.ones((15, 15)))

    return img_sudoku_processed - img_sudoku_table


def get_completed_sudoku_photo(img_sudoku_numbers, sudoku_cut):
    thresh, im_bw = cv2.threshold(img_sudoku_numbers, 128, 255, 0)
    contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    sudoku_board = [[None] * 9 for _ in range(9)]

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 500:
            x, y, w, h = cv2.boundingRect(contour)
            img_number = sudoku_cut[y:y + h, x:x + w]
            prediction = recognise(img_number)

            y_index = int(np.floor(y / 100))
            x_index = int(np.floor(x / 100))

            sudoku_board[y_index][x_index] = prediction

    return sudoku_board


def get_completed_sudoku_camera(img_sudoku_numbers, sudoku_cut, img_sudoku_result):
    thresh, im_bw = cv2.threshold(img_sudoku_numbers, 128, 255, 0)
    contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    sudoku_board = [[None] * 9 for _ in range(9)]

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 500:
            x, y, w, h = cv2.boundingRect(contour)
            img_number = sudoku_cut[y:y + h, x:x + w]
            prediction = recognise(img_number)

            y_index = int(np.floor(y / 100))
            x_index = int(np.floor(x / 100))

            cv2.putText(img_sudoku_result, str(prediction), (x_index * 70 + 20, y_index * 70 + 60),
                        cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)

            sudoku_board[y_index][x_index] = prediction

    return img_sudoku_result, sudoku_board


def render_window(img_user, img_sudoku_result):
    cv2.imshow('result', np.hstack((img_user, img_sudoku_result)))

    if cv2.waitKey(1) == 13:
        return False
    return True


def cache_sudoku_boards(sudoku_boards, sudoku_board):
    sudoku_boards.append(sudoku_board)
    if len(sudoku_boards) > cached_sudoku_boards:
        sudoku_boards.pop(0)


def get_result_sudoku_boards(sudoku_boards):
    result_sudoku_board = [[None] * 9 for _ in range(9)]
    for row in range(0, 9):
        for column in range(0, 9):
            numbers_counter = {}
            for sudoku_board in sudoku_boards:
                value = sudoku_board[row][column]
                numbers_counter[value] = 0

            for sudoku_board in sudoku_boards:
                value = sudoku_board[row][column]
                numbers_counter[value] += 1

            result_sudoku_board[row][column] = max(numbers_counter, key=numbers_counter.get)

    return result_sudoku_board


def read_image(filepath):
    img = cv2.imread(filepath)
    height, width, channels = img.shape

    global scale
    scale = 640 / height

    img_small = make_image_rectangle(img)

    img_dilate = get_dilated_image(img_small)
    points = get_contour_points(img_dilate)

    try:
        points = sort_points(points)
        img_sudoku = get_transformed_sudoku(img_small, points)
    except (ValueError, cv2.error):
        return [[None] * 9 for _ in range(9)]

    img_sudoku_numbers = get_separated_sudoku_numbers(img_sudoku)
    sudoku_board = get_completed_sudoku_photo(img_sudoku_numbers, img_sudoku)

    return sudoku_board


def read_camera():
    cap = cv2.VideoCapture(0)
    img_sudoku_grid = cv2.imread("img/sudoku-grid.png")

    global scale
    scale = 640 / cap.get(4)

    sudoku_boards = []
    loop = True

    while loop:
        success, img = cap.read()

        img_small = make_image_rectangle(img)
        img_user = draw_user_interface(img_small.copy())

        img_dilate = get_dilated_image(img_small)
        points = get_contour_points(img_dilate)

        try:
            points = sort_points(points)
            img_sudoku = get_transformed_sudoku(img_small, points)
        except (ValueError, cv2.error):
            loop = render_window(img_user, img_sudoku_grid)
            continue

        img_sudoku_numbers = get_separated_sudoku_numbers(img_sudoku)
        img_sudoku_result, sudoku_board = get_completed_sudoku_camera(img_sudoku_numbers, img_sudoku,
                                                                      img_sudoku_grid.copy())
        cache_sudoku_boards(sudoku_boards, sudoku_board)
        loop = render_window(img_user, img_sudoku_result)

    cap.release()
    cv2.destroyAllWindows()

    return get_result_sudoku_boards(sudoku_boards)
