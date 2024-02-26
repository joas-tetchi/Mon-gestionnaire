import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QListWidget, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QCalendarWidget, QTimeEdit, QGroupBox, QMessageBox 
from PySide6.QtCore import Qt, QTime, QDate, QTimer

class TaskManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire de Tâches")
        self.setGeometry(100, 100, 600, 400)  # Ajustement de la taille de la fenêtre
        self.setStyleSheet("background-color: gray;")


        # Création du groupe de boîtes pour centrer les éléments
        group_box = QGroupBox()
        self.setCentralWidget(group_box)
        group_box.setContentsMargins(300,0,300,0)

        # Création du layout principal pour le groupe de boîtes
        layout = QVBoxLayout()
        group_box.setLayout(layout)

        # Champ de saisie pour le nom de la tâche
        name_layout = QHBoxLayout()
        name_label = QLabel("Nom de la Tâche:")
        self.task_name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.task_name_input)

        # Ajout du layout du nom au layout principal
        layout.addLayout(name_layout)

        # Sélection de la date de la tâche
        date_layout = QHBoxLayout()
        date_label = QLabel("Date:")
        self.date_calendar = QCalendarWidget()
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_calendar)

        # Ajout du layout de la date au layout principal
        layout.addLayout(date_layout)

        # Sélection de l'heure de la tâche
        time_layout = QHBoxLayout()
        time_label = QLabel("Heure:")
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_edit)

        # Ajout du layout de l'heure au layout principal
        layout.addLayout(time_layout)

        # Bouton pour ajouter une tâche
        add_button = QPushButton("Ajouter Tâche")
        add_button.clicked.connect(self.add_task)
        layout.addWidget(add_button)

        # Liste des tâches
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        # Création du layout horizontal pour les boutons Supprimer, Sauvegarder et Compléter
        button_layout = QHBoxLayout()

        # Bouton pour supprimer une tâche
        remove_button = QPushButton("Supprimer")
        remove_button.clicked.connect(self.remove_task)
        button_layout.addWidget(remove_button)

        # Bouton pour sauvegarder les tâches
        save_button = QPushButton("Sauvegarder")
        save_button.clicked.connect(self.save_tasks)
        button_layout.addWidget(save_button)

        # Bouton pour marquer une tâche comme complétée
        complete_button = QPushButton("Marqué comme ...")
        complete_button.clicked.connect(self.show_completion_options)
        button_layout.addWidget(complete_button)

        # Ajout du layout horizontal des boutons au layout principal
        layout.addLayout(button_layout)

        # Widget pour le cadre d'affichage des tâches sauvegardées
        saved_tasks_frame = QWidget()
        saved_tasks_frame_layout = QVBoxLayout()

        # Étiquette pour le titre de la liste des tâches sauvegardées
        saved_tasks_label = QLabel("Liste des Tâches Sauvegardées")
        saved_tasks_frame_layout.addWidget(saved_tasks_label)

        # Liste des tâches sauvegardées chargées depuis le fichier "gestionnaire.txt"
        self.saved_tasks_list = QListWidget()
        saved_tasks_frame_layout.addWidget(self.saved_tasks_list)

        saved_tasks_frame.setLayout(saved_tasks_frame_layout)
        layout.addWidget(saved_tasks_frame)

        # Bouton pour charger les tâches sauvegardées et compléter
        load_complete_layout = QHBoxLayout()

        # Bouton pour marquer une tâche comme complétée
        load_saved_button = QPushButton("Charger")
        load_saved_button.clicked.connect(self.load_saved_tasks)
        load_complete_layout.addWidget(load_saved_button)

        layout.addLayout(load_complete_layout)

        # Liste des tâches sauvegardées
        self.saved_tasks = []

        # Timer pour vérifier l'état des tâches
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_task_status)
        self.timer.start(60000)  # Vérification toutes les minutes

    def add_task(self):
        task_name = self.task_name_input.text()
        task_date = self.date_calendar.selectedDate().toString(Qt.ISODate)
        task_time = self.time_edit.time().toString(Qt.ISODate)

        # Ajouter la tâche à la liste des tâches
        self.task_list.addItem(f"Nom: {task_name}, Date: {task_date}, Heure: {task_time}")

        # Ajouter la tâche à la liste des tâches sauvegardées
        self.saved_tasks.append((task_name, task_date, task_time))

        # Effacer les champs de saisie après l'ajout de la tâche
        self.task_name_input.clear()

    def remove_task(self):
        selected_items = self.task_list.selectedItems()
        for item in selected_items:
            self.task_list.takeItem(self.task_list.row(item))

    def save_tasks(self):
        with open("gestionnaire.txt", "w") as file:
            for task in self.saved_tasks:
                file.write(f"{task[0]},{task[1]},{task[2]}\n")

    def load_saved_tasks(self):
        self.saved_tasks_list.clear()
        self.saved_tasks.clear()
        try:
            with open("gestionnaire.txt", "r") as file:
                tasks = file.readlines()
                for task in tasks:
                    task_data = task.strip().split(',')
                    self.saved_tasks.append((task_data[0], task_data[1], task_data[2]))
                    self.saved_tasks_list.addItem(f"Nom: {task_data[0]}, Date: {task_data[1]}, Heure: {task_data[2]}")
        except FileNotFoundError:
            pass

    def show_completion_options(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            return

        completion_options = QMessageBox(self)
        completion_options.setWindowTitle("Options de Complétion")
        completion_options.setText("Sélectionnez l'état de la tâche:")
        completion_options.addButton("Terminé", QMessageBox.AcceptRole)
        completion_options.addButton("Annulé", QMessageBox.RejectRole)

        def handle_completion(option):
            if option.text() == "Terminé":
                for item in selected_items:
                    item.setBackground(Qt.green)
            elif option.text() == "Annulé":
                for item in selected_items:
                    item.setBackground(Qt.magenta)

        # Déconnexion de la fermeture de l'application
        completion_options.rejected.connect(completion_options.reject)

        completion_options.buttonClicked.connect(handle_completion)
        completion_options.open()

    def check_task_status(self):
        # Implémentez ici la logique pour vérifier l'état des tâches et mettre à jour l'affichage
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManagerApp()
    window.show()
    sys.exit(app.exec())
