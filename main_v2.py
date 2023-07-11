import csv
from datetime import datetime, timedelta

def get_week_range(date):
    # Trova il primo giorno della settimana
    start_of_week = date - timedelta(days=date.weekday())

    # Trova l'ultimo giorno della settimana
    end_of_week = start_of_week + timedelta(days=6)

    return start_of_week, end_of_week

def get_absent_weeks(file_path, email, start_date, end_date):
    present_hours = {}
    all_weeks = set()

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Salta l'intestazione

        for row in reader:
            date_str = row[4]
            attendance_date = datetime.strptime(date_str, '%d/%m/%Y')

            if row[1].lower() == email.lower() and attendance_date >= start_date:
                start_of_week, end_of_week = get_week_range(attendance_date)
                week_range = f"{start_of_week.strftime('%d/%m/%Y')} - {end_of_week.strftime('%d/%m/%Y')}"

                if week_range not in present_hours:
                    present_hours[week_range] = 0

                # Calcola le ore di presenza del tutor nella settimana
                time_range_start = datetime.strptime(row[5], '%H.%M.%S').time()
                time_range_end = datetime.strptime(row[6], '%H.%M.%S').time()
                time_difference = datetime.combine(datetime.min, time_range_end) - datetime.combine(datetime.min, time_range_start)
                present_hours[week_range] += time_difference.total_seconds() / 3600

                all_weeks.add(week_range)

    absent_weeks = []
    for week_range, hours in present_hours.items():
        if hours < 1:
            absent_weeks.append(week_range)

    # Calcola le settimane totali
    current_date = start_date
    while current_date <= end_date:
        start_of_week, end_of_week = get_week_range(current_date)
        week_range = f"{start_of_week.strftime('%d/%m/%Y')} - {end_of_week.strftime('%d/%m/%Y')}"
        all_weeks.add(week_range)
        current_date += timedelta(days=7)

    absent_weeks = list(all_weeks - set(present_hours.keys()))
    absent_weeks.sort(key=lambda x: datetime.strptime(x.split(' - ')[0], '%d/%m/%Y'))

    return absent_weeks

file_path = "E:\Matthew_Chen\Download\Modulo disponibilità Tutor (Risposte) - Risposte del modulo 1.csv"  # Sostituisci con il percorso del tuo file CSV
start_date = datetime.strptime('30/03/2023', '%d/%m/%Y')  # Sostituisci con la data di inizio da cui vuoi contare le settimane di assenza
#end_date = datetime.strptime('30/03/2023', '%d/%m/%Y')
end_date = datetime.today()
emails_file_path = 'emails.txt'  # Sostituisci con il percorso del tuo file txt contenente la lista di email

emails = []
with open(emails_file_path, 'r') as file:
     for line in file:
         email = line.strip()
         emails.append(email)

for email in emails:
    absent_weeks = get_absent_weeks(file_path, email, start_date, end_date)
    with open('assenze.txt', 'a') as file:
        file.write(f"{email}:\n")
        for week_range in absent_weeks:
            file.write(f"- {week_range}\n")
        file.write("\n")





