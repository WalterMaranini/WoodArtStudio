from flask import Flask, render_template, redirect, request, send_from_directory, session
from werkzeug.utils import secure_filename

import sqlite3
import os
import datetime

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = 'fggsagejhtewr'

# socket = SocketIO(app)
# somelist = ['mela', 'pera', 'banana', 'arancia']
i=0
DataBasePath = './database.db'
StaticsPath = "./static"


@app.route('/')
def index():
    session['refresh_time'] = 10
    return render_template('Index.html')


@app.route('/ElencoLog', methods=['GET', 'POST'])
def loggerview():
    if request.method == 'POST':
        session['refresh_time'] = request.form['refresh_time']
    connection = sqlite3.connect(DataBasePath)
    connection.row_factory = sqlite3.Row
    logs = connection.execute('SELECT * FROM Logging').fetchall()
    connection.close()
    return render_template('ElencoLog.html', logs=logs, refresh_time=session['refresh_time'])


@app.route('/EliminaTuttiLog', methods=['GET',])
def loggerviewdeleteall():
    connection = sqlite3.connect(DataBasePath)
    connection.row_factory = sqlite3.Row
    connection.execute('DELETE FROM Logging')
    connection.commit()
    connection.close()
    return redirect('/ElencoLog')


@app.route('/ElencoVersioni', methods=['GET',])
def firmwareversioni():
    connection = sqlite3.connect(DataBasePath)
    connection.row_factory = sqlite3.Row
    versioni = connection.execute('SELECT * FROM VersioniFirmware').fetchall()
    connection.close()
    return render_template('ElencoVersioni.html', versioni=versioni)


@app.route('/<int:idv>/VersionDelete', methods=('POST',))
def versiondelete(idv):
    connection = sqlite3.connect(DataBasePath)
    connection.row_factory = sqlite3.Row
    connection.execute('DELETE FROM VersioniFirmware WHERE IdVersione=?', (idv,))
    connection.commit()
    connection.close()
    return redirect('/ElencoVersioni')


@app.route('/NuovaVersione', methods=['GET', 'POST'])
def nuova_versione():
    if request.method == 'POST':
        codice_versione = request.form['CodiceVersione']
        data_versione = request.form['DataVersione']
        descrizione_versione = request.form['DescrizioneVersione']
        connection = sqlite3.connect(DataBasePath)
        connection.row_factory = sqlite3.Row
        connection.execute('INSERT INTO VersioniFirmware (CodiceVersione, DataVersione, DescrizioneVersione) VALUES (?, ?, ?)',
                           (codice_versione, data_versione, descrizione_versione))
        connection.commit()
        connection.close()
        return redirect('/ElencoVersioni')
    return render_template('NuovaVersione.html')


@app.route('/<string:codversione>/UploadVersione', methods=('GET', 'POST',))
def upload_versione(codversione):
    if request.method == 'POST':
        file = request.files['file']
        filename = codversione
        file.save(os.path.join(StaticsPath, filename))
        return 'file uploaded successfully'
    return render_template('UploadVersione.html', codice_versione=codversione)


@app.route('/<int:idx>/delete', methods=('POST',))
def delete(idx):
    connection = sqlite3.connect(DataBasePath)
    connection.row_factory = sqlite3.Row
    connection.execute('DELETE FROM Posts WHERE id=?', (idx,))
    connection.commit()
    connection.close()
    return redirect('/')


@app.route('/<int:idr>/download', methods=('POST',))
def download(idr):
    connection = sqlite3.connect(DataBasePath)
    connection.row_factory = sqlite3.Row
    row = connection.execute('SELECT info FROM Posts WHERE id=?', (idr,)).fetchone()
    connection.close()
    return send_from_directory(StaticsPath, row['info'], as_attachment=True)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        tit = request.form['title']
        info = request.form['content']
        connection = sqlite3.connect(DataBasePath)
        connection.row_factory = sqlite3.Row
        connection.execute('INSERT INTO Posts (titolo, info) VALUES (?, ?)', (tit, info))
        connection.commit()
        connection.close()
        return redirect('/')
    return render_template('create.html')


@app.route('/logger/<string:log>', methods=['GET',])
def logger(log):
    DataOraAttuale = datetime.datetime.now()
    connection = sqlite3.connect(DataBasePath)
    connection.row_factory = sqlite3.Row
    connection.execute('INSERT INTO Logging (LogMessage, Data) VALUES (?, ?)', (log, DataOraAttuale))
    connection.commit()
    connection.close()
    return "log caricato"


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(StaticsPath, filename))
        return 'file uploaded successfully'


@app.route('/StaticFiles/<path:filename>', methods=['GET', ])
def downloadfile(filename):
    return send_from_directory(StaticsPath, filename)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

