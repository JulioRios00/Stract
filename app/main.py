from flask import Flask, jsonify, Response, send_file
import processing
from flask_restx import Api, Resource
import utils

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Stract processo seletivo",
    description="Api desenvolvida para processo seletivo na Stract",
)

ns = api.namespace('Stract', description='Stract operations')

@ns.route('/')
class Home(Resource):
    @ns.doc('get_home')
    def get(self):
        return jsonify({
            "name": "Julio Araujo",
            "email": "julio.rios.araujo@gmail.com",
            "Linkedin": "https://www.linkedin.com/in/julio-araujo-a7719267//"
        })

@ns.route('/<string:platform>')
class PlatformAds(Resource):
    @ns.doc('get_platform_ads')
    @ns.param('platform', 'The platform name (meta_ads, ga4, tiktok_insights)')
    def get(self, platform):
        ads = processing.get_platforms_data(platform)
        return Response(ads, mimetype="text/csv")

@ns.route('/<string:platform>/resumo')
class PlatformSummary(Resource):
    @ns.doc('get_platform_summary')
    @ns.param('platform', 'The platform name (meta_ads, ga4, tiktok_insights)')
    def get(self, platform):
        summary = processing.get_platforms_data_summary(platform)
        return Response(summary, mimetype="text/csv")

@ns.route('/<string:platform>/download')
class PlatformDownload(Resource):
    @ns.doc('download_platform_ads')
    @ns.param('platform', 'The platform name (meta_ads, ga4, tiktok_insights)')
    def get(self, platform):
        filename = utils.generate_platform_ads_csv_file(platform)
        return send_file(
            filename, 
            as_attachment=True,
            download_name=f"{platform}_ads.csv"
        )

@ns.route('/geral')
class GeneralAds(Resource):
    @ns.doc('get_all_ads')
    def get(self):
        all_ads = processing.get_general_report()
        return Response(all_ads, mimetype="text/csv")

@ns.route('/geral/resumo')
class GeneralSummary(Resource):
    @ns.doc('get_general_summary')
    def get(self):
        summary = processing.get_general_summary()
        return Response(summary, mimetype="text/csv")

@ns.route('/geral/download')
class GeneralDownload(Resource):
    @ns.doc('download_general_summary')
    def get(self):
        filename = utils.generate_general_csv_file()
        return send_file(
            filename,
            as_attachment=True,
            download_name="platform_summary.csv"
        )

if __name__ == "__main__":
    app.run(debug=True)