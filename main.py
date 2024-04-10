from flask import Flask, render_template, request
import sys

app = Flask(__name__)

def minDistance(dist, present, n):
    min_val = sys.maxsize
    min_index = -1
    for i in range(n):
        if not present[i] and dist[i] <= min_val:
            min_val = dist[i]
            min_index = i
    return min_index

def displayMinDistance(routers, dist, n):
    result = "Router \t Distance from src<br>"
    for i in range(n):
        result += f"{routers[i]} \t\t {dist[i]}<br>"
    return result

def dijkstra(routers, table, src, n):
    dist = [sys.maxsize] * n
    present = [False] * n
    dist[src] = 0
    for _ in range(n - 1):
        u = minDistance(dist, present, n)
        present[u] = True
        for j in range(n):
            if not present[j] and table[u][j] != 0 and dist[u] != sys.maxsize and dist[u] + table[u][j] < dist[j]:
                dist[j] = dist[u] + table[u][j]
    return displayMinDistance(routers, dist, n)

def linkStateTable(routers, table, n):
    result = ""
    for i in range(n):
        LST = {}
        for j in range(n):
            if table[i][j] != 0:
                LST[routers[j]] = table[i][j]
        result += f"<br>Link State Table for {routers[i]} :<br>"
        for router, distance in LST.items():
            result += f"{router}: {distance}<br>"
    return result

@app.route('/')
def index():
    return render_template('index.html', n=5)  


@app.route('/result', methods=['POST'])
def result():
    n = int(request.form['n'])
    routers = []
    table = [[0] * n for _ in range(n)]
    src = int(request.form['src'])
    for i in range(n):
        x = request.form[f'router_{i}']
        routers.append(x)
    for i in range(n):
        for j in range(n):
            table[i][j] = int(request.form.get(f'table_{i}_{j}', 0))
    link_state_tables = linkStateTable(routers, table, n)
    dijkstra_result = dijkstra(routers, table, src, n)
    return render_template('result.html', link_state_tables=link_state_tables, dijkstra_result=dijkstra_result)

if __name__ == '__main__':
    app.run(debug=True)
