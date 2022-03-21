from multiprocessing import Process

from appointments import BackgroundAppointments

if __name__ == '__main__':
    notifiers = BackgroundAppointments().run_notify
    reminders = BackgroundAppointments().run_remind

    n_service = Process(target=notifiers)
    r_service = Process(target=reminders)

    n_service.start()
    r_service.start()
