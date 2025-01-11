from flask import Blueprint, request, jsonify
from app.services.cve_service import CVEService

cve_bp = Blueprint('cve', __name__)
cve_service = CVEService()

@cve_bp.route('/cve', methods=['POST'])
def create_cve():
    data = request.json
    cve = cve_service.create_cve(data)
    return jsonify(cve), 201

@cve_bp.route('/cve/<int:cve_id>', methods=['GET'])
def get_cve(cve_id):
    cve = cve_service.get_cve(cve_id)
    if cve:
        return jsonify(cve), 200
    return jsonify({'message': 'CVE not found'}), 404

@cve_bp.route('/cve/<int:cve_id>', methods=['PUT'])
def update_cve(cve_id):
    data = request.json
    updated_cve = cve_service.update_cve(cve_id, data)
    if updated_cve:
        return jsonify(updated_cve), 200
    return jsonify({'message': 'CVE not found'}), 404

@cve_bp.route('/cve/<int:cve_id>', methods=['DELETE'])
def delete_cve(cve_id):
    success = cve_service.delete_cve(cve_id)
    if success:
        return jsonify({'message': 'CVE deleted'}), 204
    return jsonify({'message': 'CVE not found'}), 404