"""Flask application for triangulation service."""

import requests
from flask import Flask, Response, jsonify

import TP.Code.serializers as serializers
import TP.Code.triangulation as triangulation

app = Flask(__name__)

POINT_SET_MANAGER_URL = "http://localhost:5001/pointsets"

@app.route('/triangulate/<pointset_id>', methods=['GET', 'POST'])
def triangulate_endpoint(pointset_id):
    """Endpoint pour trianguler un PointSet donné par son ID."""
    try:
        response = requests.get(f"{POINT_SET_MANAGER_URL}/{pointset_id}")
        if response.status_code == 404:
            return jsonify({"error": "PointSet not found"}), 404
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "External service unavailable", "details": str(e)}), 503

    # 2. Désérialisation
    try:
        # { changed code }
        data = serializers.bytes_to_pointset(response.content)
        points = data["points"]
    except ValueError as e:
        return jsonify({"error": "Invalid PointSet format", "details": str(e)}), 400
    except Exception:
        return jsonify({"error": "Malformed data"}), 422

    # 3. Triangulation
    try:
        # { changed code }
        result = triangulation.triangulate(points)
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        return jsonify({"error": "Triangulation failed", "details": str(e)}), 500

    # 4. Sérialisation de la réponse
    try:
        # { changed code }
        response_bytes = serializers.triangles_to_bytes(
            len(result),
            result,
            len(points),
            points
        )
        return Response(response_bytes, mimetype='application/octet-stream', status=200)
    except Exception:
        return jsonify({"error": "Serialization failed"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) # pragma: no cover