from flask.json.provider import JSONProvider
from flask import Flask, jsonify, request
import orjson
import tempfile
import os

from flask_caching import Cache

import main
import requests


class ORJSONProvider(JSONProvider):
    def __init__(self, *args, **kwargs):
        self.options = kwargs
        super().__init__(*args, **kwargs)

    def loads(self, s, **kwargs):
        return orjson.loads(s)

    def dumps(self, obj, **kwargs):
        # decode back to str, as orjson returns bytes
        return orjson.dumps(obj, option=orjson.OPT_NON_STR_KEYS).decode('utf-8')


app = Flask(__name__)
app.json = ORJSONProvider(app)


app.config['CACHE_TYPE'] = os.environ.get('CACHE_TYPE', 'redis')
app.config['CACHE_REDIS_URL'] = os.environ.get('CACHE_REDIS_URL', 'redis://localhost:6379/0')

cache = Cache(app)


@app.route('/api/v1/peaks', methods=['POST'])
def peaks():
    req = request.get_json()
    if req is None:
        return jsonify({'error': 'invalid json'}), 400

    if 'audio_url' not in req:
        return jsonify({'error': 'audio_url not provided'}), 400

    @cache.memoize(timeout=None)
    def mem(audio_url_):
        opt = main.OptionHandler()
        options = main.Options()

        # download
        obj = requests.get(audio_url_)
        audio_suffix = audio_url_.split('.')[-1]
        assert obj.status_code == 200
        with tempfile.NamedTemporaryFile(delete=True, suffix=f".{audio_suffix}") as temp_file:
            temp_file.write(obj.content)
            temp_file.seek(0)
            options.setInputFilename(temp_file.name)
            print(temp_file.name)
            options.setInputFormat(audio_suffix)
            options.setOutputFormat("json")
            options.handleZoomOption("256")
            options.handleAmplitudeScaleOption("1.0")

            with tempfile.NamedTemporaryFile(delete=True, suffix=".json") as temp_file1:
                options.setOutputFilename(temp_file1.name)
                assert opt.run(options) is True
                temp_file1.seek(0)
                file_contents = temp_file1.read()
                ret = orjson.loads(file_contents.decode('utf-8'))

        if "data" in ret:
            # divide by ret["sample_rate"]
            for i in range(len(ret["data"])):
                ret["data"][i] = ret["data"][i] / ret["sample_rate"]

        return ret, 200

    audio_url = req['audio_url']
    return mem(audio_url)
