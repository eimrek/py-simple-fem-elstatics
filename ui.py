'''
Created on 23 Jan 2015

@author: Kristjan
'''

from PySide.QtCore import *
from PySide.QtGui import *

from fem.controller import Controller

class UI(QWidget):
    def __init__(self, controller, parent=None):
        super(UI, self).__init__(parent)
        
        self.controller = controller
        
        self.h1_font = QFont("Arial", 10, QFont.Bold)
        
        main_layout = QGridLayout()
        
        self.init_geometry()
        main_layout.addLayout(self.geom_layout, 0, 0, 3, 1)
        
        self.init_mesh()
        main_layout.addLayout(self.mesh_layout, 0, 1)
        
        self.init_solver()
        main_layout.addLayout(self.solver_layout, 1, 1)
        
        self.setLayout(main_layout)
        self.setWindowTitle("FEM electric field modelling")
        
    
    def init_geometry(self):
        geom_heading = QLabel("Geometry")
        geom_heading.setFont(self.h1_font)
        
        type_label = QLabel("Type:")
        self.type_select = QComboBox()
        self.type_select.addItems(['2D', '2D axisymmetric'])
        
        type_layout = QGridLayout()
        type_layout.addWidget(type_label, 0, 0)
        type_layout.addWidget(self.type_select, 0, 1)
        
        limits_label = QLabel("Limits:")
        x_min_label = QLabel("x_min:")
        x_min = QLineEdit("-100.0")
        x_max_label = QLabel("x_max:")
        x_max = QLineEdit("100.0")
        y_min_label = QLabel("y_min:")
        y_min = QLineEdit("-100.0")
        y_max_label = QLabel("y_max:")
        y_max = QLineEdit("100.0")
        init_geom = QPushButton("Initialise/reset geometry")
        init_geom.clicked.connect(lambda: self.reset_geom(x_min.text(), x_max.text(),
                                                          y_min.text(), y_max.text()))
        
        limits_layout = QGridLayout()
        limits_layout.addWidget(limits_label, 0, 0)
        limits_layout.addWidget(x_min_label, 1, 0)
        limits_layout.addWidget(x_min, 1, 1)
        limits_layout.addWidget(x_max_label, 1, 2)
        limits_layout.addWidget(x_max, 1, 3)
        limits_layout.addWidget(y_min_label, 2, 0)
        limits_layout.addWidget(y_min, 2, 1)
        limits_layout.addWidget(y_max_label, 2, 2)
        limits_layout.addWidget(y_max, 2, 3)
        limits_layout.addWidget(init_geom, 3, 0, 1, 4)
        
        circ_label = QLabel("Add circular electrode:")
        c_x_label = QLabel("x:")
        circ_x = QLineEdit("0.0")
        c_y_label = QLabel("y:")
        circ_y = QLineEdit("0.0")
        c_R_label = QLabel("R:")
        circ_R = QLineEdit("0.0")
        c_U_label = QLabel("U:")
        circ_U = QLineEdit("0.0")
        add_circ = QPushButton("Add circular electrode")
        add_circ.clicked.connect(lambda: self.add_circular_el(circ_x.text(), circ_y.text(),
                                                      circ_R.text(), circ_U.text()))
        
        circ_layout = QGridLayout()
        circ_layout.addWidget(circ_label, 0, 0)
        circ_layout.addWidget(c_x_label, 1, 0)
        circ_layout.addWidget(circ_x, 1, 1)
        circ_layout.addWidget(c_y_label, 2, 0)
        circ_layout.addWidget(circ_y, 2, 1)
        circ_layout.addWidget(c_R_label, 3, 0)
        circ_layout.addWidget(circ_R, 3, 1)
        circ_layout.addWidget(c_U_label, 4, 0)
        circ_layout.addWidget(circ_U, 4, 1)
        circ_layout.addWidget(add_circ, 5, 0)
        
        rec_label = QLabel("Add rectangular electrode:")
        r_x1_label = QLabel("x1:")
        rec_x1 = QLineEdit("0.0")
        r_y1_label = QLabel("y1:")
        rec_y1 = QLineEdit("0.0")
        r_x2_label = QLabel("x2:")
        rec_x2 = QLineEdit("0.0")
        r_y2_label = QLabel("y2:")
        rec_y2 = QLineEdit("0.0")
        r_U_label = QLabel("U:")
        rec_U = QLineEdit("0.0")
        add_rec = QPushButton("Add rectangular electrode")
        add_rec.clicked.connect(lambda: self.add_rect_el(rec_x1.text(), rec_y1.text(),
                                                   rec_x2.text(), rec_y2.text(), rec_U.text()))
        
        rec_layout = QGridLayout()
        rec_layout.addWidget(rec_label, 0, 0)
        rec_layout.addWidget(r_x1_label, 1, 0)
        rec_layout.addWidget(rec_x1, 1, 1)
        rec_layout.addWidget(r_y1_label, 2, 0)
        rec_layout.addWidget(rec_y1, 2, 1)
        rec_layout.addWidget(r_x2_label, 3, 0)
        rec_layout.addWidget(rec_x2, 3, 1)
        rec_layout.addWidget(r_y2_label, 4, 0)
        rec_layout.addWidget(rec_y2, 4, 1)
        rec_layout.addWidget(r_U_label, 5, 0)
        rec_layout.addWidget(rec_U, 5, 1)
        rec_layout.addWidget(add_rec, 6, 0)
        
        self.geom_list = QListWidget()
        remove_sel = QPushButton("Remove selected (not impl.)")
        list_layout = QGridLayout()
        list_layout.addWidget(self.geom_list, 0, 0, 1, 2)
        list_layout.addWidget(remove_sel, 1, 1)
        
        draw_geom = QPushButton("Draw geometry")
        draw_geom.clicked.connect(self.controller.draw_geom)
        
        self.geom_layout = QGridLayout()
        self.geom_layout.addWidget(geom_heading, 0, 0)
        self.geom_layout.addLayout(type_layout, 1, 0)
        self.geom_layout.addLayout(limits_layout, 2, 0)
        self.geom_layout.addLayout(circ_layout, 3, 0)
        self.geom_layout.addLayout(rec_layout, 4, 0)
        self.geom_layout.addLayout(list_layout, 1, 1, 4, 1)
        self.geom_layout.addWidget(draw_geom, 5, 0, 1, 2)
    
    def reset_geom(self, xmin, xmax, ymin, ymax):
        try:
            self.controller.reset_geom(float(xmin), float(xmax), float(ymin), float(ymax))
            self.geom_list.clear()
        except ValueError:
            QMessageBox.information(self, "Input error",
                                    "The input format is incorrect.")
             
    def add_circular_el(self, x, y, R, u):
        try:
            self.controller.geometry.add_circular(float(x), float(y),
                                                  float(R), float(u))
            self.geom_list.addItem("Circular ("+ x + ", "+ y+ ", "+ R + ", "+u + ")")
        except ValueError:
            QMessageBox.information(self, "Input error",
                                    "The input format is incorrect.")
    
    def add_rect_el(self, x1, y1, x2, y2, u):
        try:
            self.controller.geometry.add_rectangular(float(x1), float(y1),
                                                  float(x2), float(y2), float(u))
            self.geom_list.addItem("Rectangular ("+ x1 + ", "+ y1+ ", "+ x2 + ", "+y2+", "+u + ")")
        except ValueError:
            QMessageBox.information(self, "Input error",
                                    "The input format is incorrect.")
    
    def init_mesh(self):
        mesh_heading = QLabel("Mesh")
        mesh_heading.setFont(self.h1_font)
        
        xstep_label = QLabel("x_step:")
        xstep = QLineEdit("3.0")
        xstep.setMaximumWidth(100)
        ystep_label = QLabel("y_step:")
        ystep = QLineEdit("3.0")
        ystep.setMaximumWidth(100)
        gen_mesh = QPushButton("Generate mesh")
        gen_mesh.setMaximumHeight(100);
        gen_mesh.clicked.connect(lambda: self.generate_mesh(xstep.text(), ystep.text()))
        
        draw_elem = QCheckBox("Draw elem. lines (slow)")
        draw_mesh = QPushButton("Draw mesh")
        draw_mesh.clicked.connect(lambda: self.draw_mesh(draw_elem.isChecked()))
        
        self.mesh_layout = QGridLayout()
        self.mesh_layout.addWidget(mesh_heading, 0, 0)
        self.mesh_layout.addWidget(xstep_label, 1, 0)
        self.mesh_layout.addWidget(xstep, 1, 1)
        self.mesh_layout.addWidget(ystep_label, 2, 0)
        self.mesh_layout.addWidget(ystep, 2, 1)
        self.mesh_layout.addWidget(gen_mesh, 1, 2, 2, 1)
        self.mesh_layout.addWidget(draw_elem, 3, 0)
        self.mesh_layout.addWidget(draw_mesh, 4, 0)
        
    def generate_mesh(self, xstep, ystep):
        try:
            self.controller.generate_mesh(float(xstep), float(ystep))
        except ValueError:
            QMessageBox.information(self, "Input error",
                                    "The input format is incorrect.")
    
    def draw_mesh(self, elem_lines):
        nodes_only = not elem_lines
        try:
            self.controller.draw_mesh(nodes_only)
        except AttributeError:
            QMessageBox.information(self, "Attribute error",
                                    "Generate the mesh first.")
    
    def init_solver(self):
        solver_heading = QLabel("Solver")
        solver_heading.setFont(self.h1_font)
        
        desc = QLabel("Solver type and system matrix storage:")
        solver_select = QComboBox()
        solver_select.addItems(['Numpy/Numpy matrix', 'Gaussian el./Numpy matrix',
                                'Gaussian el./skyline storage (not impl.)'])
        
        solve = QPushButton("Solve")
        solve.clicked.connect(lambda: self.controller.solve(self.type_select.currentIndex(),
                                                            solver_select.currentIndex()))
        
        with_nodes = QCheckBox("Draw mesh nodes")
        with_geom = QCheckBox("Draw geometry")
        with_geom.setChecked(True)
        draw_sol = QPushButton("Draw solution")
        draw_sol.clicked.connect(lambda: self.controller.draw_solution(with_nodes.isChecked(),
                                                                       with_geom.isChecked()))
        
        probe_label = QLabel("Probe value at point")
        pr_x_label = QLabel("x:")
        pr_x = QLineEdit("0.0")
        pr_y_label = QLabel("y:")
        pr_y = QLineEdit("0.0")
        probe = QPushButton("Probe:")
        probe.clicked.connect(lambda: self.probe_value(pr_x.text(), pr_y.text()))
        self.val =  QLineEdit("")
        self.val.setReadOnly(True)
        
        probe_layout = QGridLayout()
        probe_layout.addWidget(probe_label, 0, 0)
        probe_layout.addWidget(pr_x_label, 0, 1)
        probe_layout.addWidget(pr_x, 0, 2)
        probe_layout.addWidget(pr_y_label, 1, 1)
        probe_layout.addWidget(pr_y, 1, 2)
        probe_layout.addWidget(probe, 2, 0)
        probe_layout.addWidget(self.val, 2, 1)
        
        
        self.solver_layout = QGridLayout()
        self.solver_layout.addWidget(solver_heading, 0, 0)
        self.solver_layout.addWidget(desc, 1, 0)
        self.solver_layout.addWidget(solver_select, 1, 1)
        self.solver_layout.addWidget(solve, 2, 0)
        self.solver_layout.addWidget(with_nodes, 3, 0)
        self.solver_layout.addWidget(with_geom, 4, 0)
        self.solver_layout.addWidget(draw_sol, 5, 0, 1, 2)
        self.solver_layout.addLayout(probe_layout, 6, 0, 2, 2)
        
    def probe_value(self, x, y):
        try:
            self.val.setText(str(self.controller.probe_value(float(x), float(y))))
        except ValueError:
                QMessageBox.information(self, "Input error",
                                    "The input format is incorrect.")

if __name__ == '__main__':
    import sys
    
    app = QApplication(sys.argv)
    
    controller = Controller()
 
    ui = UI(controller)
    ui.show()
 
    sys.exit(app.exec_())