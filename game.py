import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


class Game:
    def __init__(self) -> None:
        # Level 'Nybörjare'
        self._rows = 8
        self._columns = 8
        self.mines = 10

        # Images of game
        with open("images.json") as json_file:
            self._images = json.load(json_file)

        # Launch the website TODO controlled close of driver
        url = "https://minesweeper.one/röj/"
        self._driver = webdriver.Chrome()
        self._driver.get(url)
        self._action = ActionChains(self._driver)

        # Open options menu
        options_element = self._driver.find_element(by=By.LINK_TEXT, value="Alternativ")
        options_menu_element = self._driver.find_element(by=By.ID, value="divMenuOpt")

        if not options_menu_element.is_displayed():
            options_element.click()

        # Find an uncheck question mark
        question_mark_element = self._driver.find_element(
            by=By.PARTIAL_LINK_TEXT, value="Frågetecken"
        )
        check_mark = (
            question_mark_element.find_element(
                by=By.TAG_NAME, value="img"
            ).get_attribute("src")
            == self._images["check_mark"]
        )

        if check_mark == True:
            question_mark_element.click()
        else:
            options_element.click()

        # Face element
        self._face_element = self._driver.find_element(by=By.NAME, value="face")

    @property
    def rows(self) -> int:
        """Number of rows on the board"""
        return self._rows

    @property
    def columns(self) -> int:
        """Number of columns on the board"""
        return self._columns

    def new_game(self) -> None:
        """Start new game"""
        self._face_element.click()

    def get_face(self) -> str:
        """Check game status by face expression"""

        face_element = self._driver.find_element(by=By.NAME, value="face")
        src = face_element.get_attribute("src")
        face = self._images["faces"][src]

        return face

    def get_mines_count(self) -> int:
        """Read the value of the mine counter"""

        mines_count = 0

        for digit in (1, 10, 100):
            digit_element = self._driver.find_element(
                by=By.NAME, value=f"bomb{digit}s"
            )  # TODO move to __init__
            value = self._images["counter_digits"][digit_element.get_attribute("src")]

            if digit == 100 and value == -1:
                mines_count *= -1
            else:
                mines_count += value * digit

        return mines_count

    def get_time_count(self) -> int:
        """Read the value of the time counter"""
        time_count = 0

        for digit in (1, 10, 100):
            digit_element = self._driver.find_element(
                by=By.NAME, value=f"time{digit}s"
            )  # TODO move to __init__
            value = self._images["counter_digits"][digit_element.get_attribute("src")]

            time_count += value * digit

        return time_count

    def get_board_status(self) -> list[str]:
        """Read the status of all cells in the game board"""

        cell_elements = self._driver.find_elements(
            by=By.XPATH, value="//img[starts-with(@name, 'cellIm')]"
        )
        board = [
            self._images["cells"][cell_element.get_attribute("src")]
            for cell_element in cell_elements
        ]

        return board

    def play(
        self, row: int, column: int, mouse_button: str
    ) -> None:  # TODO return score?
        """Make one move.
        Takes row and column index of cell to click and
        mouse_button takes the values 'left' or 'right' depending on which mouse button to press.
        """

        cell = f"cellIm{column}_{row}"
        cell_element = self._driver.find_element(by=By.NAME, value=cell)

        if mouse_button == "left":
            cell_element.click()
        elif mouse_button == "right":
            self._action.context_click(cell_element).perform()
        else:
            raise ValueError(f"Got illegal value of mouse_button {mouse_button}")
