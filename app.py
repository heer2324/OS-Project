#setup backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from flask import Flask, flash, redirect, render_template, request
import helpers
import matplotlib.pyplot as plt

# Configure application
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/SRTN", methods = ["GET", "POST"])
def SRTN():
    if request.method == "GET":
        return render_template("srtn-input.html")
    else:
        num = int(request.form.get("n"))
        arrival = []
        burst = []
        for i in range(num):
            arrival.append(int(request.form.get(f"arrival_time_{i}")))
            burst.append(int(request.form.get(f"burst_time_{i}")))
        
        CT = [0] * num
        TAT = [0] * num
        WT = [0] * num
        process = ""  # 0123
        time = -1
        countProcess = 0

        BT = burst.copy()

        while countProcess != num:
            time += 1
            index = 0
            min_burst = float('inf')

            for i in range(num):
                if burst[i] != 0 and arrival[i] <= time and min_burst > burst[i]:
                    min_burst = burst[i]
                    index = i

            if min_burst == float('inf'):
                process += "null "
            else:
                burst[index] -= 1
                if burst[index] == 0:
                    countProcess += 1
                    CT[index] = time + 1
                process += "P" + str(index) + " "

        for i in range(num):
            TAT[i] = CT[i] - arrival[i]
            WT[i] = TAT[i] - BT[i]

        avg_TAT = sum(TAT)/len(TAT)
        avg_WT = sum(WT)/len(WT)
        
        return render_template('srtn-output.html', gantt_string = process.rstrip(), arrival_times=arrival, burst_times=BT,
                           completion_times=CT, turnaround_times=TAT,
                           waiting_times=WT, avg_waiting_time = avg_WT, avg_turnaround_time = avg_TAT)
        

@app.route("/Proucer-Consumer")
def producer_consumer():
    return render_template("producer_consumer.html")

@app.route("/OPR", methods = ["GET", "POST"])
def OPR():
    if request.method == "GET":
        return render_template("opr-input.html")
    else:
        no_of_frames = int(request.form.get("frames"))
        no_of_pages = int(request.form.get("pages"))
        pages = []
        for i in range(1,no_of_pages+1):
            pages.append(int(request.form.get(f"page-{i}")))
        matrix, page_faults, replacements = helpers.optimal_page_replacement(pages, no_of_frames)
        return render_template("opr-output.html", table_data = matrix, pages = pages)



@app.route("/SSTF", methods = ["GET", "POST"])
def SSTF():
    if request.method == "GET":
        return render_template("sstf-input.html")
    else:
        position = int(request.form.get("position"))
        no_of_requests = int(request.form.get("requests"))
        tracks = []
        for i in range(1,no_of_requests+1):
            tracks.append(int(request.form.get(f"track-{i}")))
        
        total_seek_time, sequence = helpers.sstf(position, tracks)

        print("Sequence of executed requests:", sequence)
        print("Total seek time:", total_seek_time)
    
        plt.figure(figsize=(10, 6))
        plt.plot([position] + sequence, list(range(len(sequence) + 1)), marker='o', linestyle='-', label='Head Movement')
        plt.title('SSTF Disk Scheduling')
        plt.xlabel('Track')
        plt.ylabel('Time')
        plt.legend()
        plt.grid(True)
        plt.savefig('static/graph.png')
        return render_template("sstf-output.html", sequence=sequence, total_seek_time=total_seek_time)

    
