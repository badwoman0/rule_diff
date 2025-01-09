from flask import Flask, request, jsonify, render_template, send_file
import csv
from logic.file_handler import parse_conf, compare_configs, write_differences_to_xlsx

app = Flask(__name__)

@app.route('/upload/default', methods=['POST'])
def upload_default_config():
    file = request.files['file']
    # 保存上传的文件到指定路径
    file_path = '/tmp/default.conf'
    file.save(file_path)

    try:
        parsed_data = parse_conf(file_path)
        return jsonify({'message': '默认配置文件解析成功'})
    except Exception as e:
        return jsonify({'error': '默认配置文件解析失败', 'details': str(e)}), 400

@app.route('/upload/customer', methods=['POST'])
def upload_customer_config():
    file = request.files['file']
    # 保存上传的文件到指定路径
    file_path = '/tmp/customer.conf'
    file.save(file_path)

    try:
        parsed_data = parse_conf(file_path)
        return jsonify({'message': '用户配置文件解析成功'})
    except Exception as e:
        return jsonify({'error': '用户配置文件解析失败', 'details': str(e)}), 400

@app.route('/generate_diff', methods=['GET'])
def generate_diff():
    try:
        # 假设默认配置和客户配置文件路径
        default_conf_path = '/tmp/default.conf'
        customer_conf_path = '/tmp/customer.conf'

        # 比较配置文件并生成差异
        differences = compare_configs(default_conf_path, customer_conf_path)
        xlsx_path = '/tmp/differences.xlsx'
        # 生成XLSX文件
        write_differences_to_xlsx(differences, xlsx_path)

        # 提供XLSX文件下载
        return send_file(xlsx_path, as_attachment=True, download_name='differences.xlsx')
    except Exception as e:
        return jsonify({'error': 'Failed to compare', 'details': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
