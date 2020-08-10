import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import os.path
from pathlib import Path


class FileManager:

    def __init__(self, output_file):
        self.output_file = output_file
        self.my_file = None

    def get_or_create_file(self, k, l, choose_mode):
        if not os.path.exists(self.output_file + "/" + str(choose_mode)):
            Path(self.output_file + "/" + str(choose_mode)).mkdir(parents=True, exist_ok=True)
        self.output_file += "/" + str(choose_mode)
        if not os.path.exists(self.output_file + "/" + choose_mode + " l=" + str(l)):
            Path(self.output_file + "/" + choose_mode + " l=" + str(l)).mkdir(parents=True, exist_ok=True)
        self.output_file += "/" + choose_mode + " l=" + str(l)
        if len([filename for filename in os.listdir(self.output_file) if
                filename.startswith(choose_mode + " l=" + str(l) + " k=" + str(k) + " ")]) == 0:
            self.output_file += "/" + choose_mode + " l=" + str(l) + " k=" + str(k) + " bs=0.txt"
            self.my_file = open(self.output_file, "w+")
            best_score = 0
        else:
            file_name = [filename for filename in os.listdir(self.output_file) if
                         filename.startswith(choose_mode + " l=" + str(l) + " k=" + str(k) + " ")][0]
            best_score = int(file_name.split(" ")[-1].split(".")[0][3:])
            self.output_file += "/" + file_name
            self.my_file = open(self.output_file, "a+")
        return best_score

    def redo_file(self, best_score, new_text):
        self.my_file.close()
        os.rename(self.output_file, self.rename_best_score_file(best_score))
        self.output_file = self.rename_best_score_file(best_score)
        self.my_file = open(self.output_file, "w+")
        self.my_file.truncate(0)
        self.my_file.write(new_text)

    def update_file(self, new_text):
        self.my_file.write("\n\n\n")
        self.my_file.write(new_text)

    def rename_best_score_file(self, best_score):
        split = self.output_file.split(" ")
        del split[-1]
        split.append("bs=" + str(best_score) + ".txt")
        tmp = ""
        for s in split:
            tmp += s + " "
        tmp = tmp[:len(tmp) - 1]
        return tmp

    def store_counter_example(self, repos_path, file_name, text, cascade_cost, error_step_index):
        if not os.path.exists(repos_path + "/" + "counter_examples"):
            Path(repos_path + "/" + "counter_examples").mkdir(parents=True, exist_ok=True)
        repos_path += "/" + "counter_examples"
        if len([filename for filename in os.listdir(repos_path) if
                filename.startswith(repos_path)]) == 0:
            new_file = open(repos_path + "/" + file_name, "w+")
        else:
            return
        new_file.write(text + "\n\n")
        new_file.write("costs: " + ''.join(str(e) + " " for e in cascade_cost) + "\n" + "error at cascase " + str(error_step_index))




