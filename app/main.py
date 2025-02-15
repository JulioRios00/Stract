from flask import Flask, jsonify, Response, send_file
import processing
import utils

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "name": "Julio Araujo",
        "email": "julio.rios.araujo@gmail.com",
        "Linkedin": "https://www.linkedin.com/in/julio-araujo-a7719267//"
    })

@app.route('/<string:platform>')
def platform_ads(platform):
    ads = processing.get_platforms_data(platform)
    return Response(ads, mimetype="text/csv")

@app.route('/<string:platform>/resumo')
def platform_summary(platform):
    summary = processing.get_platforms_data_summary(platform)
    return Response(summary, mimetype="text/csv")

@app.route('/<string:platform>/download')
def platform_download(platform):
    filename = utils.generate_platform_ads_csv_file(platform)
    return send_file(
        filename,
        as_attachment=True,
        download_name=f"{platform}_ads.csv"
    )

@app.route('/geral')
def general_ads():
    all_ads = processing.get_general_report()
    return Response(all_ads, mimetype="text/csv")

@app.route('/geral/resumo')
def general_summary():
    summary = processing.get_general_summary()
    return Response(summary, mimetype="text/csv")

@app.route('/geral/download')
def general_download():
    filename = utils.generate_general_csv_file()
    return send_file(
        filename,
        as_attachment=True,
        download_name="platform_summary.csv"
    )


if __name__ == "__main__":
    app.run(debug=True)
