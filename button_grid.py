import logging
import pygame
import game_button
import constants as _c


class ButtonGrid:
    def __init__(self, n_rows, n_cols, col_width, row_height, label_list,
            callback_list, disp, x_pos, y_pos, fit_to_text=False, x_pad=10, 
            y_pad=10, log=logging.getLogger(), color=_c.BUTTON_COLOR,
            click_color=_c.DEPRESSED_BUTTON, border_color=_c.BORDER_COLOR,
            click_border_color=_c.DEPRESSED_BORDER, border_width=4,
            text_color=_c.BUTTON_TEXT_COLOR, box_color=_c.FG_COLOR,
            click_text_color=_c.DEPRESSED_TEXT_COLOR,
            box_border_color=_c.FG_BORDER_COLOR):
        """
        A class to manage a group of buttons that should be spaced out into a 
        grid. All arguments provided in lists specify functionality in 
        column-major order, values of None in lists will populate a blank space
        in the corresponding position in the grid

        Args
        -----------
        n_rows: the number of rows in the grid
        n_cols: the number of columns in the grid
        col_width: the width of each column in pixels (buttons inherit sizes)
        row_height: the height of each row in pixels (buttons inherit sizes)
        label_list: column-major ordered text to place in each button
        callback_list: column-major ordered functions to associet w/buttons
        disp: pygame display object to draw onto
        x_pos: x-coordinate of the grid's top left corner
        y_pos: y-coordinate of the grid's top left corner
        fit_to_text: boolean to shrink button width to fit text 
        x_pad: spacing between columns in pixels
        y_pad: blank spacing between rows in pixels
        log: logging module instance to write to
        
        NOTE: the remainder of the arguments specify the colors and borders in
              the grid. Each of the color arguments should be provided as an
              RGB tuple such as: (10, 40, 23). Border width is specified in 
              pixels.
        """
        # check for errors in input
        num_buttons = n_rows * n_cols
        if len(label_list) != len(callback_list):
            log.error("label list and callback list must have the same \
                length! (you provided {} and {} respectively)"
                .format(len(label_list), len(callback_list)))
            raise IndexError

        if len(label_list) > num_buttons:
            log.warn("you've provided more button specifications than this \
                grid can accomodate. Your button lists will be truncated. \
                ({} buttons requested, {} available)"
                .format(len(label_list), num_buttons))

        # expand out with blank buttons
        if len(label_list) < num_buttons:
            label_list += [None]*(num_buttons-len(label_list))
            callback_list += [None]*(num_buttons-len(label_list))

        # set up the buttons in memory
        self.buttons = []
        button_idx = 0
        self.disp = disp
        self.box_color = box_color
        self.box_border_color = box_border_color

        # draw the box that encompasses the grid
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.border_width = border_width
        self.box_width = n_cols * (x_pad+col_width) + 2*border_width + x_pad
        self.box_height = n_rows * (y_pad+row_height) + 2*border_width + y_pad
        self.draw_boundary_box()

        # iterate through the rows and columns in column-major order
        for col in range(n_cols):
            for row in range(n_rows):
                # if the label is not None create a button in this position
                if label_list[button_idx] is not None:
                    self.buttons.append(
                        game_button.PGButton(
                            x_pos=x_pos+border_width+x_pad+(x_pad+col_width)*col, 
                            y_pos=y_pos+border_width+y_pad+(y_pad+row_height)*row, 
                            width=col_width, 
                            height=row_height, 
                            text=label_list[button_idx],
                            expand=False, 
                            disp=disp, 
                            log=log,
                            color=color,
                            click_color=click_color, 
                            border_color=border_color,
                            click_border_color=click_border_color, 
                            border_width=border_width,
                            text_color=text_color, 
                            click_text_color=click_text_color)
                    )
                button_idx += 1

    def get_rect(self):
        return (self.x_pos, self.y_pos, self.box_width, self.box_height)

    def get_buttons(self):
        return self.buttons

    def draw_boundary_box(self):
        pygame.draw.rect(self.disp,  
                self.box_border_color,
                self.get_rect())
        pygame.draw.rect(self.disp,
                self.box_color,
                (self.x_pos+self.border_width, 
                    self.y_pos+self.border_width,
                    self.box_width-2*self.border_width, 
                    self.box_height-2*self.border_width)
                )